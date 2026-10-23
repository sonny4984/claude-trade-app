"""Build A4 vocab test PDF (3 shuffled sets, 1 page each) from data/vocab_items.json.
Table only: No. / English (blank) / P.O.S. / Definition. No Korean, no title, no Example."""
import json, random, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak

root = Path(__file__).resolve().parent.parent
items = json.loads((root / "data/vocab_items.json").read_text(encoding="utf-8"))
sets = int(sys.argv[1]) if len(sys.argv) > 1 else 3
out = root / "data/toeic_vocab_test.pdf"

LM, TM = 13 * mm, 12 * mm
W = A4[0] - 2 * LM
cols = [11 * mm, 52 * mm, 20 * mm, W - 83 * mm]
n = len(items)
row_h = (A4[1] - 2 * TM - 8 * mm - 6 * mm) / n
cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8.5, leading=10.5)
head = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=9, leading=11)
pos = ParagraphStyle("p", fontName="Helvetica", fontSize=7.5, leading=9)

doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=LM, rightMargin=LM,
                        topMargin=TM, bottomMargin=TM)
story, key = [], []
for s in range(sets):
    order = items[:]
    random.Random(1000 + s).shuffle(order)
    rows = [[Paragraph(h, head) for h in ("No.", "English", "P.O.S.", "Definition")]]
    for i, it in enumerate(order, 1):
        rows.append([Paragraph(str(i), cell), "", Paragraph(it["pos"], pos), Paragraph(it["def"], cell)])
    t = Table(rows, colWidths=cols, rowHeights=[8 * mm] + [row_h] * n)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9d9d9")),
        ("BOX", (0, 0), (-1, -1), 1.2, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    story += [t] + ([PageBreak()] if s < sets - 1 else [])
    key.append((s + 1, [it["en"] for it in order]))
doc.build(story)

lines = ["# Vocab test answer key", ""]
for s, ans in key:
    lines += [f"## Set {s}", ""] + [f"{i}. {a}" for i, a in enumerate(ans, 1)] + [""]
(root / "data/toeic_vocab_test_answers.md").write_text("\n".join(lines), encoding="utf-8")
print(out, n, "words x", sets, "sets")
