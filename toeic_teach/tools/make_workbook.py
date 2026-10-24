"""Build TOEIC-style Part 5 workbook PDFs (black & white, A4, 2 columns, answer sheet) + answer-key PDF.
Usage: python3 tools/make_workbook.py   -> data/workbook/*.pdf"""
import random, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, KeepTogether,
                                FrameBreak, NextPageTemplate, PageBreak, Table, TableStyle, Flowable)

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "tools"))
from p5_items import TEST_A, TEST_B, TEST_C

pdfmetrics.registerFont(TTFont("NG", str(root / "tools/fonts/NanumGothic-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NG-B", str(root / "tools/fonts/NanumGothic-Bold.ttf")))
out_dir = root / "data/workbook"
out_dir.mkdir(parents=True, exist_ok=True)

PW, PH = A4
LM = RM = 14 * mm
TM, BM = 13 * mm, 17 * mm
GUT = 9 * mm
CW = (PW - LM - RM - GUT) / 2
BODY, BOLD = "Helvetica", "Helvetica-Bold"

stem = ParagraphStyle("stem", fontName=BODY, fontSize=10.2, leading=14, leftIndent=19, firstLineIndent=-19, spaceAfter=3)
choice = ParagraphStyle("ch", fontName=BODY, fontSize=10.2, leading=14.5, leftIndent=19)
dir_t = ParagraphStyle("dt", fontName=BOLD, fontSize=12, leading=15)
dir_b = ParagraphStyle("db", fontName=BODY, fontSize=9.5, leading=13)
part = ParagraphStyle("pt", fontName=BOLD, fontSize=11, leading=14, spaceBefore=6)


class Box(Flowable):
    def __init__(self, flowables, width):
        super().__init__()
        self.fl, self.w = flowables, width
    def wrap(self, aw, ah):
        self.h = 0
        self.sizes = []
        for f in self.fl:
            w, h = f.wrap(self.w - 10 * mm, 1000)
            self.sizes.append(h)
            self.h += h + 2
        self.h += 8 * mm
        return self.w, self.h
    def draw(self):
        c = self.canv
        c.setLineWidth(1)
        c.rect(0, 0, self.w, self.h)
        y = self.h - 4 * mm
        for f, h in zip(self.fl, self.sizes):
            y -= h
            f.drawOn(c, 5 * mm, y)
            y -= 2


def build_test(name, label, items, fname):
    """items: list of (stem, [A,B,C,D], answer_letter)"""
    n = len(items)
    doc = BaseDocTemplate(str(out_dir / fname), pagesize=A4, leftMargin=LM, rightMargin=RM,
                          topMargin=TM, bottomMargin=BM, title=f"TOEIC Part 5 {label}", author="")
    hdr_h = 41 * mm
    fh = Frame(LM, PH - TM - hdr_h, PW - LM - RM, hdr_h, id="h", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    def cols(top_h):
        ch = PH - TM - BM - top_h
        return [Frame(LM, BM, CW, ch, id=f"l{top_h}", leftPadding=0, rightPadding=0, topPadding=2, bottomPadding=0),
                Frame(LM + CW + GUT, BM, CW, ch, id=f"r{top_h}", leftPadding=0, rightPadding=0, topPadding=2, bottomPadding=0)]
    state = {"last_q_page": None}

    def deco(canv, d, first, line=True):
        canv.saveState()
        mid = LM + CW + GUT / 2
        top = PH - TM - (hdr_h if first else 0)
        canv.setLineWidth(0.5)
        if line:
            canv.line(mid, BM, mid, top)
        canv.setFont(BODY, 8)
        canv.drawString(LM, 9 * mm, f"Part 5 · {label}")
        canv.drawCentredString(PW / 2, 9 * mm, str(d.page))
        canv.restoreState()

    def foot_next(canv, d):
        canv.saveState()
        canv.setFont("Helvetica-BoldOblique", 8)
        t = "GO ON TO THE NEXT PAGE"
        x = PW - RM - 6 * mm
        canv.drawRightString(x, 9 * mm, t)
        canv.setLineWidth(1.2)
        canv.line(x + 1.5 * mm, 10 * mm, x + 5.5 * mm, 10 * mm)
        canv.line(x + 3.8 * mm, 11.6 * mm, x + 5.5 * mm, 10 * mm)
        canv.line(x + 3.8 * mm, 8.4 * mm, x + 5.5 * mm, 10 * mm)
        canv.restoreState()

    def first_deco(canv, d): deco(canv, d, True); foot_next(canv, d)
    def later_deco(canv, d): deco(canv, d, False); foot_next(canv, d)
    def last_deco(canv, d): deco(canv, d, False, line=False)

    doc.addPageTemplates([
        PageTemplate(id="first", frames=[fh] + cols(hdr_h), onPage=first_deco),
        PageTemplate(id="later", frames=cols(0), onPage=later_deco),
        PageTemplate(id="sheet", frames=[Frame(LM, BM, PW - LM - RM, PH - TM - BM, id="s", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=last_deco),
    ])
    story = [Box([Paragraph("READING TEST", dir_t),
                  Paragraph("In this part, you will read sentences with a missing word or phrase. "
                            "The real Reading test gives 75 minutes for 100 questions; "
                            "for Part 5, aim for roughly 15 to 20 seconds per question.", dir_b),
                  Paragraph("PART 5", part),
                  Paragraph("<b>Directions:</b> Each sentence below is missing a word or phrase. "
                            "Four answer choices are given below each sentence. Select the best answer "
                            "and mark the letter (A), (B), (C), or (D) on the answer sheet at the end.", dir_b)],
                 PW - LM - RM),
             FrameBreak(), NextPageTemplate("later")]
    for i, (q, ch, _) in enumerate(items):
        num = 101 + i
        block = [Paragraph(f"<b>{num}.</b>&nbsp;&nbsp;{q}", stem)]
        block += [Paragraph(f"({'ABCD'[k]})&nbsp;&nbsp;{t}", choice) for k, t in enumerate(ch)]
        block.append(Spacer(1, 15))
        story.append(KeepTogether(block))
    story += [NextPageTemplate("sheet"), PageBreak()]

    # answer sheet
    sh = []
    sh.append(Paragraph("ANSWER SHEET", ParagraphStyle("t", fontName=BOLD, fontSize=15, leading=19)))
    sh.append(Paragraph(f"Part 5 · {label} &nbsp;&nbsp;&nbsp; Date: ____________ &nbsp;&nbsp; Time used: ________ min", dir_b))
    sh.append(Spacer(1, 6))
    sh.append(Paragraph("동그라미를 칠해. 확신이 없거나 찍은 문제는 오른쪽 '?'도 칠해줘.",
                        ParagraphStyle("k", fontName="NG", fontSize=9, leading=13)))
    sh.append(Spacer(1, 8))

    class Bubbles(Flowable):
        def __init__(self, total):
            super().__init__()
            self.total = total
        def wrap(self, aw, ah):
            return aw, ah
        def draw(self):
            c = self.canv
            half = (self.total + 1) // 2
            rowh = 10.2 * mm
            for col in range(2):
                x0 = col * ((PW - LM - RM) / 2) + 2 * mm
                for r in range(half):
                    k = col * half + r
                    if k >= self.total:
                        break
                    y = self.height - 4 * mm - r * rowh
                    c.setFont(BOLD, 9.5)
                    c.drawRightString(x0 + 9 * mm, y - 1, f"{101 + k}")
                    for j, letter in enumerate("ABCD"):
                        cx = x0 + 17 * mm + j * 10 * mm
                        c.setLineWidth(0.8)
                        c.circle(cx, y + 1, 3.3 * mm)
                        c.setFont(BODY, 7.5)
                        c.drawCentredString(cx, y - 0.6, letter)
                    cx = x0 + 17 * mm + 4 * 10 * mm + 2 * mm
                    c.setDash(1.5, 1.5)
                    c.circle(cx, y + 1, 3.3 * mm)
                    c.setDash()
                    c.setFont(BODY, 8)
                    c.drawCentredString(cx, y - 0.8, "?")
    b = Bubbles(n)
    b.height = 30 * mm
    # give the flowable the remaining frame height
    class Sheet(Bubbles):
        def wrap(self, aw, ah):
            self.height = ah - 4
            return aw, self.height
    sh.append(Sheet(n))
    story += sh
    doc.build(story)


def balanced_positions(n, seed):
    seq = [i % 4 for i in range(n)]
    random.Random(seed).shuffle(seq)
    return seq

# ---- Test A: place correct choice at balanced positions
a_items, a_key = [], []
pos = balanced_positions(len(TEST_A), 77)
for (q, ch, note), p in zip(TEST_A, pos):
    correct, wrongs = ch[0], ch[1:]
    order = wrongs[:p] + [correct] + wrongs[p:]
    a_items.append((q, order, "ABCD"[p]))
    a_key.append(("ABCD"[p], note, correct))
b_items = [(q, ch, a) for q, ch, a, _ in TEST_B]
b_key = [(a, note, ch["ABCD".index(a)]) for q, ch, a, note in TEST_B]

def place_items(items, seed):
    out, key = [], []
    for (q, ch, note), p in zip(items, balanced_positions(len(items), seed)):
        out.append((q, ch[1:p + 1] + [ch[0]] + ch[p + 1:], "ABCD"[p]))
        key.append(("ABCD"[p], note, ch[0]))
    return out, key

c_order = list(TEST_C)
random.Random(2410).shuffle(c_order)  # mix types so neighbouring items don't give each other away
c_items, c_key = place_items(c_order, 1024)
build_test("C", "Practice Test C (Structure Around the Blank)", c_items, "P5_TestC_structure.pdf")
if "--only-c" not in sys.argv:
    build_test("A", "Practice Test A (Weakness Focus)", a_items, "P5_TestA_weakness.pdf")
    build_test("B", "Practice Test B (Mixed Review)", b_items, "P5_TestB_mixed.pdf")

# ---- answer key (Korean)
def key_pdf(fname="P5_Answers_and_Notes.pdf", sets=None):
    sets = sets or (("Test A (약점 집중)", a_key), ("Test B (종합)", b_key))
    doc = BaseDocTemplate(str(out_dir / fname), pagesize=A4, leftMargin=LM, rightMargin=RM,
                          topMargin=TM, bottomMargin=BM, title="TOEIC Part 5 Answer Key")
    doc.addPageTemplates([PageTemplate(id="k", frames=[Frame(LM, BM, PW - LM - RM, PH - TM - BM, id="k",
                          leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
                          onPage=lambda c, d: (c.setFont("NG", 8), c.drawCentredString(PW / 2, 9 * mm, str(d.page))))])
    h = ParagraphStyle("h", fontName="NG-B", fontSize=14, leading=19, spaceAfter=4)
    s = ParagraphStyle("s", fontName="NG", fontSize=8.8, leading=12.5)
    sb = ParagraphStyle("sb", fontName="NG-B", fontSize=8.8, leading=12.5)
    sm = ParagraphStyle("sm", fontName="NG", fontSize=9, leading=13)
    story = [Paragraph("정답과 한 줄 규칙", h),
             Paragraph("채점 전에 보지 마. 틀린 문제는 번호만 골라서 나한테 보내줘. 왜 그 답을 골랐는지부터 같이 보자.", sm),
             Spacer(1, 6)]
    for label, key in sets:
        story.append(Paragraph(label, ParagraphStyle("h2", fontName="NG-B", fontSize=11.5, leading=16, spaceBefore=8, spaceAfter=4)))
        line = "  ".join(f"{101 + i}{k[0]}" for i, k in enumerate(key))
        story.append(Paragraph(f"정답표: {line}", s))
        story.append(Spacer(1, 5))
        rows = [[Paragraph("No.", sb), Paragraph("정답", sb), Paragraph("규칙", sb)]]
        for i, (letter, note, word) in enumerate(key):
            rows.append([Paragraph(str(101 + i), s), Paragraph(f"({letter}) {word}", s), Paragraph(note, s)])
        t = Table(rows, colWidths=[12 * mm, 38 * mm, PW - LM - RM - 50 * mm], repeatRows=1)
        t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.black), ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.black),
                               ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        story.append(t)
        story.append(PageBreak())
    doc.build(story[:-1])
if "--only-c" not in sys.argv:
    key_pdf()
key_pdf("P5_TestC_Answers.pdf", (("Test C (빈칸 주변 구조)", c_key),))
print("done", [p.name for p in sorted(out_dir.glob('*.pdf'))])
