"""약점 메우기 워크북 오답만 다시: python3 tools/make_weak_retry.py 2,3,5 tag -> data/workbook/Weak_Retry_<tag>.pdf (문제 + 마지막 장 정답·규칙)"""
import random, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from weak_fill_items import CH
pdfmetrics.registerFont(TTFont("S", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("K", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))
st = lambda f, s, l, c="#000000": ParagraphStyle("x", fontName=f, fontSize=s, leading=l, textColor=colors.HexColor(c))
L = "ABCD"
items = []
for ci, (title, tip, its) in enumerate(CH):
    for ii, (stem, opts, rule, src) in enumerate(its):
        order = list(range(4)); random.Random(1000 * ci + ii + 7).shuffle(order)
        ch = [opts[i] for i in order]
        items.append((stem, ch, order.index(0), rule, src))
nums = [int(x) for x in sys.argv[1].split(",")]
tag = sys.argv[2]
s = [Paragraph(f"약점 메우기 오답 다시 풀기 ({len(nums)}문항)", st("K", 16, 22)),
     Paragraph("번호는 워크북 번호 그대로. 선지 보기 전에 번호 옆에 형/부/명/동 한 글자 먼저.", st("K", 9.5, 14, "#555555")), Spacer(1, 10)]
for n in nums:
    stem, ch, a, rule, src = items[n - 1]
    s.append(KeepTogether([Paragraph(f"<b>{n}.</b> {stem}", st("S", 11, 15))] +
                          [Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;({L[k]}) {o}", st("S", 11, 15)) for k, o in enumerate(ch)] + [Spacer(1, 12)]))
s += [PageBreak(), Paragraph("정답 · 규칙", st("K", 15, 21)), Spacer(1, 6)]
for n in nums:
    stem, ch, a, rule, src = items[n - 1]
    s += [Paragraph(f"<b>{n}. ({L[a]}) {ch[a]}</b>", st("K", 10.5, 15)), Paragraph(f"{rule}  ·  원래 오답: {src}", st("K", 9.5, 14, "#444444")), Spacer(1, 5)]
SimpleDocTemplate(str(ROOT / f"data/workbook/Weak_Retry_{tag}.pdf"), pagesize=A4, leftMargin=46, rightMargin=46, topMargin=40, bottomMargin=40).build(s)
print("ok")
