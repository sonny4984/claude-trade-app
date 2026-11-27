"""약점 메우기 워크북: tools/weak_fill_items.py → data/workbook/Weak_Fill_Workbook.pdf (문제) + Weak_Fill_Answers.pdf (정답·규칙·원래 오답)."""
import random, re, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                KeepTogether, NextPageTemplate, PageBreak, CondPageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from weak_fill_items import CH, P6

LIB = "/usr/share/fonts/truetype/liberation/"
for n, f in [("S", "LiberationSans-Regular"), ("SB", "LiberationSans-Bold"), ("R", "LiberationSerif-Regular"), ("RB", "LiberationSerif-Bold")]:
    pdfmetrics.registerFont(TTFont(n, LIB + f + ".ttf"))
WQ = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
pdfmetrics.registerFont(TTFont("K", WQ, subfontIndex=0))
registerFontFamily("S", normal="S", bold="SB", italic="S", boldItalic="SB")
registerFontFamily("R", normal="R", bold="RB", italic="R", boldItalic="RB")
registerFontFamily("K", normal="K", bold="K", italic="K", boldItalic="K")
st = lambda f, s, l, c="#000000", **k: ParagraphStyle("x", fontName=f, fontSize=s, leading=l, textColor=colors.HexColor(c), **k)
H1, H2, SUB = st("K", 17, 23), st("K", 12.5, 17, "#1a56b8", spaceBefore=4), st("K", 9, 13, "#555555", spaceAfter=6)
Q, CHO = st("S", 9.8, 12.8), st("S", 9.8, 12.6, leftIndent=16)
PS = st("R", 10.4, 17, spaceAfter=6)
KT, KTB = st("K", 8.6, 12), st("K", 8.6, 12)
L = "ABCD"
PW, PH = A4
M = 34
W = PW - 2 * M
OUT = ROOT / "data/workbook"

def shuffled(opts, seed):
    order = list(range(4)); random.Random(seed).shuffle(order)
    return [opts[i] for i in order], order.index(0)

# ---------- workbook
doc = BaseDocTemplate(str(OUT / "Weak_Fill_Workbook.pdf"), pagesize=A4, leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M,
                      title="약점 메우기 워크북")
cw = (W - 18) / 2
two = [Frame(M, M, cw, PH - 2 * M, id="l", leftPadding=0, rightPadding=0), Frame(M + cw + 18, M, cw, PH - 2 * M, id="r", leftPadding=0, rightPadding=0)]
one = [Frame(M, M, W, PH - 2 * M, id="f", leftPadding=0, rightPadding=0)]
pn = lambda c, d: (c.setFont("S", 8), c.drawCentredString(PW / 2, 18, str(d.page)))
doc.addPageTemplates([PageTemplate(id="two", frames=two, onPage=pn), PageTemplate(id="one", frames=one, onPage=pn)])

total = sum(len(c[2]) for c in CH)
s = [Paragraph("약점 메우기 워크북 — Part 5 · 6", H1),
     Paragraph(f"10/23부터 대화에서 보낸 Part 5·6 오답을 출제 포인트별로 모아, 같은 규칙·같은 함정으로 문장만 바꿨어. "
               f"Part 5 {total}문항 + Part 6 4세트(16문항). 모두 새로 쓴 문장이야. "
               "풀 때 번호 옆에 '동/부/전/접/어' 한 글자를 먼저 쓰고 고르기. 정답은 Weak_Fill_Answers.pdf (원래 틀린 문제 출처 포함).", SUB)]
key = []
n = 0
for ci, (title, tip, items) in enumerate(CH):
    s += [CondPageBreak(120), Paragraph(title, H2), Paragraph(tip, SUB)]
    for ii, (stem, opts, rule, src) in enumerate(items):
        n += 1
        ch, a = shuffled(opts, 1000 * ci + ii + 7)
        key.append((n, title, L[a], ch[a], rule, src))
        blk = [Paragraph(f"<b>{n}.</b> {stem}", Q)] + [Paragraph(f"({L[k]}) {o}", CHO) for k, o in enumerate(ch)] + [Spacer(1, 7)]
        s.append(KeepTogether(blk))
s += [NextPageTemplate("one"), PageBreak(), Paragraph("Part 6 — 같은 함정을 같은 위치에", H2)]
for si, st6 in enumerate(P6):
    lo = n + 1
    body = []
    if st6.get("title"):
        body.append(Paragraph(f"<b>{st6['title']}</b>", st("RB", 11, 15, spaceAfter=6)))
    if st6.get("hdr"):
        body.append(Paragraph("<br/>".join(f"{k}: {v}" for k, v in st6["hdr"]), st("R", 10, 14, spaceAfter=8)))
    for t in st6["body"]:
        t = re.sub(r"\{(\d+)\}", lambda m: f"<b>------- ({n + int(m.group(1)) - 4 * si})</b>", t)
        body.append(Paragraph(t, PS))
    box = Table([[body]], colWidths=[W - 4])
    box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.black), ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                             ("TOPPADDING", (0, 0), (-1, -1), 8)]))
    qs = []
    for qi, (opts, rule, src) in enumerate(st6["qs"]):
        ch, a = shuffled(opts, 50000 + si * 10 + qi)
        num = n + qi + 1
        key.append((num, "Part 6", L[a], ch[a], rule, src))
        qs.append([Paragraph(f"<b>{num}.</b>", Q)] + [Paragraph(f"({L[k]}) {o}", CHO) for k, o in enumerate(ch)])
    grid = Table([[qs[0], qs[1]], [qs[2], qs[3]]], colWidths=[W / 2, W / 2])
    grid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    s += [CondPageBreak(330), Paragraph(f"<b>Questions {lo}-{lo + 3}</b> refer to the following {st6['intro']}.", st("S", 10, 14, spaceAfter=6)),
          box, Spacer(1, 8), grid, Spacer(1, 14)]
    n += 4
doc.build(s)

# ---------- answers
kd = BaseDocTemplate(str(OUT / "Weak_Fill_Answers.pdf"), pagesize=A4, leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M, title="약점 메우기 정답")
kd.addPageTemplates([PageTemplate(id="one", frames=one, onPage=pn)])
ks = [Paragraph("약점 메우기 — 정답 · 규칙 · 원래 틀린 문제", H1),
      Paragraph("정답만 보지 말고 '규칙' 칸을 소리 내서 읽기. 또 틀린 번호는 '원래 오답' 칸의 문제를 다시 찾아보기.", SUB),
      Paragraph("빠른 정답표: " + "  ".join(f"{k[0]}{k[2]}" for k in key), st("S", 8.4, 12, spaceAfter=8))]
cur = None
rows = []
def flush():
    if rows:
        t = Table([[Paragraph(x, KTB) for x in ("No.", "정답", "규칙", "원래 오답")]] + rows, colWidths=[24, 118, W * 0.45 - 20, W - 142 - W * 0.45 + 20], repeatRows=1)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#bbbbbb")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef2f8")),
                               ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        ks.append(t); ks.append(Spacer(1, 8)); rows.clear()
for num, title, letter, word, rule, src in key:
    if title != cur:
        flush(); cur = title; ks.append(Paragraph(title, H2))
    rows.append([Paragraph(str(num), KT), Paragraph(f"({letter}) {word}", st("S", 8.6, 12)), Paragraph(rule, KT), Paragraph(src, KT)])
flush()
kd.build(ks)
(OUT / "Weak_Fill_key.txt").write_text(" ".join(f"{k[0]}{k[2]}" for k in key), encoding="utf-8")
from collections import Counter
print("items", len(key), Counter(k[2] for k in key))
