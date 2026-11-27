"""RC 오답 해설지 (모듈 인자): 실제 시험지 모양 + 정답 근거 형광펜 + 해설 → Test8_RC_Review.pdf"""
import re, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, CondPageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import importlib
M = importlib.import_module(sys.argv[1])
P5, SETS, PARA, P5_KR, EX_KR, SET_VOC, META = M.P5, M.SETS, M.PARA, M.P5_KR, M.EX_KR, M.SET_VOC, M.META

LIB = "/usr/share/fonts/truetype/liberation/"
for n, f in [("S", "LiberationSans-Regular"), ("SB", "LiberationSans-Bold"), ("SI", "LiberationSans-Italic"),
             ("R", "LiberationSerif-Regular"), ("RB", "LiberationSerif-Bold"), ("RI", "LiberationSerif-Italic")]:
    pdfmetrics.registerFont(TTFont(n, LIB + f + ".ttf"))
pdfmetrics.registerFont(TTFont("K", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("DJ", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
registerFontFamily("S", normal="S", bold="SB", italic="SI", boldItalic="SB")
registerFontFamily("R", normal="R", bold="RB", italic="RI", boldItalic="RB")
registerFontFamily("K", normal="K", bold="K", italic="K", boldItalic="K")

def st(f, s, l, c="#000000", **k): return ParagraphStyle("x", fontName=f, fontSize=s, leading=l, textColor=colors.HexColor(c), **k)
W = A4[0] - 64
YEL, PINK = "#fff176", "#f8bbd0"
GREEN, RED, BLUE = "#1b7f3b", "#c62828", "#1a56b8"
OK = '<font name="DJ" color="%s">✓</font>' % GREEN
NO = '<font name="DJ" color="%s">✗</font>' % RED

def hl(t):
    t = re.sub(r"\[\[(.+?)\]\]", lambda m: f'<span backColor="{YEL}">{m.group(1)}</span>', t)
    t = re.sub(r"\{\{(.+?)\}\}", lambda m: f'<span backColor="{PINK}">{m.group(1)}</span>', t)
    return t

def kfix(t):  # 한글 해설 안의 기호
    return t.replace("✗", NO).replace("✓", OK).replace("→", '<font name="DJ">→</font>').replace("↔", '<font name="DJ">↔</font>').replace("⚠", '<font name="DJ">⚠</font>').replace("①", "(1)").replace("②", "(2)").replace("③", "(3)")

PASS = st("R", 10.6, 15.6, spaceAfter=5)
QST = st("S", 9.8, 13)
OPT = st("S", 9.6, 12.6, leftIndent=14)
KB = st("K", 9.3, 14)
KS = st("K", 8.6, 12.5, "#444444")

def opt_par(L, text, mine, ans):
    if L == ans and L == mine:
        return Paragraph(f'<font color="{GREEN}"><b>({L}) {text}</b></font> <font name="K" color="{GREEN}">◀ 정답 (내 답)</font>', OPT)
    if L == ans:
        return Paragraph(f'<font color="{GREEN}"><b>({L}) {text}</b></font> <font name="K" color="{GREEN}">◀ 정답</font>', OPT)
    if L == mine:
        return Paragraph(f'<font color="{RED}"><strike>({L}) {text}</strike></font> <font name="K" color="{RED}">◀ 내 답</font>', OPT)
    return Paragraph(f"({L}) {text}", OPT)

def q_block(num, stem, opts, mine, ans, note):
    mark = OK if mine == ans else NO
    rows = [Paragraph(f"<b>{num}.</b> {stem} {mark}" if stem else f"<b>{num}.</b> {mark}", QST)]
    rows += [opt_par(L, o, mine, ans) for L, o in zip("ABCD", opts)]
    if note:
        rows.append(Paragraph(kfix("근거: " + note), st("K", 8.4, 12, "#555555", leftIndent=14, spaceBefore=2)))
    return rows

def ex_box(num, e, mine, ans):
    lines = [Paragraph(f'<font color="{RED}"><b>{num}번 해설</b></font>  내 답 ({mine}) <font name="DJ">→</font> 정답 ({ans})', st("K", 11, 16)),
             Paragraph(kfix(f"<b>① 유형</b>  {e['kind']}"), KB),
             Paragraph(kfix(f"<b>② 봤어야 할 곳</b>  {e['look']}"), KB),
             Paragraph(kfix(f"<b>③ 어긋난 단계</b>  {e['slip']}"), KB),
             Paragraph(kfix(f"<b>④ 정답 근거</b>  {e['why']}"), KB),
             Paragraph(kfix("<b>⑤ 오답 탈락</b>"), KB)]
    lines += [Paragraph(kfix("· " + x), st("K", 9.1, 13.5, leftIndent=10)) for x in e["elim"]]
    lines += [Paragraph(kfix(f'<b>함정 이름</b>  <font color="{RED}">{e["trap"]}</font>'), KB),
              Paragraph(kfix(f'<b>기억할 규칙</b>  <font color="{BLUE}">{e["rule"]}</font>'), KB)]
    if e.get("var"):
        q, o, _ = e["var"]
        lines.append(Paragraph(kfix(f"<b>같은 규칙 변형</b> (답은 맨 뒤)  {q}  " + "  ".join(f"({L}) {x}" for L, x in zip("ABCD", o))), st("K", 9.1, 13.5, "#333333")))
    t = Table([[lines]], colWidths=[W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef4fc")), ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#9db8dd")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t

def kr_box(rows, title="해석 · 단어"):
    t = Table([[[Paragraph(f'<font color="#7a5b00"><b>{title}</b></font>', st("K", 10, 14))] + rows]], colWidths=[W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fffbea")), ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#e2c46b")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return t

def voc_line(v):
    return Paragraph("<b>단어</b>  " + "  ·  ".join((f"<b>{w}</b> ({p}) {m}" if len(x) == 3 else f"<b>{x[0]}</b> {x[1]}") for x in v for w, p, m in ([x] if len(x) == 3 else [(x[0], "", x[1])])), st("K", 9, 13.5))

def passage_box(title, paras):
    body = []
    if title:
        body.append(Paragraph(hl(title), st("R", 10.6, 14.5, spaceAfter=7)))
    body += [Paragraph(hl(p), PASS) for p in paras]
    t = Table([[body]], colWidths=[W - 2])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, colors.black), ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                           ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t

def two_col(blocks):
    rows = []
    for i in range(0, len(blocks), 2):
        a = blocks[i]; b = blocks[i + 1] if i + 1 < len(blocks) else [Paragraph("", QST)]
        rows.append([a, b])
    t = Table(rows, colWidths=[W / 2, W / 2])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]))
    return t

def tbl(rows, widths, head=True, fs=9):
    t = Table([[Paragraph(kfix(str(c)), st("K", fs, fs * 1.45)) for c in r] for r in rows], colWidths=[W * x for x in widths], repeatRows=1 if head else 0)
    s = [("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b8b8b8")), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if head: s.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef2f8")))
    t.setStyle(TableStyle(s)); return t

H1, H2, SUB = st("K", 17, 24), st("K", 12.5, 18, BLUE, spaceBefore=6, spaceAfter=4), st("K", 9, 13.5, "#555555")
s = [Paragraph(META["title"], H1),
     Paragraph(META["sub"] + " "
               f'<span backColor="{YEL}">노랑 = 정답 근거</span>, <span backColor="{PINK}">분홍 = 함정(오답이 끌린 단어)</span>. '
               f'선지: <font color="{GREEN}"><b>초록 = 정답</b></font>, <font color="{RED}"><strike>빨강</strike> = 내 답</font>.', SUB), Spacer(1, 8),
     Paragraph("한눈에 보기", H2),
     tbl([["번호", "내 답 → 정답", "유형", "함정 이름", "응시자 정답률"]] + META["summary"], [0.08, 0.3, 0.2, 0.3, 0.12]),
     Spacer(1, 8), Paragraph(META["diag_title"], H2), Paragraph(kfix(META["diag"]), KB)]
if META.get("missing"): s += [Spacer(1, 4), Paragraph(kfix(META["missing"]), st("K", 9, 13.5, "#a33"))]
s += [PageBreak()]
if P5: s.append(Paragraph("PART 5", st("SB", 13, 18, spaceAfter=6)))
def p5_kr(num):
    k = P5_KR[num]
    rows = [Paragraph(kfix(f"<b>문장 해석</b>  {k['tr']}"), st("K", 9.4, 14)),
            Paragraph("<b>선지 뜻</b>  " + "  /  ".join(f"({L}) {o}" for L, o in zip("ABCD", k["opts"])), st("K", 9, 13.5)),
            voc_line(k["voc"])]
    return kr_box(rows)

for num, stem, opts, mine, ans, e in P5:
    s.append(KeepTogether([Paragraph(f"<b>{num}.</b> {stem} {NO}", st("S", 10.2, 14)), Spacer(1, 2)]
                          + [opt_par(L, o, mine, ans) for L, o in zip("ABCD", opts)] + [Spacer(1, 6), p5_kr(num), Spacer(1, 5), ex_box(num, e, mine, ans), Spacer(1, 14)]))

for i, S in enumerate(SETS):
    if i or P5: s += [PageBreak()]
    if S.get("part"): s.append(Paragraph(S["part"], st("SB", 13, 18, spaceAfter=6)))
    s.append(Paragraph(f"<b>{S['hdr']}</b>", st("S", 10.2, 14, spaceAfter=6)))
    for title, paras in S["docs"]:
        s += [passage_box(title, paras), Spacer(1, 8)]
    s.append(two_col([q_block(*q) for q in S["qs"]]))
    first = S["qs"][0][0]
    if first in SET_VOC:
        s += [Spacer(1, 2), kr_box([voc_line(SET_VOC[first])], "지문 단어")]
    for q in S["qs"]:
        if q[0] in S["ex"]:
            k = EX_KR[q[0]]
            rows = [Paragraph(kfix(f"<b>질문 해석</b>  {k['q']}"), st("K", 9.3, 14)),
                    Paragraph("<b>선지 해석</b>  " + "  /  ".join(f"({L}) {o}" for L, o in zip("ABCD", k["opts"])), st("K", 9, 13.5)),
                    Paragraph(kfix(f"<b>근거 문장 해석</b>  {k['ev']}"), st("K", 9.3, 14))]
            s += [CondPageBreak(260), Spacer(1, 6), kr_box(rows, f"{q[0]}번 해석"), Spacer(1, 4), ex_box(q[0], S["ex"][q[0]], q[3], q[4]), Spacer(1, 8)]

s += [PageBreak(), Paragraph("바꿔 말하기 짝 (시험 전날 5분)", H2),
      tbl([["지문", "선지(정답)", "번호"]] + [[a, b, str(n)] for a, b, n in PARA], [0.48, 0.42, 0.1]),
      Spacer(1, 10), Paragraph("변형 문제 정답", H2)]
vans = [(n, e["var"][2]) for n, _, _, _, _, e in P5 if e.get("var")] + [(k, v["var"][2]) for S in SETS for k, v in S["ex"].items() if v.get("var")]
s.append(Paragraph("  ".join(f"{n}번 변형 → ({a})" for n, a in vans), KB))
s += [Spacer(1, 10), Paragraph("다음에 할 것", H2), Paragraph(kfix(META["next"]), KB)]
SimpleDocTemplate(str(HERE / META["out"]), pagesize=A4, leftMargin=32, rightMargin=32, topMargin=32, bottomMargin=32, title=META["title"]).build(s)
print("ok")
