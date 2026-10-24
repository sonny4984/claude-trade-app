"""Render the original practice test in t11_items.py using the page layout of a Korean TOEIC past-test book
(one RC test = printed pages 20-47, one passage set per page, side tab on odd pages).
Usage: python3 tools/make_t11.py [items_module] [test_no]  (default t11_items 11)
  -> data/workbook/RC_Test{N}.pdf, RC_Test{N}_Answers.pdf, RC_Test{N}_key.txt"""
import importlib, random, re, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Flowable,
                                FrameBreak, NextPageTemplate, PageBreak, KeepTogether)

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "tools"))
_mod = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "t11_items")
PART5, PART6, PART7 = _mod.PART5, _mod.PART6, _mod.PART7

LIB = "/usr/share/fonts/truetype/liberation/"
for name, f in [("S", "LiberationSans-Regular"), ("S-B", "LiberationSans-Bold"), ("S-I", "LiberationSans-Italic"),
                ("S-BI", "LiberationSans-BoldItalic"), ("R", "LiberationSerif-Regular"), ("R-B", "LiberationSerif-Bold"),
                ("R-I", "LiberationSerif-Italic"), ("R-BI", "LiberationSerif-BoldItalic")]:
    pdfmetrics.registerFont(TTFont(name, LIB + f + ".ttf"))
pdfmetrics.registerFont(TTFont("DJ", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("NG", str(root / "tools/fonts/NanumGothic-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NG-B", str(root / "tools/fonts/NanumGothic-Bold.ttf")))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("S", normal="S", bold="S-B", italic="S-I", boldItalic="S-BI")
registerFontFamily("R", normal="R", bold="R-B", italic="R-I", boldItalic="R-BI")

TEST_NO = int(sys.argv[2]) if len(sys.argv) > 2 else 11
FIRST_PRINTED = 19 + 30 * (TEST_NO - 11)  # divider page number; TEST 11 = pages 20-47
PW, PH = A4
LM, RM = 54, 48
TOP, BOT = 64, 70
W = PW - LM - RM
GAP = 44
CW = (W - GAP) / 2
GRAY = colors.HexColor("#6f6f6f")
LIGHT = colors.HexColor("#e4e4e4")
MID = colors.HexColor("#bdbdbd")

def st(**k):
    k.setdefault("fontName", "S")
    return ParagraphStyle("x", **k)

Q_NUM = st(fontName="S-B", fontSize=10.4, leading=13.2, alignment=2)
Q_TXT = st(fontSize=10.4, leading=13.2)
Q_CH = st(fontSize=10.4, leading=13.0, leftIndent=17, firstLineIndent=-17)
INTRO = st(fontSize=10.4, leading=13)
SER = st(fontName="R", fontSize=10.6, leading=12.6, alignment=TA_JUSTIFY, spaceAfter=7)
SER_L = st(fontName="R", fontSize=10.6, leading=12.6, spaceAfter=7)
SANS_P = st(fontSize=10.2, leading=12.8, spaceAfter=7)

# ---------------- helpers
def clean(t):
    return re.sub(r"\[\[(.+?)\]\]", r"\1", t)

def line_of(text, style, width, word):
    """1-based line number of `word` inside the paragraph as it will be rendered."""
    p = Paragraph(clean(text), style)
    p.wrap(width, 10000)
    for i, ln in enumerate(p.blPara.lines):
        if isinstance(ln, tuple):
            words = ln[1]
        else:
            words = [getattr(w, "text", "") for w in ln.words]
        joined = " ".join(words)
        if re.search(r"\b%s\b" % re.escape(word), joined):
            return i + 1
    raise ValueError(word)

LINES = {}

def register_lines(paras, style, width):
    for t in paras:
        for w in re.findall(r"\[\[(.+?)\]\]", t):
            LINES[w] = line_of(t, style, width, w)

def place(items, seed):
    seq = [i % 4 for i in range(len(items))]
    random.Random(seed).shuffle(seq)
    out = []
    for it, p in zip(items, seq):
        if len(it) == 4:
            out.append((it[0], it[1], it[3], it[2]))
        else:
            ch = it[1]
            out.append((it[0], ch[1:p + 1] + [ch[0]] + ch[p + 1:], p, it[2]))
    return out

def q_block(num, stem, ch, width):
    rows = []
    content = []
    if stem:
        content.append(Paragraph(stem, Q_TXT))
        content.append(Spacer(1, 3))
    for k, t in enumerate(ch):
        content.append(Paragraph(f"({'ABCD'[k]})&nbsp;{t}", Q_CH))
    t = Table([[Paragraph(f"{num}.", Q_NUM), content]], colWidths=[30, width - 30])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (0, 0), 5), ("RIGHTPADDING", (1, 0), (1, 0), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return t

def q_two_col(qs, left=None):
    n = len(qs)
    left = left if left is not None else (n + 1) // 2
    colw = (W - 20) / 2
    L = []
    for b in qs[:left]:
        L += [q_block(*b, colw), Spacer(1, 11)]
    R = []
    for b in qs[left:]:
        R += [q_block(*b, colw), Spacer(1, 11)]
    t = Table([[L, R or [Spacer(1, 1)]]], colWidths=[colw + 20, colw])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0)]))
    return t

def intro_line(lo, hi, what):
    return Paragraph(f"<b>Questions {lo}-{hi}</b> refer to the following {what}.", INTRO)

# ---------------- generic drawn components
class Draw(Flowable):
    """Base: subclasses build content in prepare(width) and draw in paint()."""
    def __init__(self, width=W):
        super().__init__()
        self.width = width
    def wrap(self, aw, ah):
        self.height = self.prepare()
        return self.width, self.height
    def drawOn(self, canvas, x, y, _sW=0):
        Flowable.drawOn(self, canvas, x, y, _sW)

def stack(paras, c, x, top, width):
    y = top
    for p in paras:
        w, h = p.wrap(width, 10000)
        y -= h
        p.drawOn(c, x, y)
        y -= getattr(p.style, "spaceAfter", 0) if hasattr(p, "style") else 0
    return y

def stack_h(paras, width):
    h = 0
    for p in paras:
        h += p.wrap(width, 10000)[1] + (p.style.spaceAfter if hasattr(p, "style") else 0)
    return h

class Box(Draw):
    """Bordered box (directions box, Part 6 passage, press release, ad, notice)."""
    def __init__(self, paras, width=W, pad=12, lw=0.9, top_pad=None):
        super().__init__(width)
        self.paras, self.pad, self.lw = paras, pad, lw
        self.top_pad = top_pad if top_pad is not None else pad
    def prepare(self):
        self.ih = stack_h(self.paras, self.width - 2 * self.pad)
        return self.ih + self.top_pad + self.pad - 4
    def draw(self):
        c = self.canv
        c.setLineWidth(self.lw); c.rect(0, 0, self.width, self.height)
        stack(self.paras, c, self.pad, self.height - self.top_pad, self.width - 2 * self.pad)

class PlainIndent(Draw):
    def __init__(self, paras, indent=26, width=W):
        super().__init__(width); self.paras, self.indent = paras, indent
    def prepare(self):
        return stack_h(self.paras, self.width - self.indent - 10)
    def draw(self):
        stack(self.paras, self.canv, self.indent, self.height, self.width - self.indent - 10)

class Phone(Draw):
    def __init__(self, msgs, width=300):
        super().__init__(width); self.msgs = msgs
    def prepare(self):
        self.bw = self.width - 70
        st_n = st(fontName="S-B", fontSize=10.6, leading=12.8)
        st_t = st(fontName="S", fontSize=10.6, leading=12.8)
        self.bubbles = []
        for name, time, text in self.msgs:
            ps = [Paragraph(f"{name} ({time})", st_n), Paragraph(text, st_t)]
            h = sum(p.wrap(self.bw - 16, 1000)[1] for p in ps) + 14
            self.bubbles.append((ps, h))
        return sum(h + 12 for _, h in self.bubbles) + 72
    def draw(self):
        c = self.canv
        c.setLineWidth(2.6); c.setStrokeColor(colors.black)
        c.roundRect(0, 0, self.width, self.height, 22)
        sx, sy, sw, sh = 14, 28, self.width - 28, self.height - 58
        c.setFillColor(colors.HexColor("#a9a9a9")); c.setLineWidth(1.4)
        c.roundRect(sx, sy, sw, sh, 8, fill=1)
        c.setFillColor(colors.black); c.circle(self.width - 18, self.height - 16, 3.4, fill=1, stroke=0)
        y = sy + sh - 12
        for i, (ps, h) in enumerate(self.bubbles):
            bx = sx + 12 if i % 2 == 0 else sx + sw - 12 - self.bw
            y -= h
            c.setFillColor(colors.white); c.setStrokeColor(colors.HexColor("#999999")); c.setLineWidth(0.6)
            c.roundRect(bx, y, self.bw, h, 9, fill=1, stroke=1)
            p = c.beginPath()
            if i % 2 == 0:
                p.moveTo(bx + 4, y + 10); p.lineTo(bx - 12, y - 6); p.lineTo(bx + 22, y + 1)
            else:
                p.moveTo(bx + self.bw - 4, y + 10); p.lineTo(bx + self.bw + 12, y - 6); p.lineTo(bx + self.bw - 22, y + 1)
            c.setFillColor(colors.white); c.drawPath(p, fill=1, stroke=0)
            c.setFillColor(colors.black)
            yy = y + h - 7
            for para in ps:
                ww, hh = para.wrap(self.bw - 16, 1000); yy -= hh; para.drawOn(c, bx + 8, yy)
            y -= 12

def email_hdr_paras(hdr, font):
    return [(Paragraph(k, st(fontName=font, fontSize=10.2, leading=12)), Paragraph(v, st(fontName="R", fontSize=10.2, leading=12)))
            for k, v in hdr]

class EmailTitle(Draw):
    """'*E-mail*' window: title bar with double rules, boxed header fields, framed body."""
    def __init__(self, hdr, body, width=W - 8):
        super().__init__(width); self.hdr, self.body_t = hdr, body
    def prepare(self):
        self.bodyw = self.width - 64
        self.paras = [Paragraph(clean(t), SER) for t in self.body_t]
        register_lines(self.body_t, SER, self.bodyw)
        self.bh = stack_h(self.paras, self.bodyw) + 14
        self.hh = 20 * len(self.hdr) + 10
        return 26 + self.hh + self.bh + 18
    def draw(self):
        c = self.canv; w, h = self.width, self.height
        c.setFillColor(LIGHT); c.setStrokeColor(colors.HexColor("#555555")); c.setLineWidth(1)
        c.rect(0, 0, w, h, fill=1)
        ty = h - 13
        c.setLineWidth(0.7)
        for dy in (-3, 0, 3):
            c.line(8, ty + dy, w / 2 - 50, ty + dy); c.line(w / 2 + 50, ty + dy, w - 8, ty + dy)
        c.setFillColor(colors.white); c.rect(w / 2 - 50, ty - 7, 100, 14, fill=1, stroke=0)
        c.setFillColor(colors.black); c.setFont("S-B", 11.5); c.drawCentredString(w / 2, ty - 4, "*E-mail*")
        c.setFillColor(colors.white); c.rect(12, ty - 5, 10, 10, fill=1); c.rect(w - 22, ty - 5, 10, 10, fill=1)
        y = h - 32
        for k, v in self.hdr:
            c.setFillColor(colors.black); c.setFont("R", 10.4); c.drawString(28, y - 11, k)
            c.setFillColor(colors.white); c.rect(118, y - 15, w - 146, 15, fill=1)
            c.setFillColor(colors.black); c.drawString(124, y - 11.5, v.replace("&lt;", "<").replace("&gt;", ">"))
            y -= 20
        by = y - 6
        c.setFillColor(colors.white); c.rect(22, 10, w - 44, by - 10, fill=1)
        stack(self.paras, c, 32, by - 10, self.bodyw)

class EmailGray(Draw):
    """Gray label cells + boxed values, framed body with scrollbar."""
    def __init__(self, hdr, body, width=W - 8):
        super().__init__(width); self.hdr, self.body_t = hdr, body
    def prepare(self):
        self.bodyw = self.width - 66
        self.paras = [Paragraph(clean(t), SER) for t in self.body_t]
        register_lines(self.body_t, SER, self.bodyw)
        self.bh = stack_h(self.paras, self.bodyw) + 16
        return 22 * len(self.hdr) + 18 + self.bh + 10
    def draw(self):
        c = self.canv; w, h = self.width, self.height
        c.setStrokeColor(colors.HexColor("#555555")); c.setLineWidth(1.2); c.setFillColor(LIGHT)
        c.rect(0, 0, w, h, fill=1)
        y = h - 10
        for k, v in self.hdr:
            c.setFillColor(colors.HexColor("#cfcfcf")); c.setLineWidth(0.8); c.rect(12, y - 17, 92, 16, fill=1)
            c.setFillColor(colors.black); c.setFont("S-B", 10.4); c.drawString(17, y - 13, k)
            c.setFillColor(colors.white); c.rect(112, y - 17, w - 130, 16, fill=1)
            c.setFillColor(colors.black); c.setFont("R", 10.2); c.drawString(118, y - 13, v.replace("&lt;", "<").replace("&gt;", ">"))
            y -= 22
        by = y - 4
        c.setFillColor(colors.white); c.rect(12, 8, w - 24, by - 8, fill=1)
        c.setFillColor(LIGHT); c.rect(w - 26, 8, 14, by - 8, fill=1)
        c.setFillColor(colors.HexColor("#9a9a9a")); c.rect(w - 24, by - 14, 10, 10, fill=1); c.rect(w - 24, 10, 10, 10, fill=1)
        c.setFillColor(colors.black)
        stack(self.paras, c, 22, by - 10, self.bodyw)

class ArticleNarrow(Draw):
    def __init__(self, body, title=None, colw=212):
        super().__init__(W); self.body_t, self.title, self.colw = body, title, colw
    def prepare(self):
        self.tp = Paragraph(self.title, st(fontName="R-B", fontSize=17, leading=19.5, alignment=TA_CENTER)) if self.title else None
        self.paras = [Paragraph(clean(t), SER) for t in self.body_t]
        register_lines(self.body_t, SER, self.colw)
        self.th = self.tp.wrap(self.colw, 1000)[1] + 6 if self.tp else 0
        return self.th + stack_h(self.paras, self.colw) + 10
    def draw(self):
        c = self.canv; x0 = (W - self.colw) / 2 + 20
        y = self.height
        if self.tp:
            hh = self.tp.wrap(self.colw, 1000)[1]; self.tp.drawOn(c, x0, y - hh); y -= self.th
        c.setLineWidth(2.2); c.line(x0, y, x0 + self.colw, y)
        yb = stack(self.paras, c, x0, y - 4, self.colw)
        c.line(x0, 2, x0 + self.colw, 2)

class ArticleTwoCol(Draw):
    def __init__(self, title, byline, col1, col2):
        super().__init__(W); self.title, self.byline, self.c1, self.c2 = title, byline, col1, col2
        self.cw = (W - 46) / 2
    def prepare(self):
        self.tp = Paragraph(self.title, st(fontName="S-B", fontSize=12.6, leading=15))
        self.bp = Paragraph(self.byline, st(fontName="R", fontSize=10.6, leading=13, spaceAfter=6))
        self.p1 = [Paragraph(clean(t), SER) for t in self.c1]
        self.p2 = [Paragraph(clean(t), SER) for t in self.c2]
        register_lines(self.c1, SER, self.cw)
        h1 = self.tp.wrap(self.cw, 1000)[1] + 4 + self.bp.wrap(self.cw, 100)[1] + 6 + stack_h(self.p1, self.cw)
        h2 = stack_h(self.p2, self.cw)
        return max(h1, h2) + 4
    def draw(self):
        c = self.canv; x1 = 18; x2 = x1 + self.cw + 14
        y = self.height
        h = self.tp.wrap(self.cw, 1000)[1]; self.tp.drawOn(c, x1, y - h); y -= h + 4
        h = self.bp.wrap(self.cw, 100)[1]; self.bp.drawOn(c, x1, y - h); y -= h + 6
        stack(self.p1, c, x1, y, self.cw)
        stack(self.p2, c, x2, self.height, self.cw)

class Chat(Draw):
    def __init__(self, msgs):
        super().__init__(W - 8); self.msgs = msgs
    def prepare(self):
        self.tw = self.width - 70
        self.paras = []
        for name, time, text in self.msgs:
            self.paras.append(Paragraph(f"<b>{name} ({time})</b><br/>{text}", st(fontSize=10.6, leading=13.4, spaceAfter=9)))
        return stack_h(self.paras, self.tw) + 60
    def draw(self):
        c = self.canv; w, h = self.width, self.height
        c.setLineWidth(1); c.rect(0, 0, w, h)
        c.line(0, h - 32, w, h - 32); c.line(0, 18, w, 18)
        c.line(w - 16, 18, w - 16, h - 32)
        c.setFillColor(colors.black); c.circle(22, h - 16, 11, fill=1)
        c.setFillColor(colors.white)
        for dx in (-5, 0, 5):
            c.circle(22 + dx, h - 13 + (2 if dx == 0 else 0), 2.6, fill=1, stroke=0)
        c.setFillColor(colors.black)
        c.rect(w - 15, h - 45, 13, 12); c.rect(w - 15, 19, 13, 12); c.rect(1, 2, 13, 14); c.rect(w - 15, 2, 14, 14)
        c.setFont("DJ", 7)
        c.drawCentredString(w - 8.5, h - 42, "▲"); c.drawCentredString(w - 8.5, 22, "▼")
        c.drawCentredString(7.5, 6, "◀"); c.drawCentredString(w - 8, 6, "▶")
        stack(self.paras, c, 26, h - 44, self.tw)

class Form(Draw):
    def __init__(self, title, intro, rows):
        super().__init__(W - 10); self.title, self.intro, self.rows = title, intro, rows
    def prepare(self):
        self.tp = Paragraph(self.title, st(fontName="R-B", fontSize=15, leading=18, alignment=TA_CENTER))
        self.ip = Paragraph(self.intro, st(fontName="R", fontSize=11, leading=13.4))
        cw = self.width - 28
        data = [[Paragraph(k, st(fontName="R", fontSize=11, leading=13.4)), Paragraph(v, st(fontName="R", fontSize=11, leading=13.4))]
                for k, v in self.rows]
        self.tbl = Table(data, colWidths=[86, cw - 86])
        self.tbl.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.6, colors.black), ("INNERGRID", (0, 0), (-1, -1), 0.6, colors.black),
                                      ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                                      ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        self.th = self.tp.wrap(cw, 100)[1]; self.ih = self.ip.wrap(cw, 1000)[1]; self.tb = self.tbl.wrap(cw, 1000)[1]
        return self.th + self.ih + self.tb + 36
    def draw(self):
        c = self.canv; w, h = self.width, self.height; cw = w - 28
        c.setLineWidth(1); c.rect(0, 0, w, h)
        y = h - 10 - self.th; self.tp.drawOn(c, 14, y)
        c.setLineWidth(0.6); c.line(0, y - 4, w, y - 4)
        y -= 8 + self.ih; self.ip.drawOn(c, 14, y)
        y -= 8 + self.tb; self.tbl.drawOn(c, 14, y)

class Review(Draw):
    def __init__(self, site, stars, body, quote=None, title=None):
        super().__init__(W - 8); self.site, self.stars, self.body_t, self.quote, self.title = site, stars, body, quote, title
    def prepare(self):
        self.tw = self.width - 60
        ps = []
        if self.title:
            ps.append(Paragraph(f"<b>{self.title}</b>", st(fontName="R", fontSize=11.5, leading=14, spaceAfter=8)))
        if not self.site.startswith("http"):
            ps.append(Paragraph(f"<b>{self.site}</b>", st(fontName="S", fontSize=11, leading=14, spaceAfter=6)))
        ps.append(Paragraph("★" * self.stars + "☆" * (5 - self.stars), st(fontName="DJ", fontSize=11.5, leading=14, spaceAfter=4)))
        if self.quote:
            ps.append(Paragraph(f"<i>{self.quote}</i>", st(fontName="S-I", fontSize=10.6, leading=13, spaceAfter=7)))
        for t in self.body_t:
            ps.append(Paragraph(t, st(fontName="R" if self.site.startswith("http") else "S", fontSize=10.6, leading=13,
                                      leftIndent=0 if self.site.startswith("http") else 14, spaceAfter=7)))
        self.ps = ps
        return stack_h(ps, self.tw) + 46
    def draw(self):
        c = self.canv; w, h = self.width, self.height
        c.setLineWidth(1); c.setFillColor(LIGHT); c.rect(0, 0, w, h, fill=1)
        c.setFillColor(colors.white); c.rect(6, 6, w - 26, h - 34, fill=1)
        if self.site.startswith("http"):
            c.roundRect(12, h - 24, w - 60, 16, 8, fill=1)
            c.setFillColor(colors.black); c.setFont("S", 10); c.drawString(22, h - 19.5, self.site)
        c.setFillColor(MID); c.rect(w - 18, 6, 12, h - 34, fill=1)
        c.setFillColor(colors.black); c.setFont("DJ", 6.5)
        c.drawCentredString(w - 12, h - 37, "▲"); c.drawCentredString(w - 12, 9, "▼")
        stack(self.ps, c, 22, h - 40, self.tw)

class WebTable(Draw):
    def __init__(self, url, title, rows, after):
        super().__init__(W - 8); self.url, self.title, self.rows, self.after = url, title, rows, after
    def prepare(self):
        self.tw = self.width - 40
        self.tp = Paragraph(f"<b>{self.title}</b>", st(fontName="S", fontSize=12, leading=15, alignment=TA_CENTER))
        data = [[Paragraph(("<b>%s</b>" % c) if i == 0 else c, st(fontSize=10.4, leading=12.6)) for c in r] for i, r in enumerate(self.rows)]
        ws = [0.18, 0.16, 0.42, 0.24]
        self.tbl = Table(data, colWidths=[self.tw * x for x in ws])
        self.tbl.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.6, colors.black), ("BACKGROUND", (0, 0), (-1, 0), LIGHT)]))
        self.ap = [Paragraph(t, SANS_P) for t in self.after]
        return 34 + self.tp.wrap(self.tw, 100)[1] + 10 + self.tbl.wrap(self.tw, 1000)[1] + 10 + stack_h(self.ap, self.tw) + 6
    def draw(self):
        c = self.canv; w, h = self.width, self.height
        c.setLineWidth(1); c.setFillColor(LIGHT); c.rect(0, 0, w, h, fill=1)
        c.setFillColor(colors.white); c.rect(6, 6, w - 12, h - 30, fill=1)
        c.roundRect(12, h - 21, w - 70, 14, 7, fill=1)
        c.setFillColor(colors.black); c.setFont("S", 9.6); c.drawString(22, h - 17, self.url)
        y = h - 34 - self.tp.wrap(self.tw, 100)[1]; self.tp.drawOn(c, 20, y)
        th = self.tbl.wrap(self.tw, 1000)[1]; y -= 10 + th; self.tbl.drawOn(c, 20, y)
        stack(self.ap, c, 20, y - 10, self.tw)

def _scrollbar(c, x, y0, y1):
    c.setFillColor(LIGHT); c.rect(x, y0, 14, y1 - y0, fill=1)
    c.setFillColor(colors.HexColor("#9a9a9a")); c.rect(x + 2, y1 - 12, 10, 10, fill=1); c.rect(x + 2, y0 + 2, 10, 10, fill=1)
    c.setFillColor(colors.black)

def _clip(c, x, y):
    # small paper-clip glyph for "Attachment:" lines
    c.saveState(); c.setLineWidth(0.8)
    c.roundRect(x, y - 1, 5, 11, 2.5); c.roundRect(x + 1.4, y + 1, 2.2, 7, 1.1)
    c.restoreState()

class EmailClassic(Draw):
    """'E-Mail Message' window: triple rules with centred label, unboxed header lines, framed body."""
    def __init__(self, hdr, body, width=W - 8):
        super().__init__(width); self.hdr, self.body_t = hdr, body
    def prepare(self):
        self.bodyw = self.width - 60
        self.paras = [Paragraph(clean(t), SER) for t in self.body_t]
        register_lines(self.body_t, SER, self.bodyw)
        self.bh = stack_h(self.paras, self.bodyw) + 16
        self.hh = 13 * len(self.hdr) + 14
        return 20 + self.hh + 10 + self.bh + 10
    def draw(self):
        c = self.canv; w, h = self.width, self.height
        c.setStrokeColor(colors.HexColor("#555555")); c.setLineWidth(1); c.setFillColor(LIGHT); c.rect(0, 0, w, h, fill=1)
        ty = h - 9; c.setLineWidth(0.6)
        for dy in (-3, 0, 3):
            c.line(4, ty + dy, w - 4, ty + dy)
        c.setFillColor(LIGHT); c.rect(w / 2 - 46, ty - 6, 92, 12, fill=1, stroke=0)
        c.setFillColor(colors.black); c.setFont("S", 8.6); c.drawCentredString(w / 2, ty - 3, "E-Mail Message")
        top = h - 20; hb = top - self.hh
        c.setFillColor(colors.white); c.setLineWidth(0.8); c.rect(10, hb, w - 30, self.hh, fill=1)
        c.setLineWidth(2); c.line(10, hb, 10, top); c.line(10, top, w - 20, top); c.setLineWidth(0.8)
        y = top - 15
        for k, v in self.hdr:
            c.setFillColor(colors.black); c.setFont("R", 10.4); c.drawString(22, y, k)
            vx = 100
            if k.lower().startswith("attachment"):
                _clip(c, vx, y); vx += 9
            c.drawString(vx, y, v.replace("&lt;", "<").replace("&gt;", ">")); y -= 13
        by = hb - 8
        c.setFillColor(colors.white); c.rect(10, 8, w - 30, by - 8, fill=1)
        c.setLineWidth(2); c.line(10, 8, 10, by); c.line(10, by, w - 20, by)
        c.setFillColor(colors.black)
        stack(self.paras, c, 24, by - 10, self.bodyw)

class Memo(Draw):
    """Boxed memo with a black 'MEMO' label and tab-aligned header."""
    def __init__(self, hdr, body, width=W - 30):
        super().__init__(width); self.hdr, self.body_t = hdr, body
    def prepare(self):
        self.bodyw = self.width - 70
        self.paras = [Paragraph(clean(t), SER) for t in self.body_t]
        register_lines(self.body_t, SER, self.bodyw)
        return 40 + 14 * len(self.hdr) + 12 + stack_h(self.paras, self.bodyw) + 10
    def draw(self):
        c = self.canv; w, h = self.width, self.height
        c.setLineWidth(1); c.rect(0, 0, w, h)
        c.setFillColor(colors.black); c.rect(36, h - 38, 76, 26, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont("S-B", 15); c.drawCentredString(74, h - 31, "MEMO")
        c.setFillColor(colors.black); y = h - 56
        for k, v in self.hdr:
            c.setFont("R", 10.6); c.drawString(36, y, k); c.drawString(100, y, v); y -= 14
        stack(self.paras, c, 36, y - 4, self.bodyw)

class WebTabs(Draw):
    """Web page: URL bar, tab row with the active tab bold, white page with scrollbar."""
    def __init__(self, url, tabs, active, body, title=None, width=W - 8):
        super().__init__(width); self.url, self.tabs, self.active, self.body_t, self.title = url, tabs, active, body, title
    def prepare(self):
        self.tw = self.width - 70
        ps = []
        if self.title:
            ps.append(Paragraph(f"<b>{self.title}</b>", st(fontName="S", fontSize=11.2, leading=14, spaceAfter=8)))
        for t in self.body_t:
            if t.startswith("• "):
                ps.append(Paragraph("•&nbsp;&nbsp;" + clean(t[2:]), st(fontSize=10.4, leading=13, leftIndent=12, firstLineIndent=-10, spaceAfter=5)))
            else:
                ps.append(Paragraph(clean(t), SANS_P))
        register_lines([t for t in self.body_t if not t.startswith("• ")], SANS_P, self.tw)
        self.ps = ps
        return 34 + 22 + 12 + stack_h(ps, self.tw) + 16
    def draw(self):
        c = self.canv; w, h = self.width, self.height
        c.setLineWidth(2.2); c.setFillColor(LIGHT); c.rect(0, 0, w, h, fill=1)
        c.setLineWidth(0.9); c.setFillColor(colors.white); c.roundRect(14, h - 26, w - 40, 17, 8, fill=1)
        c.setFillColor(colors.black); c.setFont("S", 9.8); c.drawString(24, h - 21, self.url)
        ty = h - 52; n = len(self.tabs); tabw = (w - 40) / n
        c.setFillColor(colors.white); c.rect(8, 8, w - 16, ty - 8, fill=1)
        for i, t in enumerate(self.tabs):
            x = 8 + i * tabw
            c.setFillColor(colors.white); c.rect(x, ty, tabw, 20, fill=1)
            if i == self.active:
                c.setStrokeColor(colors.white); c.line(x + 1, ty, x + tabw - 1, ty); c.setStrokeColor(colors.black)
            c.setFillColor(colors.black); c.setFont("S-B" if i == self.active else "S", 10.2)
            c.drawCentredString(x + tabw / 2, ty + 6, t)
        _scrollbar(c, w - 26, 9, ty + 20)
        stack(self.ps, c, 24, ty - 14, self.tw)

class TableBox(Draw):
    """Title + optional intro + ruled table + notes, in a box (schedules, price lists, reports, receipts)."""
    def __init__(self, title, rows, widths, intro=None, after=None, serif=True, width=W - 20):
        super().__init__(width)
        self.title, self.rows, self.widths, self.intro, self.after, self.serif = title, rows, widths, intro or [], after or [], serif
    def prepare(self):
        f = "R" if self.serif else "S"
        self.tw = self.width - 36
        self.tp = Paragraph(f"<b>{self.title}</b>", st(fontName=f, fontSize=13.5, leading=16.5, alignment=TA_CENTER, spaceAfter=8))
        self.ip = [Paragraph(t, st(fontName=f, fontSize=10.6, leading=13.2, spaceAfter=6)) for t in self.intro]
        cs = st(fontName=f, fontSize=10.4, leading=12.6)
        data = [[Paragraph(("<b>%s</b>" % x) if i == 0 else x, cs) for x in r] for i, r in enumerate(self.rows)]
        self.tbl = Table(data, colWidths=[self.tw * x for x in self.widths])
        self.tbl.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), 1.4, colors.black), ("LINEBELOW", (0, 0), (-1, 0), 0.9, colors.black),
                                      ("LINEBELOW", (0, 1), (-1, -1), 0.4, colors.black), ("LINEBELOW", (0, -1), (-1, -1), 1.4, colors.black),
                                      ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        self.ap = [Paragraph(t, st(fontName=f, fontSize=10.4, leading=13, spaceAfter=5)) for t in self.after]
        return (24 + stack_h([self.tp], self.tw) + stack_h(self.ip, self.tw) + self.tbl.wrap(self.tw, 2000)[1] + 8
                + stack_h(self.ap, self.tw))
    def draw(self):
        c = self.canv; w, h = self.width, self.height
        c.setLineWidth(1.2); c.rect(0, 0, w, h)
        y = stack([self.tp] + self.ip, c, 18, h - 12, self.tw)
        th = self.tbl.wrap(self.tw, 2000)[1]; self.tbl.drawOn(c, 18, y - th)
        stack(self.ap, c, 18, y - th - 8, self.tw)

def passage(p):
    k = p["kind"]
    if k == "letter_plain":
        return PlainIndent([Paragraph(t, SER) for t in p["body"]])
    if k == "phone":
        return Phone(p["msgs"])
    if k == "email_title":
        return EmailTitle(p["hdr"], p["body"])
    if k == "email_gray":
        return EmailGray(p["hdr"], p["body"])
    if k == "article_narrow":
        return ArticleNarrow(p["body"], p.get("title"))
    if k == "article_two_col":
        return ArticleTwoCol(p["title"], p["byline"], p["col1"], p["col2"])
    if k == "chat":
        return Chat(p["msgs"])
    if k == "ad_box":
        ps = [Paragraph(p["title"], st(fontName="R-B", fontSize=15, leading=18, alignment=TA_CENTER, spaceAfter=8))]
        ps += [Paragraph(t, st(fontName="R", fontSize=11.4, leading=14, alignment=TA_JUSTIFY, spaceAfter=6)) for t in p["body"]]
        ps.append(Paragraph(f"<b>{p['list_title']}</b>", st(fontName="R", fontSize=11.4, leading=14, spaceAfter=2)))
        ps += [Paragraph(f"•&nbsp;&nbsp;{b}", st(fontName="R", fontSize=11.4, leading=14, leftIndent=26, firstLineIndent=-10))
               for b in p["bullets"]]
        ps.append(Spacer(1, 6))
        ps += [Paragraph(t, st(fontName="R", fontSize=11.4, leading=14, spaceAfter=6)) for t in p["after"]]
        return Box(ps, width=W - 20, pad=18)
    if k == "tips":
        ps = [Paragraph(f"<i>{p['title']}</i>", st(fontName="R-I", fontSize=12, leading=15, spaceAfter=8))]
        ps += [Paragraph(t, SER) for t in p["body"]]
        return PlainIndent(ps, indent=26)
    if k == "press":
        pst = st(fontName="R", fontSize=10.8, leading=13.2, alignment=TA_JUSTIFY, spaceAfter=7)
        ps = [Paragraph(clean(t), pst) for t in p["body"]]
        register_lines(p["body"], pst, W - 40 - 52)
        return Box(ps, width=W - 40, pad=26, top_pad=20)
    if k == "ad_plain":
        ps = [Paragraph(f"<b>{p['title']}</b>", st(fontName="R", fontSize=11, leading=14, alignment=TA_CENTER, spaceAfter=8))]
        ps += [Paragraph(t, st(fontName="R", fontSize=10.4, leading=13, alignment=TA_JUSTIFY, spaceAfter=7)) for t in p["body"]]
        return Box(ps, width=W - 40, pad=22, top_pad=12)
    if k == "form":
        return Form(p["title"], p["intro"], p["rows"])
    if k == "review":
        return Review(p["site"], p["stars"], p["body"], p.get("quote"), p.get("title"))
    if k == "web_table":
        return WebTable(p["url"], p["title"], p["rows"], p["after"])
    if k == "notice_box":
        ps = [Paragraph(f"<b>{p['title']}</b>", st(fontName="R", fontSize=11.5, leading=14, alignment=TA_CENTER, spaceAfter=8))]
        ps += [Paragraph(t, st(fontName="R", fontSize=10.8, leading=13.2, alignment=TA_JUSTIFY, spaceAfter=7)) for t in p["body"]]
        return Box(ps, width=W - 30, pad=22, top_pad=12)
    if k == "email_classic":
        return EmailClassic(p["hdr"], p["body"])
    if k == "memo":
        return Memo(p["hdr"], p["body"])
    if k == "web_tabs":
        return WebTabs(p["url"], p["tabs"], p.get("active", 0), p["body"], p.get("title"))
    if k == "table_box":
        return TableBox(p["title"], p["rows"], p["widths"], p.get("intro"), p.get("after"), p.get("serif", True))
    raise ValueError(k)

class Centered(Flowable):
    def __init__(self, f):
        super().__init__(); self.f = f
    def wrap(self, aw, ah):
        w, h = self.f.wrap(aw, ah); self.fw = w; return aw, h
    def draw(self):
        self.f.drawOn(self.canv, (W - self.fw) / 2, 0)

# ---------------- page decoration
state = {"last": False}

def printed(canvas):
    return canvas.getPageNumber() + FIRST_PRINTED - 1

def deco(c, doc):
    n = printed(c)
    c.saveState()
    if n % 2 == 0:
        c.setFont("S-B", 10.5); c.drawString(LM, 40, str(n))
    else:
        tab_top = PH - 72
        c.setFillColor(GRAY); c.rect(PW - 30, tab_top - 64, 30, 64, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont("S-B", 9)
        c.saveState(); c.translate(PW - 19, tab_top - 10); c.rotate(-90); c.drawString(0, 0, "TEST"); c.restoreState()
        c.circle(PW - 15, tab_top - 48, 8.5, fill=1, stroke=0)
        c.setFillColor(GRAY); c.setFont("S-B", 8.8 if TEST_NO > 9 else 10)
        c.drawCentredString(PW - 15, tab_top - 51.2, str(TEST_NO))
        c.setFillColor(colors.black)
        if not state["last"]:
            c.setFont("S-BI", 8.2); c.drawString(PW - RM - 160, 68, "GO ON TO THE NEXT PAGE")
            c.setLineWidth(2.6); c.line(PW - RM - 160, 60, PW - RM - 12, 60)
            p = c.beginPath(); p.moveTo(PW - RM - 14, 64); p.lineTo(PW - RM, 60); p.lineTo(PW - RM - 14, 56); p.close()
            c.drawPath(p, fill=1, stroke=0)
        c.setFont("S", 9); c.drawRightString(PW - RM - 20, 40, f"TEST {TEST_NO}")
        c.setFont("S-B", 10.5); c.drawRightString(PW - RM, 40, str(n))
    c.restoreState()

def divider(c, doc):
    c.saveState()
    c.setFillColor(colors.HexColor("#f7f4ee")); c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#ece7dd")); c.setFont("S-B", 260); c.drawCentredString(PW / 2 + 40, PH / 2 + 60, "RC")
    c.setFillColor(colors.white); c.rect(PW / 2 - 160, PH / 2 - 120, 330, 150, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#333333")); c.setFont("NG-B", 30); c.drawString(PW / 2 - 140, PH / 2 - 55, "실전 TEST")
    c.setFont("S-B", 84); c.drawString(PW / 2 + 40, PH / 2 - 80, f"{TEST_NO}")
    c.setLineWidth(0.8); c.line(PW / 2 - 150, PH / 2 - 20, PW / 2 + 30, PH / 2 - 20); c.line(PW / 2 - 150, PH / 2 - 75, PW / 2 + 30, PH / 2 - 75)
    c.setFont("NG", 9); c.setFillColor(colors.HexColor("#666666"))
    c.drawCentredString(PW / 2, 80, "개인 학습용으로 새로 작성한 연습 문제입니다. 실제 기출 문항이 아닙니다.")
    c.restoreState()

def register_cb(c, doc):
    c.setNamedCB("blanknum", _blank_number)

def sheet(c, doc):
    deco(c, doc)

doc = BaseDocTemplate(str(root / f"data/workbook/RC_Test{TEST_NO}.pdf"), pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TOP,
                      bottomMargin=BOT, title=f"RC Practice TEST {TEST_NO}", author="")
full = Frame(LM, BOT, W, PH - TOP - BOT, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="full")
HDR = 238
p5a = [Frame(LM, PH - TOP - HDR, W, HDR, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="hdr"),
       Frame(LM, BOT, CW, PH - TOP - HDR - BOT, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="l1"),
       Frame(LM + CW + GAP, BOT, CW, PH - TOP - HDR - BOT, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="r1")]
p5b = [Frame(LM, BOT, CW, PH - TOP - BOT, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="l2"),
       Frame(LM + CW + GAP, BOT, CW, PH - TOP - BOT, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="r2")]
doc.addPageTemplates([PageTemplate(id="div", frames=[full], onPage=divider),
                      PageTemplate(id="p5a", frames=p5a, onPageEnd=deco),
                      PageTemplate(id="p5b", frames=p5b, onPageEnd=deco),
                      PageTemplate(id="full", frames=[full], onPage=lambda c, d: register_cb(c, d), onPageEnd=deco)])

key = []
B12 = st(fontName="S-B", fontSize=12.5, leading=15, spaceAfter=10)
DIR = st(fontSize=10.6, leading=13.6, spaceAfter=10)

story = [Spacer(1, 1), NextPageTemplate("p5a"), PageBreak()]
story.append(Box([Paragraph("READING TEST", B12),
                  Paragraph("In the Reading test, you will read a variety of texts and answer several different types of reading "
                            "comprehension questions. The entire Reading test will last 75 minutes. There are three parts, and "
                            "directions are given for each part. You are encouraged to answer as many questions as possible "
                            "within the time allowed.", DIR),
                  Paragraph("You must mark your answers on the separate answer sheet. Do not write your answers in your test "
                            "book.", DIR),
                  Paragraph("PART 5", B12),
                  Paragraph("<b>Directions:</b> A word or phrase is missing in each of the sentences below. Four answer choices "
                            "are given below each sentence. Select the best answer to complete the sentence. Then mark the letter "
                            "(A), (B), (C), or (D) on your answer sheet.", DIR)], pad=16, top_pad=16))
story += [FrameBreak()]
p5 = place(PART5, 1101 + 100 * (TEST_NO - 11))
P5_GAPS = getattr(_mod, "P5_GAPS", (14, 14, 27, 27, 31, 31))
groups = [(0, 4), (4, 8), (8, 14), (14, 20), (20, 25), (25, 30)]
for gi, (a, b) in enumerate(groups):
    for i in range(a, b):
        stem, ch, ans, note = p5[i]
        key.append((101 + i, "ABCD"[ans], ch[ans], note))
        story += [q_block(101 + i, stem, ch, CW), Spacer(1, P5_GAPS[gi])]
    if gi == 1:
        story += [NextPageTemplate("p5b"), PageBreak()]
    elif gi == 3:
        story += [NextPageTemplate("p5b"), PageBreak()]
    elif gi == 5:
        if PART6 or PART7:
            story += [NextPageTemplate("full"), PageBreak()]
    else:
        story.append(FrameBreak())

# Part 6
P6_IN = st(fontSize=10.8, leading=25, spaceAfter=7)
P6_INS = st(fontSize=10.8, leading=16, spaceAfter=8)

DASH = "-------"

def _blank_number(canv, kind, label):
    # called by <onDraw> right after the dashes: print the question number centred under them, as in the book
    info = canv._curr_tx_info
    dw = pdfmetrics.stringWidth(DASH, P6_IN.fontName, P6_IN.fontSize)
    canv.saveState(); canv.setFont("S-B", 9.6)
    canv.drawCentredString(info["cur_x"] - dw / 2, info["cur_y"] - 11.5, f"{label}.")
    canv.restoreState()


def blank(n):
    return f'{DASH}<onDraw name="blanknum" label="{n}"/>'

p6 = place([q for s in PART6 for q in s["qs"]], 1102 + 100 * (TEST_NO - 11))
qi = 0
for si, s in enumerate(PART6):
    lo = 131 + si * 4
    if si == 0:
        story += [Box([Paragraph("PART 6", B12),
                       Paragraph("<b>Directions:</b> Read the texts that follow. A word, phrase, or sentence is missing in parts of "
                                 "each text. Four answer choices for each question are given below the text. Select the best answer "
                                 "to complete the text. Then mark the letter (A), (B), (C), or (D) on your answer sheet.", DIR)],
                      pad=16, top_pad=16), Spacer(1, 22)]
    story += [intro_line(lo, lo + 3, s["intro"]), Spacer(1, 12)]
    ps = []
    if s.get("title"):
        ps.append(Paragraph(f"<i>{s['title']}</i>" if s["intro"] == "flyer" else f"<b>{s['title']}</b>",
                            st(fontSize=11, leading=15, spaceAfter=10)))
    if s.get("hdr"):
        ps.append(Paragraph("<br/>".join(f"{k}: {v}" for k, v in s["hdr"]), st(fontSize=10.8, leading=15, spaceAfter=12)))
    for t in s["body"]:
        txt = t
        for n in range(131, 147):
            txt = txt.replace("{%d}" % n, blank(n))
        # prose is set with the book's double spacing whether or not it holds a blank; address/sign-off lines stay single
        prose = "<br/>" not in txt and len(clean(txt)) > 45
        ps.append(Paragraph(txt, P6_IN if prose else P6_INS))
    story += [Centered(Box(ps, width=W - 6, pad=16, top_pad=14)), Spacer(1, 20)]
    qs = []
    for j in range(4):
        stem, ch, ans, note = p6[qi]; qi += 1
        key.append((lo + j, "ABCD"[ans], ch[ans], note))
        qs.append((lo + j, "", ch))
    story += [q_two_col(qs), PageBreak()]

# Part 7
p7 = place([q for s in PART7 for q in s["qs"]], 1103 + 100 * (TEST_NO - 11))
qi, n = 0, 147
PAGES = {  # set index -> how passages/questions are split over pages
    9: [["p0"], ["q"]], 10: [["p0", "p1"], ["q"]], 11: [["p0", "p1"], ["q"]],
    12: [["p0", "p1"], ["p2", "q"]], 13: [["p0", "p1"], ["p2", "q"]], 14: [["p0", "p1"], ["p2", "q"]],
}
for si, s in enumerate(PART7):
    if si == 0:
        story += [Box([Paragraph("PART 7", B12),
                       Paragraph("<b>Directions:</b> In this part you will read a selection of texts, such as magazine and "
                                 "newspaper articles, e-mails, and instant messages. Each text or set of texts is followed by "
                                 "several questions. Select the best answer for each question and mark the letter (A), (B), (C), "
                                 "or (D) on your answer sheet.", DIR)], pad=16, top_pad=16), Spacer(1, 22)]
    lo, hi = n, n + len(s["qs"]) - 1
    flows = [passage(p) for p in s["passages"]]
    for f in flows:
        f.wrap(W, 10000)  # lays text out now so synonym-question line numbers are known
    qs = []
    for _ in s["qs"]:
        stem, ch, ans, note = p7[qi]; qi += 1
        stem = re.sub(r"\{LINE:(\w+)\}", lambda m: str(LINES[m.group(1)]), stem)
        key.append((n, "ABCD"[ans], ch[ans], note))
        qs.append((n, stem, ch)); n += 1
    qtab = q_two_col(qs, s.get("left"))
    plan = PAGES.get(si, [["p0", "q"]])
    for pi, page in enumerate(plan):
        if pi == 0:
            story += [intro_line(lo, hi, s["intro"]), Spacer(1, 12)]
        for part in page:
            if part == "q":
                story += [Spacer(1, 10), qtab]
            else:
                story += [Centered(flows[int(part[1:])]), Spacer(1, 22)]
        if si == len(PART7) - 1 and pi == len(plan) - 1:
            break
        story.append(PageBreak())
assert n == 201 or not PART7

class Stop(Flowable):
    def wrap(self, aw, ah):
        self.aw = aw; return aw, 40
    def draw(self):
        state["last"] = True
        c = self.canv; c.setFont("S-B", 11)
        if self.aw < W * 0.8:  # Part 5-only mock: the note sits in the right column
            c.drawCentredString(self.aw / 2, 22, "Stop! This is the end of Part 5.")
            c.drawCentredString(self.aw / 2, 8, "Check your work if time remains.")
            return
        c.drawCentredString(W / 2, 22, "Stop! This is the end of the test. If you finish before time is called, you may go")
        c.drawCentredString(W / 2, 8, "back to Parts 5, 6, and 7 and check your work.")
story += [Spacer(1, 30), Stop()]

class Sheet(Flowable):
    def wrap(self, aw, ah):
        self.h = ah - 2; return aw, self.h
    def draw(self):
        c = self.canv
        c.setFont("S-B", 15); c.drawString(0, self.h - 14, f"ANSWER SHEET — TEST {TEST_NO} (Reading)")
        c.setFont("S", 9.5); c.drawString(0, self.h - 30, "Date: __________   Part 5 end: ______   Part 6 end: ______   Part 7 end: ______")
        c.setFont("NG", 9); c.drawString(0, self.h - 45, "답을 칠하고, 확신 없이 고른 문제는 오른쪽 점선 '?'도 칠하기.")
        colw = W / 4; rowh = 25
        for k in range(100):
            col, r = divmod(k, 25)
            x0 = col * colw; y = self.h - 70 - r * rowh
            c.setFont("S-B", 8.5); c.drawRightString(x0 + 22, y - 2, str(101 + k))
            for j, L in enumerate("ABCD"):
                cx = x0 + 34 + j * 18
                c.setLineWidth(0.7); c.circle(cx, y + 1, 7.4); c.setFont("S", 6.5); c.drawCentredString(cx, y - 1.2, L)
            cx = x0 + 34 + 4 * 18 + 4
            c.setDash(1.2, 1.2); c.circle(cx, y + 1, 7.4); c.setDash(); c.drawCentredString(cx, y - 1.2, "?")
story += [NextPageTemplate("full"), PageBreak(), Sheet()]

class Unlast(Flowable):
    def wrap(self, aw, ah): return 0, 0
    def draw(self): state["last"] = True
doc.build(story)

# ---------------- answer key (Korean)
kd = BaseDocTemplate(str(root / f"data/workbook/RC_Test{TEST_NO}_Answers.pdf"), pagesize=A4, leftMargin=40, rightMargin=40,
                     topMargin=40, bottomMargin=46, title=f"RC TEST {TEST_NO} Answer Key")
kd.addPageTemplates([PageTemplate(id="k", frames=[Frame(40, 46, PW - 80, PH - 86, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
                                  onPage=lambda c, d: (c.setFont("NG", 8), c.drawCentredString(PW / 2, 26, str(d.page))))])
h1 = st(fontName="NG-B", fontSize=15, leading=20, spaceAfter=4)
h2 = st(fontName="NG-B", fontSize=11.5, leading=16, spaceBefore=8, spaceAfter=4)
sm = st(fontName="NG", fontSize=8.8, leading=12.3)
smb = st(fontName="NG-B", fontSize=8.8, leading=12.3)
ks = [Paragraph(f"실전 TEST {TEST_NO} 정답과 해설", h1),
      Paragraph("채점 후 틀린 번호와 '?' 번호, Part별 끝난 시각을 보내줘. 맞은 개수로 책의 RC 환산표에 대보면 대략적인 점수대를 볼 수 있어 "
                "(새로 쓴 문제라 실제 점수와는 다를 수 있음).", sm), Spacer(1, 6)]
for label, lo, hi in (("Part 5", 101, 130), ("Part 6", 131, 146), ("Part 7", 147, 200)):
    part = [k for k in key if lo <= k[0] <= hi]
    ks += [Paragraph(label, h2), Paragraph("정답표: " + "  ".join(f"{a}{b}" for a, b, _, _ in part), sm), Spacer(1, 4)]
    rows = [[Paragraph(x, smb) for x in ("No.", "정답", "근거 · 규칙")]]
    rows += [[Paragraph(str(a), sm), Paragraph(f"({b}) {c}", sm), Paragraph(d, sm)] for a, b, c, d in part]
    t = Table(rows, colWidths=[30, 150, PW - 80 - 180], repeatRows=1)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.black), ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.black),
                           ("BACKGROUND", (0, 0), (-1, 0), LIGHT), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    ks.append(t)
kd.build(ks)
(root / f"data/workbook/RC_Test{TEST_NO}_key.txt").write_text(" ".join(f"{a}{b}" for a, b, _, _ in key), encoding="utf-8")
from collections import Counter
print("answers", Counter(k[1] for k in key), "lines", LINES)
