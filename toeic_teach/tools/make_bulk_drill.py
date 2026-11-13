"""약점 빅데이터 뭉텅이 드릴.
1) 동하 오답 기록 전부(data/progress.json 메모 + ETS Vol.3 Test 1·4 오답 + 11/10~13 해석 진단)를 같은 분류기로 유형 분류해 유형별 오답 수를 센다.
2) 지금까지 만든 문제 은행(tools/*_items.py, 새로 쓴 P5 610문항 + P6)에서 같은 유형 문항을 뽑아, 오답이 많은 유형일수록 많이 준다.
Usage: python3 tools/make_bulk_drill.py [총문항수=200] -> data/workbook/Bulk_Drill_01.pdf, data/analysis/weakness_bigdata.md"""
import glob, importlib, json, os, random, re, sys
from collections import Counter, defaultdict
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether, FrameBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
TOTAL = int(sys.argv[1]) if len(sys.argv) > 1 else 200

# 유형: (이름, 알고리즘 한 줄, 정규식)  위에서부터 먼저 걸리는 유형으로 분류
TYPES = [
    ("전치사 vs 접속사", "전/접 혼합 → 빈칸 뒤 명사구면 전치사, 문장이면 접속사", r"전치사 vs 접속사|접속사 자리|전치사 자리|뒤가 절|뒤가 명사구|despite|although|during|while\b|unless|in case|so that|whenever|except|as soon as|upon|by the time|접속부사"),
    ("동사 개수·꼬리(분사/to V)", "접속사 + 1 = 동사. 동사가 찼으면 to V / -ing / p.p. 꼬리", r"꼬리|진짜 동사|본동사|정동사|분사|후치 수식|that 생략|동사 불가|동사는 |p\.p\.|to부정사|동명사|V-ing|to V|동사원형"),
    ("수동·능동 / 시제 / 수일치", "목적어 유무로 태, 시간 표현으로 시제, 주어로 수일치", r"수동|능동|태:|시제|현재완료|과거완료|수일치|단수|복수 동사|since \+|by the time"),
    ("품사 자리: 부사", "ed·ing·형용사·동사 앞, 완전한 문장 뒤 = 부사", r"부사 자리|→ 부사|부사\."),
    ("품사 자리: 형용사", "한정사 + 형용사 + 명사 / be + 형용사", r"형용사 자리|→ 형용사|명사 앞"),
    ("품사 자리: 명사", "동사·전치사 뒤, 한정사 뒤 = 명사. 사람/사물 명사 구분", r"명사 자리|→ 명사|복합명사|목적어 → "),
    ("대명사·관계사", "뒤 구조로 격 결정. 회사 = its, 사람 = his/her", r"대명사|소유격|재귀|관계대명사|관계사|whose|whom|those|anyone"),
    ("전치사 용법·고정 전치사", "기간 for/over, 마감 by, 계속 until, 주제 on. 동사·형용사와 짝인 전치사", r"전치사 의미|전치사 용법|전치사:|\bfor \+|until|within|throughout|across|be \w+ (to|for|with|of|at|in)\b|\+ ?(from|with|to|for|of|on|at|in)\b|upon request"),
    ("어휘: 연어·짝", "동사→목적어, 형용사→명사, 명사→수식어·동사, 부사→특징 부사", r"연어|짝|어휘|collocation|= "),
]
RX = [(n, a, re.compile(p)) for n, a, p in TYPES]


def classify(note):
    for n, _, r in RX:
        if r.search(note):
            return n
    return "기타"


# ---------- 1) 오답 빅데이터
prog = json.load(open(ROOT / "data/progress.json", encoding="utf-8"))
err_notes = [h["note"] for v in prog.values() for h in v.get("history", []) if h.get("result") == "wrong" and h.get("note")]
err_notes += [  # ETS Vol.3 Test 1 (확정) · Test 4 P5·P6 (사진 판독) · 해석 진단
    "명사 앞 → 형용사 regional", "연어: 짝 and surrounding areas → city", "전치사 용법: for + 기간 현재완료", "어휘: feel confident about 짝",
    "부사 자리: When ___ applied", "어휘: doubled in volume 짝", "명사 자리: make substitutions", "대명사: 소유격 its", "어휘: a superb, 최상급 불가 짝",
    "전치사 용법: 주제 on", "명사 앞 → 형용사 diverse", "어휘: invite to a workshop 짝", "어휘: circle the village 짝", "진짜 동사: 삽입구 뒤 동사 contains",
    "전치사 용법: across all segments", "시제: 현재진행 are experiencing", "p.p. 꼬리: as advertised", "부사 자리: highly values", "명사 자리: 복합명사 productivity",
    "명사 앞 → 형용사 internal", "접속사 자리: whenever 뒤가 절", "V-ing: by sending", "어휘: fill a prescription 연어", "to V: be considered to V",
    "진짜 동사: The auction (to benefit) is", "to V: ask staff to keep", "진짜 동사: and will stick around 병렬",
]
err = Counter(classify(n) for n in err_notes)

# ---------- 2) 문제 은행
bank = defaultdict(list)
for f in sorted(glob.glob(str(ROOT / "tools/*_items.py"))):
    name = os.path.basename(f)[:-3]
    if name in ("check_items", "p5_items"):
        continue
    mod = importlib.import_module(name)
    for i, it in enumerate(getattr(mod, "PART5", [])):
        if len(it) >= 3 and len(it[1]) == 4:
            bank[classify(it[2])].append((name.replace("_items", ""), i + 101, it[0], it[1], it[2]))

names = [n for n, _, _ in TYPES]
w = {n: err[n] + 2 for n in names}  # +2: 오답이 없어도 최소량
tw = sum(w.values())
quota = {n: min(len(bank[n]), max(8, round(TOTAL * w[n] / tw))) for n in names}
rng = random.Random(1113)
sets = {}
for n in names:
    pool = bank[n][:]
    rng.shuffle(pool)
    out = []
    for src, no, stem, ch, note in pool[:quota[n]]:
        p = rng.randrange(4)
        opts = ch[1:p + 1] + [ch[0]] + ch[p + 1:]
        out.append((src, no, stem, opts, p, note))
    sets[n] = out

# ---------- 분석 문서
order = sorted(names, key=lambda n: -err[n])
md = ["# 동하 약점 빅데이터 (자동 집계)", "", f"오답 메모 {len(err_notes)}건(10/23~11/13)을 유형 분류한 결과와, 문제 은행(새로 쓴 P5 {sum(len(v) for v in bank.values())}문항)에서 뽑은 드릴 분량.", "",
      "| 순위 | 유형 | 오답 수 | 비율 | 은행 문항 | 이번 드릴 |", "|---|---|---|---|---|---|"]
tot = sum(err[n] for n in names) or 1
for i, n in enumerate(order, 1):
    md.append(f"| {i} | {n} | {err[n]} | {err[n] * 100 // tot}% | {len(bank[n])} | {len(sets[n])} |")
md += ["", f"분류되지 않은 메모(P7 독해·연계 등): {err['기타']}건. P7은 Weakness_Book_v1 6~8장과 TEST 38로 연습.", ""]
(ROOT / "data/analysis/weakness_bigdata.md").write_text("\n".join(md), encoding="utf-8")

# ---------- PDF
F = str(ROOT / "tools/fonts") + "/"
LIB = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("N", F + "NanumGothic-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NB", F + "NanumGothic-Bold.ttf"))
pdfmetrics.registerFont(TTFont("S", LIB + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("S-B", LIB + "LiberationSans-Bold.ttf"))
registerFontFamily("S", normal="S", bold="S-B", italic="S", boldItalic="S-B")
registerFontFamily("N", normal="N", bold="NB", italic="N", boldItalic="NB")
st = lambda n, f, s, l, **k: ParagraphStyle(n, fontName=f, fontSize=s, leading=l, **k)
T, H, K, KS = st("t", "NB", 18, 24), st("h", "NB", 12, 16), st("k", "N", 9.5, 14), st("ks", "N", 8.2, 11.5)
Q, QC = st("q", "S", 9.8, 12.6), st("qc", "S", 9.8, 12.2, leftIndent=15)
C, CB = st("c", "N", 8, 11), st("cb", "NB", 8, 11)
P = Paragraph
LM, TM = 15 * mm, 14 * mm
W = A4[0] - 2 * LM
GAP = 10 * mm
CW = (W - GAP) / 2
doc = BaseDocTemplate(str(ROOT / "data/workbook/Bulk_Drill_01.pdf"), pagesize=A4, leftMargin=LM, rightMargin=LM, topMargin=TM, bottomMargin=TM, title="약점 뭉텅이 드릴 01")
fr = lambda x, w_, i: Frame(x, TM, w_, A4[1] - 2 * TM, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id=i)
foot = lambda c, d: (c.setFont("N", 8), c.drawCentredString(A4[0] / 2, 7 * mm, str(d.page)))
doc.addPageTemplates([PageTemplate(id="one", frames=[fr(LM, W, "f")], onPage=foot),
                      PageTemplate(id="two", frames=[fr(LM, CW, "l"), fr(LM + CW + GAP, CW, "r")], onPage=foot)])
from reportlab.platypus import NextPageTemplate
n_all = sum(len(v) for v in sets.values())
s = [P("약점 뭉텅이 드릴 01", T), Spacer(1, 2 * mm),
     P(f"지금까지 쌓인 오답 메모 <b>{len(err_notes)}건</b>을 유형별로 세고, 많이 틀린 유형일수록 문제를 많이 넣었어. 총 <b>{n_all}문항</b> (Part 5). "
       "문제는 그동안 내가 새로 써서 TEST 11~38에 냈던 문항 은행에서 유형별로 뽑은 거라, 본 적 있는 문장도 섞여 있어. 답을 기억하는 문제는 <b>근거를 말로</b> 해보고 넘어가.", K), Spacer(1, 3 * mm)]
rows = [[P(h, CB) for h in ("순위", "유형", "오답 수", "드릴 문항", "알고리즘 한 줄")]]
algo = {n: a for n, a, _ in TYPES}
for i, n in enumerate(order, 1):
    rows.append([P(str(i), C), P(f"<b>{n}</b>", C), P(str(err[n]), C), P(str(len(sets[n])), C), P(algo[n], C)])
t = Table(rows, colWidths=[10 * mm, 42 * mm, 15 * mm, 17 * mm, W - 84 * mm])
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9d9d9")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
s += [t, Spacer(1, 3 * mm),
      P(f"※ 유형 분류는 메모의 키워드로 자동으로 한 거라 몇 건은 옆 유형으로 들어갔을 수 있어. P7 독해·연계 오답({err['기타']}건)은 여기 말고 약점 책 6~8장과 TEST 38에서 연습해.", KS),
      Spacer(1, 3 * mm), P("푸는 법", H),
      P("유형 하나를 한 번에 끝까지. 유형 이름이 곧 힌트니까 <b>알고리즘 한 줄만 적용</b>해서 빠르게 풀어 (문항당 20초). 유형 끝에 맞은 개수를 적고, 80% 아래인 유형은 다음 날 다시.", K)]
key = []
num = 0
for n in order:
    if not sets[n]:
        continue
    s += [NextPageTemplate("two"), PageBreak(), P(f"{n} ({len(sets[n])}문항)", H), P(algo[n], KS), Spacer(1, 3 * mm)]
    for src, no, stem, opts, p, note in sets[n]:
        num += 1
        key.append((num, "ABCD"[p], note, f"{src}-{no}"))
        s.append(KeepTogether([P(f"<b>{num}.</b> {stem}", Q)] + [P(f"({'ABCD'[i]}) {o}", QC) for i, o in enumerate(opts)] + [Spacer(1, 7)]))
    s.append(P("맞은 개수: ______ / " + str(len(sets[n])), KS))
s += [NextPageTemplate("one"), PageBreak(), P("정답", H)]
kr = [[P(f"<b>{a}</b> {b}", C) for a, b, _, _ in key[i:i + 10]] + [""] * (10 - len(key[i:i + 10])) for i in range(0, len(key), 10)]
kt = Table(kr, colWidths=[W / 10] * 10)
kt.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
s += [kt, Spacer(1, 4 * mm), P("해설 (틀린 번호만 찾아봐)", H)]
hr = [[P(h, CB) for h in ("번호", "정답", "근거 · 규칙", "출처")]] + [[P(str(a), C), P(b, C), P(c, C), P(d, C)] for a, b, c, d in key]
ht = Table(hr, colWidths=[11 * mm, 10 * mm, W - 39 * mm, 18 * mm], repeatRows=1)
ht.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9d9d9")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
s.append(ht)
doc.build(s)
print("errors", len(err_notes), dict(err))
print("bank", {n: len(bank[n]) for n in names + ["기타"]})
print("drill", {n: len(sets[n]) for n in names}, n_all, Counter(k[1] for k in key))
