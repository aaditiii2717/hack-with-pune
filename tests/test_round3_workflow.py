"""End-to-end acceptance checks for the role-based software handover."""
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

# Isolate tests from any local .env credentials or a developer's configured database.
os.environ["DATABASE_URL"] = ""
os.environ["KC_DEMO_MODE"] = "1"
os.environ["COOKIE_SECURE"] = "1"
os.environ["GROQ_API_KEY"] = ""

import server  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


class HandoverJourneyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        data = Path(self.tmp.name) / "data"
        data.mkdir()
        server.DATA = data
        server.DB = data / "test.sqlite3"
        server.UPLOADS = data / "uploads"
        server.UPLOADS.mkdir()
        server.USE_POSTGRES = False
        server.init_db()
        self.client = TestClient(server.app, base_url="https://testserver")
        self.client.__enter__()

    def tearDown(self) -> None:
        self.client.__exit__(None, None, None)
        self.tmp.cleanup()

    def demo_login(self, role: str) -> None:
        response = self.client.post("/api/kc/demo/session", json={"role": role})
        self.assertEqual(response.status_code, 200, response.text)

    def test_reviewer_intern_recipient_journey_and_permissions(self) -> None:
        self.assertEqual(self.client.get("/api/health").json()["status"], "ok")
        self.assertIn("Knowledge Continuity", self.client.get("/").text)

        self.demo_login("admin")
        templates = self.client.get("/api/kc/templates").json()
        software = next(t for t in templates if t["id"] == "software-project")
        self.assertGreaterEqual(len(software["fields"]), 14)
        self.assertIn("tests", {field["key"] for field in software["fields"]})

        created = self.client.post("/api/kc/handovers", json={
            "template_id": "software-project",
            "title": "Round 3 test feature handoff",
            "departing_person": "Demo Intern",
            "recipient": "Demo Engineer",
            "owner": "Demo Reviewer",
            "employee_id": "demo_intern",
            "recipient_id": "demo_engineer",
        })
        self.assertEqual(created.status_code, 200, created.text)
        handover_id = created.json()["handover"]["id"]
        self.assertEqual(len(created.json()["fields"]), len(software["fields"]))

        self.demo_login("employee")
        self.assertEqual(self.client.post(f"/api/kc/handovers/{handover_id}/publish").status_code, 403)
        source = self.client.post(f"/api/kc/handovers/{handover_id}/sources", json={
            "name": "Feature notes", "source_type": "text",
            "content": "The current feature is a prototype. Run tests with python -m unittest discover -s tests. The next engineer should verify the API and database contract.",
            "added_by": "Demo Intern",
        })
        self.assertEqual(source.status_code, 200, source.text)
        self.assertEqual(self.client.post(f"/api/kc/handovers/{handover_id}/submit").json()["status"], "Submitted")
        self.demo_login("recipient")
        self.assertEqual(self.client.get(f"/api/kc/handovers/{handover_id}/recipient").status_code, 403)

        self.demo_login("admin")
        handover = self.client.get(f"/api/kc/handovers/{handover_id}").json()
        for field in handover["fields"]:
            saved = self.client.patch(f"/api/kc/fields/{field['id']}", json={
                "value": f"Reviewer-confirmed test content for {field['label']}.",
                "state": "Manual", "visible_to_recipient": True,
            })
            self.assertEqual(saved.status_code, 200, saved.text)
            approved = self.client.post(f"/api/kc/fields/{field['id']}/approve")
            self.assertEqual(approved.status_code, 200, approved.text)

        published = self.client.post(f"/api/kc/handovers/{handover_id}/publish")
        self.assertEqual(published.status_code, 200, published.text)
        self.assertEqual(published.json()["version"], 1)
        self.assertEqual(self.client.post(f"/api/kc/handovers/{handover_id}/publish").status_code, 409)

        self.demo_login("recipient")
        recipient_view = self.client.get(f"/api/kc/handovers/{handover_id}/recipient")
        self.assertEqual(recipient_view.status_code, 200, recipient_view.text)
        self.assertTrue(all(field["approved"] for field in recipient_view.json()["fields"]))
        self.assertTrue(all("owner_note" not in field for field in recipient_view.json()["fields"]))
        self.assertEqual(self.client.post(f"/api/kc/handovers/{handover_id}/ask", json={"question": "What is the next step?"}).status_code, 200)
        self.assertEqual(self.client.post(f"/api/kc/handovers/{handover_id}/acknowledge", json={"name": "Demo Engineer"}).status_code, 200)

    def test_invalid_input_and_unauthenticated_access_fail_cleanly(self) -> None:
        self.assertEqual(self.client.get("/api/kc/handovers").status_code, 401)
        self.demo_login("admin")
        malformed = self.client.post("/api/kc/templates", content="{", headers={"content-type":"application/json"})
        self.assertEqual(malformed.status_code, 400)
        invalid_template = self.client.post("/api/kc/templates", json={"name":"Empty","fields":[]})
        self.assertEqual(invalid_template.status_code, 422)


if __name__ == "__main__":
    unittest.main()
