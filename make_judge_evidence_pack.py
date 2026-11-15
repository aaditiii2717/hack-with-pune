"""Generate a judge-readable, entirely synthetic source pack in Markdown, DOCX, and PDF."""
from pathlib import Path
import re
import unicodedata

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

import server

ROOT = Path(__file__).resolve().parent
SOURCES = server.demo_source_specs()

INTRO = """# Knowledge Continuity | Judge Evidence Pack

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
"""

def build_markdown() -> str:
    out=[INTRO]
    for _, name, _, content in SOURCES:
        out += [f"## Source: {name}", content]
    out += ["## Source inventory", "Six synthetic inputs: README (Markdown), WhatsApp-style chat (text), Gmail-style departure thread (text), issue export (CSV), manual test log (log), and handover FAQ (Markdown). The same source content seeds the judge demo."]
    return "\n\n".join(out) + "\n"

def build_docx(markdown: str) -> None:
    doc=Document()
    sec=doc.sections[0]
    sec.top_margin=Inches(.65); sec.bottom_margin=Inches(.65)
    sec.left_margin=Inches(.75); sec.right_margin=Inches(.75)
    normal=doc.styles["Normal"]; normal.font.name="Aptos"; normal.font.size=Pt(9); normal.font.color.rgb=RGBColor(42,48,58)
    for style_name,size,color in [("Title",25,"17213A"),("Heading 1",17,"17213A"),("Heading 2",12,"0D8279")]:
        st=doc.styles[style_name]; st.font.name="Aptos Display"; st.font.size=Pt(size); st.font.bold=True; st.font.color.rgb=RGBColor.from_string(color)
    hp=sec.header.paragraphs[0]; hp.text="KNOWLEDGE CONTINUITY  /  SYNTHETIC JUDGE EVIDENCE"; hp.style="Caption"; hp.runs[0].font.color.rgb=RGBColor(13,130,121)
    fp=sec.footer.paragraphs[0]; fp.alignment=WD_ALIGN_PARAGRAPH.CENTER; fp.add_run("Synthetic demo only  |  16 November 2026").font.size=Pt(8)
    for raw in markdown.splitlines():
        if not raw.strip(): continue
        if raw.startswith("# "): doc.add_heading(raw[2:],0)
        elif raw.startswith("## "): doc.add_heading(raw[3:],1)
        elif raw.startswith("- "): doc.add_paragraph(raw[2:],style="List Bullet")
        elif re.match(r"\d+\. ",raw): doc.add_paragraph(re.sub(r"^\d+\. ","",raw),style="List Number")
        else:
            p=doc.add_paragraph()
            if raw.startswith("**") and raw.endswith("**"): p.add_run(raw.strip("*")).bold=True
            else: p.add_run(raw.replace("**",""))
    doc.save(ROOT/"Knowledge_Continuity_Judge_Synthetic_Evidence_Pack.docx")

def build_pdf(markdown: str) -> None:
    # Small dependency-free PDF writer; wrap to a conservative line width.
    pages=[]; current=[]; y=748
    for raw in markdown.splitlines():
        line=raw.strip()
        if not line:
            y-=7
            continue
        if line.startswith("# "): size=20; text=line[2:]; bold=True
        elif line.startswith("## "): size=13; text=line[3:]; bold=True
        else: size=9; text=line.replace("**",""); bold=False
        text=unicodedata.normalize("NFKD",text).encode("ascii","replace").decode("ascii")
        width=68 if size>13 else (95 if size==13 else 112)
        words=text.split(); lines=[]; buf=""
        for word in words:
            candidate=(buf+" "+word).strip()
            if len(candidate)>width and buf: lines.append(buf); buf=word
            else: buf=candidate
        if buf: lines.append(buf)
        leading=size+5
        if y-leading*len(lines)<55:
            pages.append(current); current=[]; y=748
        for textline in lines:
            current.append((textline,size,bold,y)); y-=leading
        y-=5
    if current: pages.append(current)
    objs=[]
    def obj(data): objs.append(data); return len(objs)
    regular=obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    boldfont=obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    page_ids=[]
    for page_no,lines in enumerate(pages,1):
        commands=["BT"]
        for text,size,is_bold,y in lines:
            escaped=text.replace("\\","\\\\").replace("(","\\(").replace(")","\\)")
            commands += ["0.09 0.13 0.23 rg",f"/{'F2' if is_bold else 'F1'} {size} Tf",f"1 0 0 1 48 {y} Tm ({escaped}) Tj"]
        commands += ["0.35 0.38 0.42 rg","/F1 8 Tf",f"1 0 0 1 48 30 Tm (Synthetic demo only  |  Page {page_no}) Tj","ET"]
        stream="\n".join(commands).encode("ascii")
        stream_id=obj(b"<< /Length "+str(len(stream)).encode()+b" >>\nstream\n"+stream+b"\nendstream")
        pid=obj(f"<< /Type /Page /Parent PAGES /MediaBox [0 0 612 792] /Resources << /Font << /F1 {regular} 0 R /F2 {boldfont} 0 R >> >> /Contents {stream_id} 0 R >>".encode())
        page_ids.append(pid)
    pages_id=obj(("<< /Type /Pages /Kids ["+" ".join(f"{p} 0 R" for p in page_ids)+f"] /Count {len(page_ids)} >>").encode())
    root=obj(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode())
    for pid in page_ids: objs[pid-1]=objs[pid-1].replace(b"/Parent PAGES",f"/Parent {pages_id} 0 R".encode())
    pdf=bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offsets=[0]
    for i,data in enumerate(objs,1): offsets.append(len(pdf)); pdf.extend(f"{i} 0 obj\n".encode()+data+b"\nendobj\n")
    xref=len(pdf); pdf.extend(f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode())
    for off in offsets[1:]: pdf.extend(f"{off:010d} 00000 n \n".encode())
    pdf.extend(f"trailer\n<< /Size {len(objs)+1} /Root {root} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    (ROOT/"Knowledge_Continuity_Judge_Synthetic_Evidence_Pack.pdf").write_bytes(pdf)

if __name__=="__main__":
    text=build_markdown()
    (ROOT/"judge_synthetic_evidence_pack.md").write_text(text,encoding="utf-8")
    build_docx(text); build_pdf(text)
    print("Generated synthetic source pack: Markdown, DOCX, PDF")
