"""Build an original TOEIC-style RC practice test PDF (Parts 5-7, 100 questions) + answer sheet + Korean answer key.
Usage: python3 tools/make_mock.py [items_module] [number]  -> data/workbook/RC_Mock<number>_*.pdf"""
import importlib, random, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, KeepTogether, FrameBreak,
                                NextPageTemplate, PageBreak, Table, TableStyle, Flowable, CondPageBreak)

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "tools"))
MOD = sys.argv[1] if len(sys.argv) > 1 else "mock1_items"
NUM = sys.argv[2] if len(sys.argv) > 2 else "1"
_m = importlib.import_module(MOD)
PART5, PART6, PART7 = _m.PART5, _m.PART6, _m.PART7

pdfmetrics.registerFont(TTFont("NG", str(root / "tools/fonts/NanumGothic-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NG-B", str(root / "tools/fonts/NanumGothic-Bold.ttf")))
out_dir = root / "data/workbook"
out_dir.mkdir(parents=True, exist_ok=True)
NAME = f"RC Practice Test {NUM}"

PW, PH = A4
LM = RM = 14 * mm
TM, BM = 13 * mm, 17 * mm
W = PW - LM - RM
GUT = 9 * mm
CW = (W - GUT) / 2
SANS, SANSB, SERIF, SERIFB = "Helvetica", "Helvetica-Bold", "Times-Roman", "Times-Bold"

st = lambda **k: ParagraphStyle("x", **k)
q_stem = st(fontName=SANS, fontSize=10, leading=13.5, leftIndent=19, firstLineIndent=-19, spaceAfter=2)
q_ch = st(fontName=SANS, fontSize=10, leading=13.8, leftIndent=19)
q_ch_hang = st(fontName=SANS, fontSize=10, leading=13.2, leftIndent=37, firstLineIndent=-18)
p_txt = st(fontName=SERIF, fontSize=10.6, leading=14.2, spaceAfter=5)
p_head = st(fontName=SERIFB, fontSize=11.5, leading=15, alignment=TA_CENTER, spaceAfter=5)
p_small = st(fontName=SANS, fontSize=9.3, leading=12.5)
intro = st(fontName=SANSB, fontSize=10, leading=13, spaceBefore=4, spaceAfter=5)
dir_t = st(fontName=SANSB, fontSize=12, leading=15)
dir_b = st(fontName=SANS, fontSize=9.5, leading=13)
part_t = st(fontName=SANSB, fontSize=11, leading=14, spaceBefore=5)

# ---------- answer placement
def place(items, seed):
    seq = [i % 4 for i in range(len(items))]
    random.Random(seed).shuffle(seq)
    out = []
    for it, p in zip(items, seq):
        stem, ch, note = it[0], it[1], it[2]
        if len(it) == 4:  # fixed order
            out.append((stem, ch, it[3], note))
        else:
            order = ch[1:p + 1] + [ch[0]] + ch[p + 1:]
            out.append((stem, order, p, note))
    return out

p5 = place(PART5, 500 + int(NUM))
p6_flat = place([q for s in PART6 for q in s["qs"]], 600 + int(NUM))
p7_flat = place([q for s in PART7 for q in s["qs"]], 700 + int(NUM))
key = []  # (num, letter, correct_text, note)

def q_flow(num, stem, ch, width_note=False):
    fl = []
    if stem:
        fl.append(Paragraph(f"<b>{num}.</b>&nbsp;&nbsp;{stem}", q_stem))
        lead = ""
    else:
        lead = f"<b>{num}.</b>&nbsp;&nbsp;"
    for k, t in enumerate(ch):
        txt = f"({'ABCD'[k]})&nbsp;&nbsp;{t}"
        if not stem and k == 0:
            fl.append(Paragraph(lead + txt, st(fontName=SANS, fontSize=10, leading=13.2, leftIndent=37, firstLineIndent=-37)))
        else:
            fl.append(Paragraph(txt, q_ch_hang))
    fl.append(Spacer(1, 10))
    return fl

def two_col(qflows):
    half = (len(qflows) + 1) // 2
    left = [f for q in qflows[:half] for f in q]
    right = [f for q in qflows[half:] for f in q]
    t = Table([[left, right]], colWidths=[CW + GUT / 2, CW + GUT / 2])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t

def blank(n):
    return f"<u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{n}.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>"

def render_blocks(blocks):
    boxes, cur = [], []
    for kind, val in blocks + [("sep", "")]:
        if kind == "sep":
            if cur:
                boxes.append(cur)
            cur = []
            continue
        if kind == "h":
            cur.append(Paragraph(val, p_head))
        elif kind == "p":
            for n in range(131, 147):
                val = val.replace("{%d}" % n, blank(n))
            cur.append(Paragraph(val, p_txt))
        elif kind == "kv":
            rows = [[Paragraph(f"<b>{k}:</b>", p_small), Paragraph(v, p_small)] for k, v in val]
            t = Table(rows, colWidths=[22 * mm, W - 42 * mm])
            t.setStyle(TableStyle([("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.black), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                   ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
            cur += [t, Spacer(1, 6)]
        elif kind == "table":
            ncol = len(val[0])
            rows = [[Paragraph(("<b>%s</b>" % c) if i == 0 else c, p_small) for c in r] for i, r in enumerate(val)]
            t = Table(rows, colWidths=[(W - 20 * mm) / ncol] * ncol)
            t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.black), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            cur += [t, Spacer(1, 6)]
        elif kind == "chat":
            for name, time, text in val:
                cur.append(Paragraph(f"<b>{name}</b> &nbsp;[{time}]<br/>{text}", st(fontName=SANS, fontSize=9.6, leading=12.8, spaceAfter=4)))
    out = []
    for b in boxes:
        t = Table([[b]], colWidths=[W - 8 * mm])
        t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, colors.black), ("LEFTPADDING", (0, 0), (-1, -1), 8),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        t.hAlign = "CENTER"
        out += [t, Spacer(1, 6)]
    return out

class Box(Flowable):
    def __init__(self, fl):
        super().__init__(); self.fl = fl
    def wrap(self, aw, ah):
        self.sz = [f.wrap(W - 10 * mm, 1000)[1] for f in self.fl]
        self.h = sum(self.sz) + 2 * len(self.fl) + 8 * mm
        assert self.h <= HDR or True
        return W, self.h
    def draw(self):
        c = self.canv; c.setLineWidth(1); c.rect(0, 0, W, self.h)
        y = self.h - 4 * mm
        for f, h in zip(self.fl, self.sz):
            y -= h; f.drawOn(c, 5 * mm, y); y -= 2

# ---------- document
doc = BaseDocTemplate(str(out_dir / f"RC_Mock{NUM}_Test.pdf"), pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM,
                      bottomMargin=BM, title=NAME, author="")
HDR = 50 * mm
def cols(top):
    h = PH - TM - BM - top
    return [Frame(LM, BM, CW, h, leftPadding=0, rightPadding=0, topPadding=2, bottomPadding=0),
            Frame(LM + CW + GUT, BM, CW, h, leftPadding=0, rightPadding=0, topPadding=2, bottomPadding=0)]
full = [Frame(LM, BM, W, PH - TM - BM, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)]
state = {"stop": False}

def footer(c, d, line_top=None, arrow=True):
    c.saveState()
    if line_top is not None:
        c.setLineWidth(0.5); c.line(LM + CW + GUT / 2, BM, LM + CW + GUT / 2, line_top)
    c.setFont(SANS, 8); c.drawString(LM, 9 * mm, NAME); c.drawCentredString(PW / 2, 9 * mm, str(d.page))
    if arrow and not state["stop"]:
        c.setFont("Helvetica-BoldOblique", 8); x = PW - RM - 6 * mm
        c.drawRightString(x, 9 * mm, "GO ON TO THE NEXT PAGE")
        c.setLineWidth(1.2); c.line(x + 1.5 * mm, 10 * mm, x + 5.5 * mm, 10 * mm)
        c.line(x + 3.8 * mm, 11.6 * mm, x + 5.5 * mm, 10 * mm); c.line(x + 3.8 * mm, 8.4 * mm, x + 5.5 * mm, 10 * mm)
    c.restoreState()

def cover(c, d):
    c.saveState()
    c.setLineWidth(2); c.rect(LM, PH - 120 * mm, W, 80 * mm)
    c.setFont(SANSB, 22); c.drawCentredString(PW / 2, PH - 62 * mm, "READING TEST")
    c.setFont(SANS, 13); c.drawCentredString(PW / 2, PH - 74 * mm, "Parts 5, 6, and 7  ·  100 Questions  ·  75 Minutes")
    c.setFont(SANSB, 14); c.drawCentredString(PW / 2, PH - 92 * mm, NAME)
    c.setFont(SANS, 9.5)
    c.drawCentredString(PW / 2, PH - 108 * mm, "Original practice material written for personal study. This is not an official ETS test.")
    c.setFont("NG", 10.5)
    lines = ["사용법", "1. 타이머 75분. Part 5·6은 15분 안팎, Part 7에 약 60분을 목표로.",
             "2. 답은 마지막 장 답안지에 칠하고, 확신 없는 문제는 '?'도 칠하기.",
             "3. Part 별로 끝난 시각을 답안지 상단에 적기 (시간 배분 진단용).",
             "4. 채점은 별도 PDF(정답과 해설). 틀린 번호와 '?' 번호를 보내주면 함께 분석."]
    y = PH - 140 * mm
    for i, l in enumerate(lines):
        c.setFont("NG-B" if i == 0 else "NG", 11 if i == 0 else 10.5); c.drawString(LM + 6 * mm, y, l); y -= 8 * mm
    c.restoreState()

doc.addPageTemplates([
    PageTemplate(id="cover", frames=full, onPage=cover),
    PageTemplate(id="p5first", frames=[Frame(LM, PH - TM - HDR, W, HDR, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)] + cols(HDR),
                 onPageEnd=lambda c, d: footer(c, d, PH - TM - HDR)),
    PageTemplate(id="p5", frames=cols(0), onPageEnd=lambda c, d: footer(c, d, PH - TM)),
    PageTemplate(id="full", frames=full, onPageEnd=lambda c, d: footer(c, d)),
    PageTemplate(id="sheet", frames=full, onPageEnd=lambda c, d: footer(c, d, arrow=False)),
])

story = [Spacer(1, 1), NextPageTemplate("p5first"), PageBreak()]
story += [Box([Paragraph("READING TEST", dir_t),
               Paragraph("In the Reading test, you will read a variety of texts and answer reading comprehension questions. "
                         "The entire Reading test lasts 75 minutes and has three parts. Answer as many questions as possible "
                         "within the time allowed, and mark your answers on the answer sheet.", dir_b),
               Paragraph("PART 5", part_t),
               Paragraph("<b>Directions:</b> Each sentence below is missing a word or phrase. Four answer choices are given "
                         "below each sentence. Select the best answer to complete the sentence.", dir_b)]),
          FrameBreak(), NextPageTemplate("p5")]
for i, (stem, ch, ans, note) in enumerate(p5):
    n = 101 + i
    key.append((n, "ABCD"[ans], ch[ans], note))
    blk = [Paragraph(f"<b>{n}.</b>&nbsp;&nbsp;{stem}", q_stem)] + \
          [Paragraph(f"({'ABCD'[k]})&nbsp;&nbsp;{t}", q_ch) for k, t in enumerate(ch)] + [Spacer(1, 13)]
    story.append(KeepTogether(blk))

story += [NextPageTemplate("full"), PageBreak(),
          Box([Paragraph("PART 6", part_t),
               Paragraph("<b>Directions:</b> Each text below is missing words, phrases, or a sentence. Four answer choices "
                         "are given for each question below the text. Select the best answer to complete the text.", dir_b)]),
          Spacer(1, 8)]
n, qi = 131, 0
for s in PART6:
    blocks = render_blocks(s["blocks"])
    qfl = []
    for _ in s["qs"]:
        stem, ch, ans, note = p6_flat[qi]; qi += 1
        key.append((n, "ABCD"[ans], ch[ans], note))
        qfl.append(q_flow(n, "", ch)); n += 1
    story.append(KeepTogether([Paragraph(s["intro"], intro)] + blocks + [Spacer(1, 4), two_col(qfl)]))
    story.append(Spacer(1, 14))

story += [PageBreak(),
          Box([Paragraph("PART 7", part_t),
               Paragraph("<b>Directions:</b> In this part, you will read texts such as notices, e-mails, articles, and "
                         "online chats. Each text or set of texts is followed by several questions. Select the best answer "
                         "for each question.", dir_b)]),
          Spacer(1, 8)]
qi = 0
for s in PART7:
    blocks = render_blocks(s["blocks"])
    qfl = []
    for _ in s["qs"]:
        stem, ch, ans, note = p7_flat[qi]; qi += 1
        key.append((n, "ABCD"[ans], ch[ans], note))
        qfl.append(q_flow(n, stem, ch)); n += 1
    multi = sum(1 for b in s["blocks"] if b[0] == "sep") > 0
    if multi:
        story += [CondPageBreak(120 * mm), Paragraph(s["intro"], intro)] + blocks + [CondPageBreak(70 * mm), two_col(qfl), Spacer(1, 14)]
    else:
        story.append(KeepTogether([Paragraph(s["intro"], intro)] + blocks + [Spacer(1, 4), two_col(qfl)]))
        story.append(Spacer(1, 14))

class Stop(Flowable):
    def wrap(self, aw, ah): return aw, 14 * mm
    def draw(self):
        state["stop"] = True
        c = self.canv; c.setFont(SANSB, 10.5)
        c.drawCentredString(W / 2, 6 * mm, "Stop! This is the end of the test. If you finish before time is called,")
        c.drawCentredString(W / 2, 1 * mm, "you may go back to Parts 5, 6, and 7 and check your work.")
story += [Spacer(1, 6), Stop()]
assert n == 201, n

# ---------- answer sheet
class Sheet(Flowable):
    def wrap(self, aw, ah):
        self.h = ah - 4; return aw, self.h
    def draw(self):
        c = self.canv
        c.setFont(SANSB, 15); c.drawString(0, self.h - 6 * mm, "ANSWER SHEET")
        c.setFont(SANS, 9.5)
        c.drawString(0, self.h - 13 * mm, f"{NAME}    Date: __________    Part 5 end: ______   Part 6 end: ______   Part 7 end: ______")
        c.setFont("NG", 9); c.drawString(0, self.h - 19 * mm, "답을 칠하고, 확신이 없거나 찍은 문제는 오른쪽 점선 '?'도 칠해줘.")
        colw = W / 4
        rowh = 9.4 * mm
        for k in range(100):
            col, r = divmod(k, 25)
            x0 = col * colw
            y = self.h - 28 * mm - r * rowh
            c.setFont(SANSB, 8.5); c.drawRightString(x0 + 8 * mm, y - 1, str(101 + k))
            for j, letter in enumerate("ABCD"):
                cx = x0 + 12.5 * mm + j * 6.6 * mm
                c.setLineWidth(0.7); c.circle(cx, y + 1.2, 2.7 * mm)
                c.setFont(SANS, 6.5); c.drawCentredString(cx, y - 0.6, letter)
            cx = x0 + 12.5 * mm + 4 * 6.6 * mm + 1.5 * mm
            c.setDash(1.2, 1.2); c.circle(cx, y + 1.2, 2.7 * mm); c.setDash()
            c.setFont(SANS, 7); c.drawCentredString(cx, y - 0.6, "?")
            if k % 25 == 0 and k:
                pass
        for col in range(1, 4):
            c.setLineWidth(0.4); c.line(col * colw - 2 * mm, 20 * mm, col * colw - 2 * mm, self.h - 24 * mm)

story += [NextPageTemplate("sheet"), PageBreak(), Sheet()]
doc.build(story)

# ---------- answer key (Korean)
kd = BaseDocTemplate(str(out_dir / f"RC_Mock{NUM}_Answers.pdf"), pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM,
                     bottomMargin=BM, title=f"{NAME} Answer Key")
kd.addPageTemplates([PageTemplate(id="k", frames=full, onPage=lambda c, d: (c.setFont("NG", 8), c.drawCentredString(PW / 2, 9 * mm, str(d.page))))])
h = st(fontName="NG-B", fontSize=14, leading=19, spaceAfter=4)
h2 = st(fontName="NG-B", fontSize=11.5, leading=16, spaceBefore=8, spaceAfter=4)
s = st(fontName="NG", fontSize=8.8, leading=12.3)
sb = st(fontName="NG-B", fontSize=8.8, leading=12.3)
ks = [Paragraph(f"{NAME} 정답과 해설", h),
      Paragraph("채점 전에 보지 마. 틀린 번호와 '?' 번호, Part별로 끝난 시각을 보내주면 왜 그 답을 골랐는지부터 같이 볼게.", s),
      Spacer(1, 6)]
for label, lo, hi in (("Part 5", 101, 130), ("Part 6", 131, 146), ("Part 7", 147, 200)):
    part = [k for k in key if lo <= k[0] <= hi]
    ks.append(Paragraph(label, h2))
    ks.append(Paragraph("정답표: " + "  ".join(f"{a}{b}" for a, b, _, _ in part), s))
    ks.append(Spacer(1, 4))
    rows = [[Paragraph("No.", sb), Paragraph("정답", sb), Paragraph("근거 · 규칙", sb)]]
    rows += [[Paragraph(str(a), s), Paragraph(f"({b}) {c}", s), Paragraph(d, s)] for a, b, c, d in part]
    t = Table(rows, colWidths=[11 * mm, 58 * mm, W - 69 * mm], repeatRows=1)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.black), ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.black),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    ks.append(t)
kd.build(ks)
from collections import Counter
print("answers:", Counter(k[1] for k in key), "total", len(key))
(out_dir / f"RC_Mock{NUM}_key.txt").write_text(" ".join(f"{a}{b}" for a, b, _, _ in key), encoding="utf-8")
