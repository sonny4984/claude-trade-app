"""TEST 34 Part 7 해설지: 지문 전체 해석 + 문항·선지 해석(인쇄 순서) + 정답 + 해설 + 어휘.
Usage: python3 tools/make_t34_kaesul.py"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import t34_items as m, t34_kr as k
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
root = Path(__file__).resolve().parent.parent
F = Path(__file__).parent / "fonts"
pdfmetrics.registerFont(TTFont("N", str(F / "NanumGothic-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NB", str(F / "NanumGothic-Bold.ttf")))
from reportlab.lib.fonts import addMapping
addMapping("N", 0, 0, "N"); addMapping("N", 1, 0, "NB"); addMapping("N", 0, 1, "N"); addMapping("N", 1, 1, "NB")
key = {int(x[:3]): "ABCD".index(x[3]) for x in (root / "data/workbook/RC_Test34_key.txt").read_text().split()}
LINES = {"recognizes": 4, "support": 7, "drew": 2}
MINE = {149: "D", 156: "C", 157: "A", 164: "B", 177: "C", 180: "C"}  # 동하 오답 (11/7)
S = lambda **kw: ParagraphStyle("x", **{"fontName": "N", "fontSize": 9.3, "leading": 13.2, **kw})
H = S(fontName="NB", fontSize=12, leading=15, textColor=colors.white)
SUB = S(fontName="NB", fontSize=9.6, textColor=colors.HexColor("#1f4e79"), spaceBefore=6, spaceAfter=2)
P = S(spaceAfter=3); QE = S(fontName="NB", fontSize=9.3); QK = S(textColor=colors.HexColor("#333333"))
OPT = S(leftIndent=14); EXP = S(leftIndent=8, textColor=colors.HexColor("#7a2e00")); VOC = S(fontSize=8.6, leading=12)
def bar(t):
    tb = Table([[Paragraph(t, H)]], colWidths=[515])
    tb.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1f4e79")), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    return tb
story = [Paragraph("실전 TEST 34 · PART 7 정답 및 해설", S(fontName="NB", fontSize=16, leading=20)),
         Paragraph("지문 전체 해석 · 문항/선지 해석(시험지 인쇄 순서) · 정답 근거 · 어휘. <font color='#c00000'>[동하 오답]</font> 표시는 11/7 풀이 기준.", P), Spacer(1, 6)]
qs = [q for s in m.PART7 for q in s["qs"]]
for first, last, kind, paras, vocab in k.SETS:
    story += [Spacer(1, 6), bar(f"Questions {first}-{last}  |  {kind}"), Paragraph("지문 해석", SUB)]
    story += [Paragraph(x, P) for x in paras]
    story.append(Paragraph("문항 해설", SUB))
    for n in range(first, last + 1):
        it = qs[n - 147]; qk, ok = k.QK[n]
        if len(it) == 4:
            en, kr, ans = it[1], ok, it[3]
        else:
            p = key[n]
            en = it[1][1:p + 1] + [it[1][0]] + it[1][p + 1:]
            kr = ok[1:p + 1] + [ok[0]] + ok[p + 1:]
            ans = p
        assert ans == key[n], n
        stem = re.sub(r"\{LINE:(\w+)\}", lambda mm: str(LINES[mm.group(1)]), it[0])
        blk = [Paragraph(f"{n}. {stem}", QE), Paragraph(qk, QK)]
        for i, (e, kk) in enumerate(zip(en, kr)):
            L = "ABCD"[i]
            if i == ans:
                blk.append(Paragraph(f"<font color='#0a7a2a'><b>({L}) {e}</b> — {kk}  ← 정답</font>", OPT))
            elif MINE.get(n) == L:
                blk.append(Paragraph(f"<font color='#c00000'>({L}) {e} — {kk}  ← 동하 오답</font>", OPT))
            else:
                blk.append(Paragraph(f"({L}) {e} — {kk}", OPT))
        tag = " <font color='#c00000'>[동하 오답]</font>" if n in MINE else ""
        note = it[2]
        if len(it) != 4:  # notes name options in item order (A = correct); convert to printed letters
            def mp(mm):
                j = "ABCD".index(mm.group(1))
                return "(" + "ABCD"[p if j == 0 else (j - 1 if j - 1 < p else j)]
            note = re.sub(r"\(([ABCD])(?=[ )])", mp, note)
        blk += [Paragraph(f"정답 ({'ABCD'[ans]}){tag}  해설: {note}", EXP), Spacer(1, 5)]
        story.append(KeepTogether(blk))
    story += [Paragraph("어휘", SUB), Paragraph(vocab, VOC)]
out = root / "data/workbook/RC_Test34_P7_해설지.pdf"
SimpleDocTemplate(str(out), pagesize=A4, leftMargin=40, rightMargin=40, topMargin=36, bottomMargin=36,
                  title="TEST 34 Part 7 해설지").build(story)
print(out)
