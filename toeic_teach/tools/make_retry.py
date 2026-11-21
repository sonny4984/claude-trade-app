"""백지 재풀이 시트 (11/18 동하와 정한 루틴).
틀린 문제를 다음 날 해설 없이 다시 풀고, 이유를 한 줄로 직접 쓰게 하는 시트 + 별도 '모범 이유' 장.
Usage: python3 tools/make_retry.py <items_module> <test_no> <num,num,...> [tag]
  -> data/workbook/Retry_<tag>.pdf (문제 + 이유 칸), Retry_<tag>_check.pdf (모범 이유 한 줄)
문항 순서·선지 순서는 원래 시험지에 인쇄된 그대로 (make_t11.place와 같은 seed)."""
import importlib, re, sys, random
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle
from reportlab.lib import colors

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "tools"))
mod_name, test_no, nums = sys.argv[1], int(sys.argv[2]), [int(x) for x in sys.argv[3].split(",")]
tag = sys.argv[4] if len(sys.argv) > 4 else f"T{test_no}"
mod = importlib.import_module(mod_name)

for n, f in [("NG", "NanumGothic-Regular"), ("NG-B", "NanumGothic-Bold")]:
    pdfmetrics.registerFont(TTFont(n, str(root / f"tools/fonts/{f}.ttf")))
LIB = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("S", LIB + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("S-B", LIB + "LiberationSans-Bold.ttf"))

# reproduce the printed option order exactly as make_t11 does
NATURAL = getattr(mod, "NATURAL_KEY", False)
def place(items, seed):
    fixed = [it[3] for it in items if len(it) == 4]
    rng, pool = random.Random(seed), []
    if NATURAL:
        cap = round(0.3 * len(items)) + (2 if len(items) <= 30 else 0)
        cnt = [fixed.count(k) for k in range(4)]
        for _ in range(len(items) - len(fixed)):
            k = rng.randrange(4)
            while cnt[k] >= cap or (len(pool) >= 3 and pool[-1] == pool[-2] == pool[-3] == k):
                k = rng.randrange(4)
            pool.append(k); cnt[k] += 1
    else:
        raise SystemExit("NATURAL_KEY 모듈만 지원")
    it_pool, out = iter(pool), []
    for it in items:
        if len(it) == 4:
            out.append((it[0], it[1], it[3], it[2]))
        else:
            p = next(it_pool); ch = it[1]
            out.append((it[0], ch[1:p + 1] + [ch[0]] + ch[p + 1:], p, it[2]))
    return out

p5 = place(mod.PART5, 1101 + 100 * (test_no - 11))
REASON = getattr(mod, "RETRY_REASON", {})

H = ParagraphStyle("h", fontName="NG-B", fontSize=15, leading=20, spaceAfter=4)
SM = ParagraphStyle("s", fontName="NG", fontSize=9.5, leading=13.5, textColor=colors.HexColor("#444444"))
Q = ParagraphStyle("q", fontName="S", fontSize=11, leading=15)
CH = ParagraphStyle("c", fontName="S", fontSize=11, leading=15, leftIndent=18)
LB = ParagraphStyle("l", fontName="NG", fontSize=10, leading=14)
KB = ParagraphStyle("k", fontName="NG", fontSize=10.5, leading=15)
KBB = ParagraphStyle("kb", fontName="NG-B", fontSize=10.5, leading=15)

def line_box():
    t = Table([[Paragraph("유형:", LB), "", Paragraph("답:", LB), ""], [Paragraph("이유 한 줄:", LB), "", "", ""]],
              colWidths=[62, 250, 34, 140], rowHeights=[22, 30])
    t.setStyle(TableStyle([("LINEBELOW", (1, 0), (1, 0), 0.5, colors.grey), ("LINEBELOW", (3, 0), (3, 0), 0.5, colors.grey),
                           ("SPAN", (1, 1), (3, 1)), ("LINEBELOW", (1, 1), (3, 1), 0.5, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    return t

story = [Paragraph(f"백지 재풀이 — {tag}", H),
         Paragraph("해설·정답 보지 말고 풀기. 1) 유형 먼저(품사/동사 개수/병렬/전·접/대명사/어휘) 2) 답 3) 이유 한 줄을 '단서 → 규칙 → 답' 모양으로. "
                   "이유를 못 쓰면 아직 내 것이 아님 → X 표시. 다 쓰고 나서 check 장으로 대조.", SM), Spacer(1, 12)]
for n in nums:
    stem, ch, ans, note = p5[n - 101]
    block = [Paragraph(f"<b>{n}.</b> {stem}", Q)] + [Paragraph(f"({'ABCD'[k]}) {c}", CH) for k, c in enumerate(ch)]
    block += [Spacer(1, 6), line_box(), Spacer(1, 16)]
    story.append(KeepTogether(block))
out = root / "data/workbook"
SimpleDocTemplate(str(out / f"Retry_{tag}.pdf"), pagesize=A4, leftMargin=50, rightMargin=50, topMargin=44, bottomMargin=44,
                  title=f"Retry {tag}").build(story)

ks = [Paragraph(f"백지 재풀이 — {tag} 대조용", H),
      Paragraph("내가 쓴 이유와 비교: 단서(빈칸 옆 어디를 봤나)와 규칙 이름이 같으면 ○, 답만 맞고 이유가 다르면 △(다음 날 다시).", SM), Spacer(1, 10)]
for n in nums:
    stem, ch, ans, note = p5[n - 101]
    short = REASON.get(n) or re.sub(r"\(.*?\)\s*$", "", note)
    ks += [Paragraph(f"<b>{n}. ({'ABCD'[ans]}) {ch[ans]}</b>", KBB), Paragraph(short, KB), Spacer(1, 10)]
SimpleDocTemplate(str(out / f"Retry_{tag}_check.pdf"), pagesize=A4, leftMargin=50, rightMargin=50, topMargin=44, bottomMargin=44,
                  title=f"Retry {tag} check").build(ks)
print("ok", [f"{n}{'ABCD'[p5[n-101][2]]}" for n in nums])
