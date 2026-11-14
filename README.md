# Knowledge Continuity

Knowledge Continuity turns a departing teammate’s scattered project context into an evidence-linked handover that a reviewer can approve and the next engineer can use. The Round 3 implementation is focused on intern-built software features: what works, how to run it, why it was built this way, what is still open, and how the next engineer can continue safely.

## The handover journey

1. A **Senior reviewer / owner** selects the engineering starter template or a custom template, creates a handover, and assigns the builder and incoming engineer.
2. The **Intern / builder** adds authorized notes, documents, code or exports. The system extracts passages, proposes field content, and links claims to source passages. The builder can correct the draft and answer focused questions for missing context.
3. The **Senior reviewer / owner** checks evidence, edits content, controls recipient visibility field by field, approves fields, and publishes a version.
4. The **Incoming engineer** sees only the assigned published handover and approved visible fields, can follow citations, ask a question, and acknowledge receipt.

These are separate role-based workspaces over one API. The server enforces assignment, review and publication permissions; hiding a button in the browser is not the security boundary.

## Engineering starter template

The editable-copy starter prompts for 14 areas: user outcome and acceptance criteria; feature boundaries; delivery status with proof; architecture and code map; reproducible setup; data model and API contracts; core logic and assumptions; decisions and chronology; test evidence; defects, security and privacy risks; ownership and dependencies; prioritized next work; canonical repository references; and a first-day plan for the incoming engineer. Owners can copy the starter and adapt fields to their project. Generated or inferred content remains subject to human review.

## What is implemented

- Landing page, demo entry point, and distinct owner, builder, and incoming-engineer workspaces.
- Account and role setup, assigned handovers, default/custom editable templates, and field-level editing.
- TXT, Markdown, CSV, JSON, LOG, HTML, CSS, JavaScript/TypeScript, Python, SQL, YAML, PDF, and DOCX source intake (up to 10 MB per file).
- Passage-based source indexing, structured AI-assisted extraction when a provider key is configured, server-side citation ID and exact-quote validation, and a local source-matching fallback.
- Found/inferred/missing or manual field states, focused questions for missing context, reviewer approval, recipient visibility controls, versioned publication, and acknowledgement.
- Recipient Q&A constrained to the approved handover source set, source-linked project timeline, and an activity trail.
- Synthetic Human Value Calculator data for the judge demo; it is fictional and not customer data.

The app does not connect to GitHub, Slack, or other project systems automatically. A user must provide authorized exports or files. Citation checks establish traceability to supplied text, not that a statement is true, current, or complete.

## Technology and data flow

- **UI:** responsive HTML, CSS and browser JavaScript served by FastAPI.
- **API:** Python 3.12, FastAPI and Uvicorn.
- **Storage:** SQLite for local development; PostgreSQL for hosted deployment. Supabase's transaction pooler is appropriate for Vercel's short-lived serverless requests. Source text, passages, field states, approvals, versions, accounts, sessions, Q&A, and uploaded originals are persisted in the database; the deployed workflow does not depend on writable local disk.
- **AI:** optional Groq or OpenAI-compatible chat completions. The server validates output structure and citations. Without a configured provider, source matching and excerpt-based answers remain available.
- **Documents:** `pypdf` and `python-docx` parse PDF and DOCX; plain and code formats use text extraction.
- **Deployment:** Vercel Python function configured in `vercel.json`.

The central flow is: authorized source → normalized text → stable passage IDs → proposed field and evidence → server citation validation → human correction/approval → role-filtered published snapshot.

## Run locally

Requirements: Python 3.12 (3.10+ may work locally, but deployment targets 3.12).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`. To use the synthetic judge experience, set `KC_DEMO_MODE=1` in the local `.env` and visit `/demo`; `run.bat` also starts this synthetic demo. For a private workspace, disable demo mode and visit `/login` to set up the first owner account. The local database is `data/sitewise.sqlite3` (legacy filename). Leave `DATABASE_URL` blank for SQLite.

Optional AI configuration: set one of `GROQ_API_KEY` or `OPENAI_API_KEY` in `.env`. Never put keys in browser code, source files, or the repository. To use hosted Postgres locally, set `DATABASE_URL` to the Supabase transaction-pooler URI and URL-encode any special characters in its password.

## Deploy on Vercel

The project owner reported that the Vercel deployment error was cleared. The team should open the deployed URL and verify the core journey before submitting it.

1. Push the public source repository and import it into Vercel. Keep the repository root as the root directory and use the FastAPI preset / `vercel.json` configuration.
2. Configure a Supabase PostgreSQL project and copy its **Transaction pooler** connection URI. Add it in Vercel → Project → Settings → Environment Variables as `DATABASE_URL`.
3. Add `KC_DEMO_MODE=1` and `COOKIE_SECURE=1` for the synthetic judging deployment. Add `GROQ_API_KEY` only if live AI extraction is enabled. Do not add `NEXT_PUBLIC_*` database credentials or a service-role key to this server app.
4. Apply variables to Production (and Preview if used), redeploy, then open `/api/health` and `/demo` on the deployed domain.
5. Verify in a private browser window: owner/reviewer, builder, and recipient flow; refresh; source citations; publication; and recipient visibility.

The transaction-pooler password belongs only in Vercel's encrypted environment settings or a private local `.env`; never commit it. `.env` is ignored by Git. Rotating a credential that has been pasted into chat or another public place is recommended.

## Tests

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

The acceptance tests run in a temporary SQLite database and cover health/landing, the 14-field template, reviewer-created assignment, builder submission, recipient denial before publication, reviewer approval and publication, duplicate publication rejection, role-filtered recipient access, Q&A, acknowledgement, malformed JSON, invalid empty templates, and unauthenticated access. The last local run completed 2 tests successfully. This does not replace verification against the live Vercel and Supabase deployment.

## Limitations and next steps

- The judge demo intentionally bypasses login and grants synthetic role sessions. Keep it isolated to fictional demo data; do not use this mode for real confidential work.
- Account setup is owner-managed; there is no email invitation or password-reset delivery service.
- The role model is for a single workspace/project environment; organization-level tenant isolation, external security review, backup/restore drills, monitoring/alerting, and formal retention controls require further production operations work.
- AI availability and output depend on the configured provider. The safe fallback is source excerpts; the reviewer remains accountable for publication.

## Round 3 commitments

1. **Better template — delivered:** expanded the software handover starter to 14 practical engineering sections with explicit proof, status, operational setup, risk, ownership, and continuation prompts.
2. **Better hierarchy — delivered:** made the Senior reviewer / owner → Intern / builder → Incoming engineer workflow and permissions explicit across onboarding, workspaces, assignment, review, and recipient sharing.
3. **Production-ready system — Round 3 hardening delivered:** persistent hosted database support, server-enforced role/access checks, safe citation filtering, secure session-cookie behavior, malformed-input responses, template validation, concurrent first-owner setup protection, duplicate-publish rejection, and end-to-end workflow tests. A hackathon build is not a substitute for an independently audited production service; remaining operational limits are listed above.

## Submission details

- Source: https://github.com/aaditiii2717/hack-with-pune
- Live deployment: `https://knowledge-continuity-4m1bfr7il-yaye2.vercel.app` (verify before submission)
- Final product brief: `Knowledge_Continuity_Round3_Final_Submission.pdf`
