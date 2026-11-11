# Knowledge Continuity

A developer handoff workspace for intern-built software features. A senior engineer sets an editable template, the intern contributes code and project context, and the next engineer receives a reviewed continuation plan that distinguishes working, partial, mocked, planned, and unknown behavior.

## Run locally

1. Python 3.10+ is required.
2. Install dependencies: `python -m pip install -r requirements.txt`.
3. Start the app: `python -m uvicorn server:app --host 127.0.0.1 --port 8000` (or run `run.bat`).
4. Open http://127.0.0.1:8000 and choose **Try the interactive demo**. `run.bat` enables the synthetic judge demo and opens `/demo` without a login. For a private workspace, unset `KC_DEMO_MODE`, then create the first Admin account at `/login`.

The API uses SQLite at `data/sitewise.sqlite3` (the filename is legacy). API reference: http://127.0.0.1:8000/docs.

## Role workspaces

- Senior / Admin: `/app` — customize the Software project handover template, assign the intern and incoming engineer, review evidence, ask for missing context, approve recipient visibility, publish, and inspect version snapshots.
- Intern / builder: `/employee` — add authorized code and project sources, review extracted fields, answer targeted gap questions, edit the handover, and submit it. Interns cannot approve or publish.
- Incoming engineer: `/recipient` — read only the assigned published sections and cited references, acknowledge receipt, and ask questions against the approved handover.

The Admin creates accounts and shares temporary passwords privately. There is no email invitation service.

## Judge demo access

When `KC_DEMO_MODE=1`, `/demo` lets a judge enter the reviewer, intern, or incoming engineer workspace without credentials. Startup creates a fictional Human Value Calculator handover with dated evidence, open questions, and linked fields. Demo sessions are privileged role sessions; enable this only on an isolated judging deployment that contains synthetic demo data. Leave it disabled for real team work.

## Developer handover template

A Software project handover starter is added to existing workspaces as well as new ones. It covers user problem and scope, implementation status (working / partial / mocked / planned), architecture and code map, local setup, formulas and assumptions, data and integrations, decisions, tests, known gaps and risks, prioritized next work, reference links, and the incoming engineer's first steps. The owner can edit or remove fields before starting a handover.

Sources support TXT, Markdown, CSV, JSON, LOG, HTML, CSS, JavaScript, JSX, TypeScript, TSX, Python, SQL, YAML, PDF, and DOCX (up to 10 MB). Extracted searchable text is stored in SQLite; uploaded originals are stored under `data/uploads/` and can be downloaded by assigned owners and employees. Incoming engineers receive only approved cited excerpts, not the full original file. This is not a live GitHub/Slack connector or whole-repository importer. Do not upload `.env` files, tokens, passwords, or other secrets. Use only sources you are authorized to share.

Documents and code files are split into stable passage IDs. When an LLM key is configured, it drafts structured fields and citations; the server checks cited IDs and exact quote text. If the provider is unavailable, extraction and Q&A fall back to local source matching/excerpts. This verifies traceability, not whether the claim is true or current. Without an API key, the app uses local text matching and returns source excerpts rather than semantic AI drafts. OpenAI is supported with `OPENAI_API_KEY`; Groq is supported with `GROQ_API_KEY` using its OpenAI-compatible endpoint and defaults to `openai/gpt-oss-20b`. Set `OPENAI_BASE_URL` and `OPENAI_MODEL` to override provider defaults.

Before publication, Missing fields can create focused questions for the intern. The incoming engineer's Q&A is limited to the published approved source set and abstains when it cannot find support. A timeline view groups complete dates explicitly present in sources and links each entry back to its passage; upload, publication, and acknowledgement timestamps appear in a separate activity trail. Recipient timeline entries are limited to exact quotes in owner-approved visible fields. Senior review is required before sharing.

## Demo and deployment limits

Use synthetic, public, permissioned, or anonymized material in a demo. The current app is a local prototype, not a production deployment. Before internet hosting, configure HTTPS/secure cookies, email invitations and password reset, rate limits, backups, source retention, and organization-level access controls.
