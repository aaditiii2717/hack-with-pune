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
        self.assertIn("png", self.client.get("/api/kc/capabilities").json()["uploads"])

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
        image = self.client.post(
            f"/api/kc/handovers/{handover_id}/upload",
            data={"description": "A marked-up architecture diagram showing the API boundary."},
            files={"file": ("architecture.png", b"\x89PNG\r\n\x1a\nsynthetic", "image/png")},
        )
        self.assertEqual(image.status_code, 200, image.text)
        image_detail = self.client.get(f"/api/kc/handovers/{handover_id}").json()
        image_source = next(source for source in image_detail["sources"] if source["id"] == image.json()["id"])
        self.assertEqual(image_source["source_type"], "png")
        missing_description = self.client.post(
            f"/api/kc/handovers/{handover_id}/upload",
            files={"file": ("architecture.png", b"\x89PNG\r\n\x1a\nsynthetic", "image/png")},
        )
        self.assertEqual(missing_description.status_code, 422)
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
        self.assertEqual(self.client.get("/api/kc/templates").status_code, 401)
        self.assertEqual(self.client.get("/api/projects").status_code, 404)
        self.assertEqual(self.client.get("/api/projects/proj_mehta/dashboard").status_code, 404)
        with server.connect() as db:
            db.execute("INSERT INTO kc_users VALUES(?,?,?,?,?,?,?)",("usr_test_admin","test-admin@example.test","Test Admin","admin",server.password_hash("test password long enough"),1,server.now()))
        login=self.client.post("/api/kc/auth/login",json={"email":"test-admin@example.test","password":"test password long enough"})
        self.assertEqual(login.status_code,200,login.text)
        malformed = self.client.post("/api/kc/templates", content="{", headers={"content-type":"application/json"})
        self.assertEqual(malformed.status_code, 400)
        invalid_template = self.client.post("/api/kc/templates", json={"name":"Empty","fields":[]})
        self.assertEqual(invalid_template.status_code, 422)
        secret_note = self.client.post("/api/kc/handovers/demo-software-handover/sources", json={"name":"Secrets","content":"password=ThisIsASecretCredential123"})
        self.assertEqual(secret_note.status_code, 422)

    def test_public_demo_is_limited_to_synthetic_accounts_templates_and_handovers(self) -> None:
        # A real workspace may share this hosted database; the public demo identity
        # must not gain access to its users, custom templates, or handover records.
        with server.connect() as db:
            stamp=server.now()
            db.execute("INSERT INTO kc_users VALUES(?,?,?,?,?,?,?)",("usr_private","owner@example.test","Private Owner","admin","unused",1,stamp))
            db.execute("INSERT INTO kc_templates VALUES(?,?,?,?,?,?,?,?)",("tpl_private","Confidential Process", "Private", "Custom", 0, "[]", stamp, stamp))
            db.execute("INSERT INTO kc_handovers(id,title,template_id,departing_person,recipient,owner,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)",("ho_private","Private handover","software-project","Owner","Recipient","Owner","Draft",stamp,stamp))

        self.demo_login("admin")
        users=self.client.get("/api/kc/users")
        self.assertEqual(users.status_code,200,users.text)
        self.assertEqual({u["id"] for u in users.json()},{"demo_admin","demo_intern","demo_engineer"})
        templates=self.client.get("/api/kc/templates")
        self.assertEqual(templates.status_code,200,templates.text)
        self.assertNotIn("Confidential Process",{t["name"] for t in templates.json()})
        handovers=self.client.get("/api/kc/handovers")
        self.assertEqual(handovers.status_code,200,handovers.text)
        self.assertNotIn("ho_private",{h["id"] for h in handovers.json()})
        self.assertEqual(self.client.get("/api/kc/handovers/ho_private").status_code,403)
        self.assertEqual(self.client.post("/api/kc/handovers/ho_private/publish").status_code,403)
        self.assertEqual(self.client.post("/api/kc/users",json={"email":"new@example.test","display_name":"New","role":"employee","temporary_password":"long password 123"}).status_code,403)

    def test_judge_demo_has_mixed_synthetic_sources_and_recipient_view(self) -> None:
        self.demo_login("employee")
        detail=self.client.get("/api/kc/handovers/demo-software-handover")
        self.assertEqual(detail.status_code,200,detail.text)
        names={source["name"] for source in detail.json()["sources"]}
        self.assertTrue({"Synthetic README.md","Synthetic WhatsApp export.txt","Synthetic Gmail departure thread.txt","Synthetic issue export.csv","Synthetic test-run.log","Synthetic handover Q&A.md"}.issubset(names))
        # Repeated seed/startup must not multiply demo resources or passages.
        with server.connect() as db:
            before=db.execute("SELECT COUNT(*) n FROM kc_sources WHERE handover_id='demo-software-handover'").fetchone()["n"]
            server.ensure_demo_workspace(db)
            after=db.execute("SELECT COUNT(*) n FROM kc_sources WHERE handover_id='demo-software-handover'").fetchone()["n"]
        self.assertEqual(before,after)
        self.demo_login("recipient")
        public=self.client.get("/api/kc/handovers/demo-published-handover/recipient")
        self.assertEqual(public.status_code,200,public.text)
        self.assertTrue(public.json()["sources"])
        self.assertTrue(all(field["approved"] and field["citations"] for field in public.json()["fields"]))

    def test_upload_rejects_executables_bad_documents_and_credential_dumps(self) -> None:
        self.demo_login("employee")
        path="/api/kc/handovers/demo-software-handover/upload"
        cases=[
            (("payload.exe",b"MZ\x00\x00","application/octet-stream"),415),
            (("broken.pdf",b"not a pdf","application/pdf"),422),
            (("notes.txt",b"password=SuperSecretValue123456","text/plain"),422),
            (("eicar.txt",b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE","text/plain"),422),
            (("broken.docx",b"not a zip archive","application/vnd.openxmlformats-officedocument.wordprocessingml.document"),422),
        ]
        for (name,payload,mime),expected in cases:
            response=self.client.post(path,files={"file":(name,payload,mime)})
            self.assertEqual(response.status_code,expected,(name,response.text))
        self.assertEqual(self.client.post(path,files={"file":("large.txt",b"x"*(10*1024*1024+1),"text/plain")}).status_code,413)
        pack=server.BASE/"Knowledge_Continuity_Judge_Synthetic_Evidence_Pack.pdf"
        if pack.exists():
            accepted=self.client.post(path,files={"file":(pack.name,pack.read_bytes(),"application/pdf")})
            self.assertEqual(accepted.status_code,200,accepted.text)


if __name__ == "__main__":
    unittest.main()
