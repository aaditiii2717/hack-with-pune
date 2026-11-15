# Knowledge Continuity | Judge Evidence Pack

**SYNTHETIC DEMONSTRATION DATA ONLY.** Every person, date, project note, conversation, issue, test result, URL, and email below is invented for this demo. There is no connected Gmail or WhatsApp account, no real repository, no customer or payroll data, and no credentials. Do not treat the example setup commands or implementation claims as verified facts about a real service.

## What this pack demonstrates

An intern-built software feature is handed to a senior reviewer and then to an incoming engineer. The source trail deliberately contains both useful context and gaps: a README, WhatsApp-style decision chat, Gmail-style departure thread, issue export, manual test log, and FAQ. Knowledge Continuity indexes these sources into stable passages, proposes template fields with citations, preserves uncertainty and disagreement, generates follow-up questions, and lets a reviewer approve only the information intended for the recipient.

## Fast judge walkthrough

1. Open the demo and choose the intern workspace. Open Human Value Calculator - first-build handoff and inspect My resources. Six differently formatted, synthetic sources should be available.
2. Open Template fields. Review the cited implementation, calculation, setup, tests, risk, and next-work details. Notice that uncertain release information remains a question and the rounding disagreement is called out rather than silently resolved.
3. Open Senior reviewer. Inspect evidence, edit or reject a field, then approve and publish only reviewed content.
4. Open the incoming engineer workspace. Read the published version, inspect citations, ask what to do next, and acknowledge receipt.

## Facts the sample evidence supports

- The fictional feature estimates weekly labor value as weekly hours saved multiplied by hourly value. This is an estimate, not validated ROI.
- The screen and estimate display work only with sample/local input according to the synthetic README; no database persistence or customer data is evidenced.
- The browser calculation is mapped to a fictional source path. An experimental API exists in the story but is not connected.
- The two documented checks are manual arithmetic examples. Automated, accessibility, negative-input, blank-input, deployment, and load testing are not documented.
- The rounding rule conflicts across the README and chat. The senior reviewer says not to decide silently.
- The next engineer should verify setup, obtain the rounding decision, add validation and automated tests, and avoid persistence until privacy decisions are made.
- The deployment URL and release commit/tag are not supplied. The demo intentionally asks the reviewer to confirm them.
- No actual Gmail, WhatsApp, GitHub, or customer systems are connected.

## Trust and data-security behavior

The product accepts a limited allowlist of text/code/document/image types, caps uploads at 10 MB, bounds PDF pages and DOCX archive expansion, rejects active-content PDFs, malformed files, executable/archived types, obvious credential dumps, and known antivirus test markers. Uploaded content is parsed as data and never executed; originals are private attachments, not rendered inline. Images require a contributor description; image pixels are not OCR/vision analyzed. Citation checks establish that a quote exists in a supplied passage, not that the statement is true. A human remains responsible for approval.

**Security limitation:** this deployment does not have a configured antivirus engine such as ClamAV. These checks reduce common upload risks but cannot guarantee malware detection. Do not upload confidential or real customer data to the public synthetic demo.


## Source: Synthetic README.md

SYNTHETIC SAMPLE — Human Value Calculator. All names, dates, repository references, and project history below are fictional.

Purpose: a small-team prototype estimates the weekly labor value of one workflow improvement. It is an estimate, not audited ROI, a customer promise, or a validated business metric.

Feature scope: one user enters weekly hours saved and an hourly value. The screen displays a weekly estimate. Multi-week forecasts, saved accounts, customer billing, and production analytics are out of scope.

Current implementation: the calculator form and estimate display work with sample/local inputs. The estimate is not saved to a database. No customer data or production credentials are included. Deployment status and last deployed commit are not recorded in the supplied project sources.

Architecture (fictional project map): `src/calculator/estimate.ts` holds the browser calculation; `src/calculator/EstimateForm.tsx` owns input state; `api/estimate.py` is a local-only experimental endpoint. The form currently calculates in the browser; the API route is not connected to the screen. No database integration is implemented.

Local setup (fictional project): Node.js 20; run `npm install`, then `npm run dev`. For the isolated API experiment, create a Python 3.12 environment, run `python -m pip install -r requirements.txt`, then `python -m uvicorn api.estimate:app --reload`. These commands have not been verified in this demo environment. No secret values belong in a handover; ask the owner for access through the approved secret manager.

Data and privacy: inputs are held in browser memory only. Do not enter personal, payroll, customer, or confidential data. The demo uses invented numbers and has no external integrations.

Decision recorded 2026-11-09: keep the first build to a weekly estimate so the team can validate the user need before adding persistence or forecasting. The owner must approve any change to this scope.

Known gaps: automated tests are absent; input validation and accessibility are incomplete; rounding behavior conflicts across sources; zero/negative inputs are not specified; the API route is unused; no database or production deployment is evidenced. Treat all of these as open work, not completed features.

Next build order: inspect the form and estimate function; agree rounding and invalid-input behavior with the reviewer; add unit tests; connect the API only after a reviewed contract; do not add persistence until privacy and retention are decided.

Synthetic repository reference: `https://example.invalid/human-value-calculator` (reserved example domain; not a real repository).

## Source: Synthetic WhatsApp export.txt

SYNTHETIC CHAT EXPORT — fictional participants; no real phone numbers or customer messages.

2026-11-10 10:12 — Intern: The calculator returns weekly hours saved multiplied by hourly value. I used 2 decimals in the screen, but an earlier sketch says round to a whole number. I could not find an owner decision.

2026-11-10 10:18 — Senior reviewer: Keep the conflict visible. Do not choose a rounding rule silently. Ask me before changing the display or calling the number ROI.

2026-11-10 10:24 — Intern: I checked zero hours and a normal positive example manually. Negative hours and blank input still need validation. I did not write automated tests.

2026-11-11 15:40 — Intern: The screen is local-only. The API experiment is not wired to it, and no database or customer data is connected.

2026-11-11 15:46 — Senior reviewer: Before the next engineer releases anything, confirm the exact deployment/tag with me; the exported project notes do not identify a verified staging release.

## Source: Synthetic Gmail departure thread.txt

SYNTHETIC EMAIL EXPORT — illustrative Gmail-style thread only. No real mailbox was connected and no email was sent.

From: Demo Intern
To: Demo Senior Reviewer
Date: 2026-11-12
Subject: Human Value Calculator — before I hand it over

I added the local setup commands and code map to the README. Please confirm whether the UI should show two decimals or round to a whole number; my sources disagree. I tested one zero input and one positive input by hand, but did not test negative or blank values. There is no saved-data flow yet. I have not captured a verified deployment URL or commit, so please confirm that with the team before calling a build released.

I did not include any API keys, passwords, customer records, or real contact details. If the next engineer needs service access, please share it through the team's secret manager, not email or this handover.

Reviewer reply (synthetic): Thanks. Keep rounding marked unresolved until product approves it. Add validation and automated tests before connecting persistent data. The release tag is still unverified; ask the release owner. Never copy secret values into a handover.

## Source: Synthetic issue export.csv

id,title,status,owner,priority,acceptance_criteria,dependency
HVC-14,Decide estimate rounding,Open,Senior reviewer,High,Product owner records one rounding rule and updates UI plus tests,Product decision
HVC-15,Validate blank and negative inputs,Todo,Incoming engineer,High,Blank and negative values show clear inline errors; valid zero remains supported,None
HVC-16,Add automated calculation tests,Todo,Incoming engineer,High,Tests cover zero positive negative blank and chosen rounding,Agree rounding rule
HVC-17,Verify local setup and API contract,Todo,Incoming engineer,Medium,Fresh clone follows README and unused API route is either integrated or removed,Access to repository
HVC-18,Confirm verified release identifier,Blocked,Senior reviewer,High,Reviewer confirms deployment URL and commit/tag from release owner,Release owner confirmation
HVC-19,Decide whether results may be persisted,Open,Product owner,Medium,Document user need consent retention and deletion before adding a database,Privacy review

## Source: Synthetic test-run.log

SYNTHETIC MANUAL CHECK LOG — not output from an automated CI run.

Run date: 2026-11-10. Environment: local prototype, sample inputs only.

Case: weekly hours saved = 2; hourly value = 500. Expected arithmetic before display rounding: 1000. Observed: 1000.00.

Case: weekly hours saved = 0; hourly value = 500. Expected arithmetic: 0. Observed: 0.00.

Not tested: blank input, negative values, decimal precision, keyboard-only use, screen-reader behavior, API endpoint, database persistence, deployment, load, or real customer data.

Result: 2 manual examples passed; this is not evidence of automated tests or production readiness.

## Source: Synthetic handover Q&A.md

SYNTHETIC DEMO ANSWERS — answers are limited to the supplied fictional sources.

Q: What does the feature do? A: It estimates weekly labor value from weekly hours saved multiplied by an hourly value.

Q: Is the estimate validated ROI? A: No. The README calls it an unvalidated estimate, not audited ROI or a customer promise.

Q: Where does the calculation happen? A: The fictional code map says `src/calculator/estimate.ts`; the form currently calculates in the browser. The experimental API is not connected.

Q: Is data saved? A: No. Inputs stay in browser memory; no database persistence is implemented.

Q: What is complete? A: The calculator form and estimate display work with sample/local inputs. Automated tests, complete validation, API integration, and production deployment are not evidenced.

Q: What was tested? A: Two manual examples only: 2 hours at 500 gives 1000 before rounding; zero hours gives zero. No automated test run is documented.

Q: What rounding rule is approved? A: The README and chat conflict. The reviewer explicitly says not to choose silently; a product decision is still required.

Q: What should the next engineer do first? A: Verify a fresh local setup, ask the reviewer about rounding, then add blank/negative input validation and automated tests.

Q: Is there a verified staging release? A: No supplied source names a verified deployment or commit. Confirm with the release owner before calling any build released.

Q: Where are credentials? A: No credentials are in the sample. Ask the owner for access through the approved secret manager; never put secrets in the handover.

Q: Can the estimate be used with customer or payroll data? A: No. The sample explicitly says not to enter personal, payroll, customer, or confidential data.

Q: Why is there no persistence? A: The team deferred it until the user need, consent, retention, and deletion behavior receive a privacy review.

## Source inventory

Six synthetic inputs: README (Markdown), WhatsApp-style chat (text), Gmail-style departure thread (text), issue export (CSV), manual test log (log), and handover FAQ (Markdown). The same source content seeds the judge demo.
