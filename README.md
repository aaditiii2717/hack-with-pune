# Knowledge Continuity

Knowledge Continuity turns a departing teammate’s scattered project context into an evidence-linked handover that a reviewer can approve and the next engineer can use. The Round 3 implementation is focused on intern-built software features: what works, how to run it, why it was built this way, what is still open, and how the next engineer can continue safely.

## The handover journey

1. A **Senior reviewer / owner** selects the engineering starter template or a custom template, creates a handover, and assigns the builder and incoming engineer.
2. The **Intern / builder** adds authorized notes, documents, code or exports. The system extracts passages, proposes field content, and links claims to source passages. The builder can correct the draft and answer focused questions for missing context.
3. The **Senior reviewer / owner** checks evidence, edits content, controls recipient visibility field by field, approves fields, and publishes a version.
4. The **Incoming engineer** sees only the assigned published handover and approved visible fields, can follow citations, ask a question, and acknowledge receipt.

These are separate role-based workspaces over one API. Each handover shows a live responsibility rail for setup, builder work, senior review, and recipient acknowledgement; its current, waiting, and complete states come from the saved handover status. The server enforces assignment, review and publication permissions; hiding a button in the browser is not the security boundary.

## Engineering starter template

The editable-copy starter prompts for 14 areas: user outcome and acceptance criteria; feature boundaries; delivery status with proof; architecture and code map; reproducible setup; data model and API contracts; core logic and assumptions; decisions and chronology; test evidence; defects, security and privacy risks; ownership and dependencies; prioritized next work; canonical repository references; and a first-day plan for the incoming engineer. Owners can copy the starter and adapt fields to their project. Generated or inferred content remains subject to human review.

## What is implemented

- Landing page, demo entry point, and distinct owner, builder, and incoming-engineer workspaces.
- Account and role setup, assigned handovers, default/custom editable templates, and field-level editing.
- TXT, Markdown, CSV, JSON, LOG, HTML, CSS, JavaScript/TypeScript, Python, SQL, YAML, PDF, DOCX, PNG, JPEG, GIF, and WebP source intake (up to 10 MB per file).
- Image originals are stored privately; the uploader must provide a short description that becomes searchable and citable. Image pixels are not OCR- or vision-analyzed. The incoming engineer sees approved descriptions in the handover, not the private original image file.
- Passage-based source indexing, structured AI-assisted extraction when a provider key is configured, server-side citation ID and exact-quote validation, and a local source-matching fallback.
- Found/inferred/missing or manual field states, focused questions for missing context, reviewer approval, recipient visibility controls, versioned publication, and acknowledgement.
- Recipient Q&A constrained to the approved handover source set, source-linked project timeline, and an activity trail.
- Synthetic Human Value Calculator data for the judge demo; it is fictional and not customer data.
- Judge source pack in Markdown, DOCX, and PDF: synthetic README, WhatsApp-style chat, Gmail-style departure thread, issue CSV, manual test log, and judge FAQ. The same source set is seeded in the demo and available in the intern and published recipient workspaces.

The app does not connect to GitHub, Slack, or other project systems automatically. A user must provide authorized exports or files. Citation checks establish traceability to supplied text, not that a statement is true, current, or complete.

## Synthetic judge pack and safe source intake

Open Knowledge_Continuity_Judge_Synthetic_Evidence_Pack.pdf for the judge-readable source bundle, or use the DOCX/Markdown copy to inspect the synthetic examples. The Gmail- and WhatsApp-style exports are fictional; the product does not connect to either service.

Uploads are limited to an allowlist, one file per request, 10 MB, and bounded extraction. PDFs receive header, active-content, page, and text-size checks. DOCX ZIP expansion, entry count, compression ratio, embedded payload paths, and archive integrity are checked. Executables and archives are rejected. Obvious credentials and the EICAR antivirus test string are rejected from both uploaded files and pasted notes/answers. Originals download as attachments and are never executed. Images are stored as originals; contributors must add a searchable description, and image pixels are not OCR/vision processed.

**Malware and demo limits:** there is no antivirus engine. These checks reduce common risks; they do not prove a file is safe. The public demo intentionally has no login and uses shared synthetic role accounts. Server access checks limit those demo identities to explicitly assigned synthetic handovers and built-in templates; account/template administration and legacy Sitewise APIs are unavailable to demo users. Demo activity can change shared sample data, so never enter customer data, secrets, or other confidential information in the public demo.

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
3. Add `KC_DEMO_MODE=1` and `COOKIE_SECURE=1` for the synthetic judging deployment. Set a unique random `KC_RATE_LIMIT_KEY` for stable hashed login-limit identifiers; if omitted, the server derives it from `DATABASE_URL`. Add `GROQ_API_KEY` only if live AI extraction is enabled. Do not add `NEXT_PUBLIC_*` database credentials or a service-role key to this server app.
4. Apply variables to Production (and Preview if used), redeploy, then open `/api/health` and `/demo` on the deployed domain.
5. Verify in a private browser window: owner/reviewer, builder, and recipient flow; refresh; source citations; publication; and recipient visibility.

The transaction-pooler password belongs only in Vercel's encrypted environment settings or a private local `.env`; never commit it. `.env` is ignored by Git. Rotating a credential that has been pasted into chat or another public place is recommended.

## Tests

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

The current suite has 9 tests: 6 end-to-end/API acceptance tests and 3 offline backup-tool safety tests. It covers the reviewer-builder-recipient workflow, authorization and recipient visibility, demo isolation from real users/custom templates/unassigned handovers, retired Sitewise endpoint denial, malformed input, source secrecy checks, demo seeding, upload rejection, persistent login throttling, refusal to use the transaction pooler for dumps, and refusal to restore to the configured production Supabase project. The suite passed locally on 16 November 2026. It does not verify a live Vercel deployment, contact a real Supabase database, or replace an independent security review.

## Login throttling and database backups

Password login stores failed-attempt counters in PostgreSQL/SQLite, keyed by HMAC digests rather than raw email/IP values. The current limits are 8 failed attempts per account and 40 per client IP in a 15-minute window; the public demo role-session endpoint is separately limited to 60 sessions per IP per window. A correct login clears the account counter. Set a unique random `KC_RATE_LIMIT_KEY` in Vercel for stable HMAC identifiers, or leave it blank to derive the key from `DATABASE_URL`. The public judge demo is still a role-selector demo and does not use passwords.

`python backup_database.py` creates a compressed PostgreSQL dump in the ignored `backups/` folder. Install PostgreSQL client tools first and set `SUPABASE_BACKUP_URL` in your private `.env` to a Direct or Session connection URI; do not use the Vercel transaction-pooler URI. Backups contain project data, are not encrypted by the script, and must be kept in encrypted, access-controlled storage. `BACKUP_RESTORE.md` explains how to restore only into a separate empty staging project with `python restore_database.py <dump-file>` and verify the app journey. **The scripts and runbook are prepared, but no live backup/restore drill has been run yet.** Supabase documents daily managed backups for Pro and higher plans; Free plans should export regularly and keep an off-site copy. See [Supabase backup guidance](https://supabase.com/docs/guides/platform/backups) and [connection guidance for dump/restore](https://supabase.com/docs/guides/database/connecting-to-postgres).

## Limitations and next steps

- Public demo sessions are shared, unauthenticated, and intended only for fictional judge data. Data entered by one demo visitor may be visible to other demo visitors. The demo role is scoped to explicitly assigned synthetic handovers, but this is not a tenant-isolation design for confidential customer work.
- Account setup is owner-managed; there is no email invitation or password-reset delivery. Login throttling is a baseline control, not a substitute for a managed identity provider or independent abuse monitoring. The demo's shared sample state may be changed during judging.
- The app has no antivirus engine, independent penetration test, formal data-retention controls, organization-level tenant system, backup/restore drills, or production monitoring/alerting.
- The product does not automatically connect to GitHub, Slack, WhatsApp, or Gmail; authorized exports/files must be supplied by the user. Optional LLM calls send selected source text to the configured provider. The source-only fallback remains available without a provider key.
- Citation checks establish traceability to supplied text, not that a claim is true, current, or complete. A human reviewer remains responsible for approval and sharing.

## Round 3 commitments

1. **Better template — delivered:** expanded the software handover starter to 14 practical engineering sections with explicit proof, status, operational setup, risk, ownership, and continuation prompts.
2. **Better hierarchy — delivered:** made the Senior reviewer / owner → Intern / builder → Incoming engineer workflow and permissions explicit across onboarding, workspaces, assignment, review, and recipient sharing.
3. **Production-readiness hardening — Round 3 work delivered; operational readiness remains:** persistent hosted database support, server-enforced role/access checks, demo data scoping, legacy API shutdown, source credential checks, upload bounds, login throttling, backup/restore scripts and runbook, safe citation filtering, secure session-cookie behavior, malformed-input responses, template validation, duplicate-publish rejection, and end-to-end workflow tests. The live restore drill, antivirus, independent security review, formal tenant isolation, and monitoring are outstanding; this is a hackathon MVP, not a claim of production certification.

## Submission details

- Source: https://github.com/aaditiii2717/hack-with-pune
- Live deployment: `https://knowledge-continuity-mu.vercel.app` (verify before submission)
- Final product brief: `Knowledge_Continuity_Round3_Final_Submission.pdf`
- Judge evidence pack: `Knowledge_Continuity_Judge_Synthetic_Evidence_Pack.pdf`
