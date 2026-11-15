"""Generate the Round 3 handover product brief PDF from the repository's shipped scope."""
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
doc = Document()
section = doc.sections[0]
section.top_margin = Inches(.65)
section.bottom_margin = Inches(.65)
section.left_margin = Inches(.78)
section.right_margin = Inches(.78)

styles = doc.styles
styles['Normal'].font.name = 'Aptos'
styles['Normal'].font.size = Pt(9.5)
styles['Normal'].font.color.rgb = RGBColor(42, 48, 58)
for name, size, color in [('Title', 27, '17213A'), ('Heading 1', 17, '17213A'), ('Heading 2', 12, '0D8279')]:
    style = styles[name]
    style.font.name = 'Aptos Display'
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor.from_string(color)

header = section.header.paragraphs[0]
header.text = 'KNOWLEDGE CONTINUITY  /  ROUND 3 PRODUCT BRIEF'
header.style = 'Caption'
header.runs[0].font.color.rgb = RGBColor(13, 130, 121)
header.runs[0].font.bold = True
footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer.add_run('We Code Coders  ·  Round 3  ·  15 November 2026').font.size = Pt(8)

doc.add_paragraph('ROUND 3  /  FINAL PRODUCT', style='Subtitle')
doc.add_heading('Knowledge Continuity', 0)
p = doc.add_paragraph()
p.add_run('A reviewed, evidence-linked handover for software work that outlives its first builder.').bold = True
doc.add_paragraph('When an intern hands an unfinished feature to a senior engineer, critical context is scattered across notes, code, exports, and conversations. Knowledge Continuity turns authorized sources into an editable, cited handover: a reviewer checks it, controls what the next engineer sees, and publishes the continuation plan.')

doc.add_heading('Who uses it', level=1)
for title, body in [
    ('Senior reviewer / owner', 'Sets the template and assignments, reviews evidence, edits and approves fields, controls visibility, and publishes a version.'),
    ('Intern / builder', 'Adds authorized sources, checks extracted content, answers targeted questions, and submits the handover. Cannot publish.'),
    ('Incoming engineer', 'Reads the assigned published handover and approved visible fields, follows citations, asks questions, and acknowledges receipt.'),
]:
    p = doc.add_paragraph(style='List Bullet')
    p.add_run(title + ' — ').bold = True
    p.add_run(body)

doc.add_heading('Main journey', level=1)
doc.add_paragraph('Assign work → add project sources → extract and verify passages → complete the template and resolve gaps → senior review and field-level approval → publish a version → incoming engineer reads, asks, and acknowledges.', style='Intense Quote')

doc.add_heading('The three Round 2 commitments', level=1)
for title, body in [
    ('1  Better template — delivered', 'The software handover starter now has 14 sections: user outcome and acceptance criteria; scope; delivery status and proof; architecture and code map; reproducible setup; data/API contracts; logic and assumptions; decisions and chronology; test evidence; known defects/security/privacy risks; dependencies and ownership; prioritized next work; canonical references; and a first-day continuation plan. Owners copy and adapt the starter.'),
    ('2  Better hierarchy — delivered', 'The app makes the senior reviewer/owner → intern/builder → incoming engineer responsibilities explicit. Assignment, submission, approval, publication, and recipient access are enforced by the API, including per-field recipient visibility.'),
    ('3  Production-ready system — Round 3 hardening delivered', 'Hosted PostgreSQL support for serverless deployment; secure session-cookie settings; server-side role and assignment checks; citation ID/quote validation; safe recipient filtering; malformed JSON and invalid-template handling; concurrent first-owner setup protection; duplicate-publication rejection; and end-to-end role-journey acceptance tests. Remaining operational work is disclosed below; this hackathon build has not had an independent security audit.'),
]:
    p = doc.add_paragraph(style='List Number')
    p.add_run(title + ': ').bold = True
    p.add_run(body)

doc.add_heading('Completed capabilities', level=1)
for item in [
    'Distinct landing, reviewer, builder, and incoming-engineer experiences; synthetic Human Value Calculator demo.',
    'Default and owner-customized templates; assigned handovers; field editing, status, and focused missing-context questions.',
    'TXT, Markdown, CSV, JSON, LOG, web/code text formats, PDF, DOCX, PNG, JPEG, GIF, and WebP intake (10 MB per file). Images are stored privately; a contributor description is indexed and cited. No OCR/vision is claimed.',
    'Stable source passage IDs, structured AI-assisted extraction when configured, citation checks, and local source-matching fallback.',
    'Human approval, field-level visibility, versioned publication, recipient Q&A over approved sources, timeline, and acknowledgement.',
    'Judge evidence pack in Markdown, DOCX and PDF: synthetic README, WhatsApp-style chat, Gmail-style departure thread, issue CSV, manual test log and Q&A. The synthetic evidence also seeds the intern and published recipient demos.',
    'PostgreSQL persistence for source text and originals; SQLite local development.',
    'Bounded upload parsing: 10 MB cap, allowlisted extensions, PDF active-content/page/text checks, DOCX archive expansion/integrity checks, and rejection of obvious credential dumps and the EICAR test signature. Uploaded files are data, never executed, and originals download as attachments.',
]: doc.add_paragraph(item, style='List Bullet')

doc.add_heading('Architecture and implementation', level=1)
doc.add_paragraph('Responsive HTML/CSS/browser JavaScript is served by a Python 3.12 FastAPI application. SQLite supports local use; Supabase PostgreSQL via its transaction pooler persists hosted data. PDF and DOCX parsing use pypdf and python-docx. Groq or OpenAI-compatible models can draft structured values; the server verifies cited passage IDs and exact quote text. Without a provider key, local matching and evidence excerpts remain available. A human reviewer remains responsible for truth and publication.')
doc.add_paragraph('Authorized source → normalized text → stable passages → proposed field and citations → server validation → human edit/approval → role-filtered versioned handover.', style='Intense Quote')

doc.add_heading('Verification', level=1)
doc.add_paragraph('Local acceptance command: python -m unittest discover -s tests -v. The latest run passed 4 tests. Coverage includes health and landing, the 14-field starter, reviewer assignment, builder submission, recipient denial before publication, field approval, publication, duplicate publish rejection, recipient filtering, Q&A, acknowledgement, unauthenticated access, malformed JSON, invalid empty templates, idempotent mixed-source demo seeding, and rejection of executable, malformed, credential-containing, EICAR test, and oversized uploads. The test suite uses isolated temporary SQLite and synthetic data.')
doc.add_paragraph('Security limit: the hosted demo has no configured antivirus engine. The upload checks reduce common risks but do not guarantee malware detection. Keep the public demo synthetic-only; citation checks prove quote traceability, not truth.')

doc.add_heading('Setup and submission links', level=1)
doc.add_paragraph('Repository: https://github.com/aaditiii2717/hack-with-pune')
doc.add_paragraph('Current production domain shown in Vercel: https://knowledge-continuity-mu.vercel.app (open and verify the live workflow before submitting).')
doc.add_paragraph('Judge evidence pack: Knowledge_Continuity_Judge_Synthetic_Evidence_Pack.pdf; editable copy: Knowledge_Continuity_Judge_Synthetic_Evidence_Pack.docx.')
doc.add_paragraph('Local: create a Python virtual environment, install requirements.txt, copy .env.example to .env, then run python -m uvicorn server:app --host 127.0.0.1 --port 8000. Keep .env and database credentials out of Git. Hosted Vercel requires DATABASE_URL (Supabase transaction pooler), KC_DEMO_MODE=1 for fictional judging data, and COOKIE_SECURE=1; an AI provider key is optional.')

doc.add_heading('Known limits and roadmap', level=1)
doc.add_paragraph('The demo bypasses login and must contain synthetic data only. Account provisioning is owner-managed; there is no email invite/password-reset service or automatic GitHub/Slack connector. Organization-level tenant isolation, independent security audit, backup/restore drills, production monitoring, and formal retention controls remain future operational work. The next development phase should prioritize secure invitations and account recovery, integration-backed source sync, stronger organization and retention controls, and operational monitoring/restore validation.')

docx_path = ROOT / 'Knowledge_Continuity_Round3_Final_Submission.docx'
doc.save(docx_path)

# Emit a clean, dependency-free PDF from the same DOCX paragraphs. Text is wrapped
# before encoding to keep the artifact portable and readable without Office installed.
import re

pages: list[list[tuple[str, int, bool]]] = [[]]
y = 748
for paragraph in doc.paragraphs:
    text = re.sub(r'\s+', ' ', paragraph.text).strip()
    if not text:
        y -= 7
        continue
    style = paragraph.style.name
    size = 23 if style == 'Title' else (16 if style == 'Heading 1' else (11 if style == 'Heading 2' else 9))
    leading = size + (6 if size >= 16 else 4)
    usable = max(40, int(540 / (size * .49)))
    words = text.encode('ascii', 'replace').decode('ascii').split()
    lines: list[str] = []
    current = ''
    for word in words:
        candidate = (current + ' ' + word).strip()
        if len(candidate) > usable and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    if y - leading * len(lines) < 54:
        pages.append([])
        y = 748
    for line in lines:
        pages[-1].append((line, size, style.startswith('Heading') or style == 'Title'))
        y -= leading
    y -= 7 if size < 16 else 10

objects: list[bytes] = []
def add_obj(data: bytes) -> int:
    objects.append(data)
    return len(objects)

font_regular = add_obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
font_bold = add_obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>')
page_ids: list[int] = []
for page_lines in pages:
    cmds = ['BT']
    y = 748
    for line, size, bold in page_lines:
        font = 'F2' if bold else 'F1'
        color = '0.05 0.45 0.42 rg' if bold and size == 16 else '0.09 0.13 0.23 rg' if bold else '0.16 0.19 0.23 rg'
        escaped = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        cmds += [color, f'/{font} {size} Tf', f'1 0 0 1 52 {y} Tm ({escaped}) Tj']
        y -= size + (6 if size >= 16 else 4)
    cmds.append('ET')
    stream = ('\n'.join(cmds)).encode('ascii')
    stream_id = add_obj(b'<< /Length ' + str(len(stream)).encode() + b' >>\nstream\n' + stream + b'\nendstream')
    page_id = add_obj(f'<< /Type /Page /Parent PAGES /MediaBox [0 0 612 792] /Resources << /Font << /F1 {font_regular} 0 R /F2 {font_bold} 0 R >> >> /Contents {stream_id} 0 R >>'.encode())
    page_ids.append(page_id)
pages_id = add_obj(('<< /Type /Pages /Kids [' + ' '.join(f'{pid} 0 R' for pid in page_ids) + f'] /Count {len(page_ids)} >>').encode())
catalog_id = add_obj(f'<< /Type /Catalog /Pages {pages_id} 0 R >>'.encode())
for pid in page_ids:
    objects[pid - 1] = objects[pid - 1].replace(b'/Parent PAGES', f'/Parent {pages_id} 0 R'.encode())
pdf = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
offsets = [0]
for index, obj in enumerate(objects, 1):
    offsets.append(len(pdf))
    pdf.extend(f'{index} 0 obj\n'.encode() + obj + b'\nendobj\n')
xref = len(pdf)
pdf.extend(f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode())
for offset in offsets[1:]:
    pdf.extend(f'{offset:010d} 00000 n \n'.encode())
pdf.extend(f'trailer\n<< /Size {len(objects)+1} /Root {catalog_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
(ROOT / 'Knowledge_Continuity_Round3_Final_Submission.pdf').write_bytes(pdf)
print('Generated DOCX and PDF submission briefs.')
