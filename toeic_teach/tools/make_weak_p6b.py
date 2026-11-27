"""P6 보충 6세트 -> data/workbook/Weak_Fill_P6_extra.pdf (문제 226~249 + 마지막 장 정답·규칙)"""
import random, re, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, CondPageBreak, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from weak_fill_items import P6_EXTRA
LIB = "/usr/share/fonts/truetype/liberation/"
for n, f in [("S", "LiberationSans-Regular"), ("SB", "LiberationSans-Bold"), ("R", "LiberationSerif-Regular"), ("RB", "LiberationSerif-Bold")]:
    pdfmetrics.registerFont(TTFont(n, LIB + f + ".ttf"))
pdfmetrics.registerFont(TTFont("K", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))
registerFontFamily("S", normal="S", bold="SB", italic="S", boldItalic="SB"); registerFontFamily("R", normal="R", bold="RB", italic="R", boldItalic="RB")
registerFontFamily("K", normal="K", bold="K", italic="K", boldItalic="K")
st = lambda f, s, l, c="#000000", **k: ParagraphStyle("x", fontName=f, fontSize=s, leading=l, textColor=colors.HexColor(c), **k)
L = "ABCD"; W = A4[0] - 68; START = 226
s = [Paragraph("약점 메우기 Part 6 보충 — 226~249", st("K", 16, 22)),
     Paragraph("앞 4세트에 없던 Part 6 오답 포인트(Test 5·TEST 44·모의고사·1000제 10회)를 6세트로. 정답은 마지막 장.", st("K", 9.5, 14, "#555555")), Spacer(1, 10)]
key = []; n = START - 1
for si, st6 in enumerate(P6_EXTRA):
    base = n
    body = []
    if st6.get("title"): body.append(Paragraph(f"<b>{st6['title']}</b>", st("RB", 11, 15, spaceAfter=6)))
    if st6.get("hdr"): body.append(Paragraph("<br/>".join(f"{k}: {v}" for k, v in st6["hdr"]), st("R", 10, 14, spaceAfter=8)))
    for t in st6["body"]:
        t = re.sub(r"\{(\d+)\}", lambda m: f"<b>------- ({base + int(m.group(1)) - 4 * si})</b>", t)
        body.append(Paragraph(t, st("R", 10.4, 17, spaceAfter=6)))
    box = Table([[body]], colWidths=[W - 4])
    box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.black), ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 8)]))
    qs = []
    for qi, (opts, rule, src) in enumerate(st6["qs"]):
        order = list(range(4)); random.Random(70000 + si * 10 + qi).shuffle(order)
        ch = [opts[i] for i in order]; a = order.index(0); num = base + qi + 1
        key.append((num, L[a], ch[a], rule, src))
        qs.append([Paragraph(f"<b>{num}.</b>", st("S", 9.8, 13))] + [Paragraph(f"({L[k]}) {o}", st("S", 9.8, 13, leftIndent=16)) for k, o in enumerate(ch)])
    grid = Table([[qs[0], qs[1]], [qs[2], qs[3]]], colWidths=[W / 2, W / 2])
    grid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    s += [CondPageBreak(330), Paragraph(f"<b>Questions {base + 1}-{base + 4}</b> refer to the following {st6['intro']}.", st("S", 10, 14, spaceAfter=6)), box, Spacer(1, 8), grid, Spacer(1, 14)]
    n += 4
s += [PageBreak(), Paragraph("정답 · 규칙 · 원래 오답", st("K", 15, 21)), Spacer(1, 6),
      Paragraph("빠른 정답표: " + "  ".join(f"{k[0]}{k[1]}" for k in key), st("S", 9, 13, spaceAfter=8))]
for num, a, word, rule, src in key:
    s += [Paragraph(f"<b>{num}. ({a}) {word}</b>", st("K", 10, 14)), Paragraph(f"{rule}  ·  원래 오답: {src}", st("K", 9.2, 13.5, "#444444")), Spacer(1, 5)]
SimpleDocTemplate(str(ROOT / "data/workbook/Weak_Fill_P6_extra.pdf"), pagesize=A4, leftMargin=34, rightMargin=34, topMargin=34, bottomMargin=34).build(s)
print("ok", " ".join(f"{k[0]}{k[1]}" for k in key))
