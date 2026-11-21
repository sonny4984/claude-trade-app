"""Build A4 vocab test PDF (shuffled sets, 1 page each) from a word-list JSON.
Usage: python3 tools/make_vocab_test.py data/vocab_s1.json [sets]
Shows English; student writes the Korean meaning. Example sentence has the word removed (blank)
so it can be written in by hand (GoodNotes). Korean appears only in the answer key."""
import json, random, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak

src = Path(sys.argv[1]).resolve()
sets = int(sys.argv[2]) if len(sys.argv) > 2 else 3
items = json.loads(src.read_text(encoding="utf-8"))
BLANK = "_" * 16
for it in items:  # the word and its forms must not survive in the example
    assert "{}" in it["ex"], it["en"]
    left = it["ex"].replace("{}", "").lower()
    assert it["stem"] not in left, f'{it["en"]}: stem left in example'
out = src.with_name(src.stem + "_test.pdf")

LM, TM = 13 * mm, 12 * mm
W = A4[0] - 2 * LM
cols = [9 * mm, 36 * mm, 14 * mm, 38 * mm, W - 97 * mm]
n = len(items)
row_h = min(16 * mm, (A4[1] - 2 * TM - 8 * mm - 6 * mm) / n)
cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8, leading=10)
big = ParagraphStyle("b", fontName="Helvetica-Bold", fontSize=10, leading=12)
head = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=9, leading=11)
pos = ParagraphStyle("p", fontName="Helvetica", fontSize=7.5, leading=9)

doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=LM, rightMargin=LM, topMargin=TM, bottomMargin=TM)
story, key = [], []
for s in range(sets):
    order = items[:]
    random.Random(2000 + s).shuffle(order)
    rows = [[Paragraph(h, head) for h in ("No.", "English", "P.O.S.", "Korean", "Example")]]
    for i, it in enumerate(order, 1):
        rows.append([Paragraph(str(i), cell), Paragraph(it["en"], big), Paragraph(it["pos"], pos), "",
                     Paragraph(it["ex"].replace("{}", BLANK), cell)])
    t = Table(rows, colWidths=cols, rowHeights=[8 * mm] + [row_h] * n)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9d9d9")),
        ("BOX", (0, 0), (-1, -1), 1.2, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    story += [t] + ([PageBreak()] if s < sets - 1 else [])
    key.append((s + 1, order))
doc.build(story)

lines = ["# Answer key", ""]
for s, order in key:
    lines += [f"## Set {s}", "", "| No. | English | P.O.S. | Korean | Example |", "|---|---|---|---|---|"]
    lines += [f'| {i} | {it["en"]} | {it["pos"]} | {it["ko"]} | {it["ex"].replace("{}", "**" + it["en"] + "**")} |'
              for i, it in enumerate(order, 1)] + [""]
src.with_name(src.stem + "_answers.md").write_text("\n".join(lines), encoding="utf-8")
print(out, n, "words x", sets, "sets")
