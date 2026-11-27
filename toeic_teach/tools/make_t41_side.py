"""TEST 41: 문제 바로 옆에 정답·해설을 붙인 복습용 PDF. -> data/workbook/RC_Test41_문제+해설.pdf"""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import t41_items as m
F = str(ROOT / "tools/fonts") + "/"; L = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("N", F + "NanumGothic-Regular.ttf")); pdfmetrics.registerFont(TTFont("NB", F + "NanumGothic-Bold.ttf"))
pdfmetrics.registerFont(TTFont("S", L + "LiberationSans-Regular.ttf")); pdfmetrics.registerFont(TTFont("S-B", L + "LiberationSans-Bold.ttf"))
registerFontFamily("S", normal="S", bold="S-B", italic="S", boldItalic="S-B"); registerFontFamily("N", normal="N", bold="NB", italic="N", boldItalic="NB")
st = lambda n, f, s, l: ParagraphStyle(n, fontName=f, fontSize=s, leading=l)
Q, C, K, H, T = st("q", "S", 10, 13.5), st("c", "S", 9.8, 13), st("k", "N", 9, 13.5), st("h", "NB", 11, 15), st("t", "NB", 15, 20)
P = Paragraph; AB = "ABCD"
W = landscape(A4)[0] - 24 * mm
rows = [[P("<b>문제</b>", H), P("<b>정답 · 알고리즘 해설</b>", H)]]
for i, it in enumerate(m.PART5):
    stem, opts, note, a = it
    q = [P(f"<b>{101 + i}.</b> {stem}", Q)] + [P(f"({AB[k]}) {o}", C) for k, o in enumerate(opts)]
    rows.append([q, [P(f"<b>정답 ({AB[a]}) {opts[a]}</b>", K), Spacer(1, 3), P(note, K)]])
s7 = m.PART7[0]; p = s7["passages"][0]
for stem, opts, note, a in s7["qs"]:
    q = [P(f"<b>{p['title']}</b>", Q)] + [P(b, C) for b in p["body"]] + [Spacer(1, 4), P(f"<b>147.</b> {stem}", Q)] + [P(f"({AB[k]}) {o}", C) for k, o in enumerate(opts)]
    rows.append([q, [P(f"<b>정답 ({AB[a]}) {opts[a]}</b>", K), Spacer(1, 3), P(note, K)]])
t = Table(rows, colWidths=[W * 0.5, W * 0.5], repeatRows=1)
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5e7eb")),
                       ("BACKGROUND", (1, 1), (1, -1), colors.HexColor("#f8fafc")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
out = ROOT / "data/workbook/RC_Test41_문제+해설.pdf"
SimpleDocTemplate(str(out), pagesize=landscape(A4), leftMargin=12 * mm, rightMargin=12 * mm, topMargin=12 * mm, bottomMargin=12 * mm, title="TEST 41 문제+해설").build(
    [P("11/15 시험 복원 문항: 문제 + 정답·해설", T), P("공개 복원 자료 기반이라 실제 시험 문장·정답과 다를 수 있음.", K), Spacer(1, 4 * mm), t])
print(out)
