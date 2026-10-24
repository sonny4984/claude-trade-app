"""Wrong-answer rule cards (same 3-column layout as the 10/23 review pack) + 3-day check boxes,
a 2-choice retrieval quiz on the same rules, and the 7-day plan. Black & white, A4.
Sources: data/progress.json (81 wrong items up to 10/24), grouped by the rule that fixes them.
Usage: python3 tools/make_cards.py -> data/workbook/Cards_1024.pdf"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

root = Path(__file__).resolve().parent.parent
pdfmetrics.registerFont(TTFont("NG", str(root / "tools/fonts/NanumGothic-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NG-B", str(root / "tools/fonts/NanumGothic-Bold.ttf")))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("NG", normal="NG", bold="NG-B", italic="NG", boldItalic="NG-B")
W = A4[0] - 24 * mm
st = lambda **k: ParagraphStyle("x", **k)
H1 = st(fontName="NG-B", fontSize=16, leading=22, spaceAfter=4)
H2 = st(fontName="NG-B", fontSize=11.5, leading=16, spaceBefore=6, spaceAfter=3)
B = st(fontName="NG", fontSize=9.6, leading=14)
C = st(fontName="NG", fontSize=8.9, leading=12.6)
CB = st(fontName="NG-B", fontSize=8.9, leading=12.6)
Q = st(fontName="NG", fontSize=9.8, leading=14.5, leftIndent=18, firstLineIndent=-18, spaceAfter=5)

PLAN = [
 ("10/25 (토)", "카드 A·B 외우기 → 퀴즈 1-15 → 변형 21문항(TEST 14 오답) → P7 2세트"),
 ("10/26 (일)", "카드 전체 1회독 → 퀴즈 전체 → TEST 14 Part 6·7 채점 → 실전 세트 1개(P5만 10분)"),
 ("10/27 (월)", "카드 C·D 집중 → 변형 문제 → P7 3세트(시간 재기: 단일 1세트 4분)"),
 ("10/28 (화)", "카드 E·F·G → 퀴즈 오답만 → RC 실전 1세트 75분"),
 ("10/29 (수)", "실전 채점 오답 → 새 카드 추가 → P7 이중·삼중 4세트"),
 ("10/30 (목)", "카드 체크 3칸 안 찬 것만 → 가벼운 P5 30문항 → 일찍 자기"),
 ("10/31 (금)", "시험 당일: 아침에 카드 A·C만 한 번 넘기기. 새 문제 금지"),
]

# (단서 / 질문, 규칙, 예문, 출처 오답)
CARDS = {
 "A. 빈칸 뒤에 붙는 말(짝)로 고르기": [
  ("familiarize oneself ___", "<b>with</b> (숙지하다)", "New hires should familiarize themselves <b>with</b> the manual.", "T14-112"),
  ("___ to the manual", "<b>refer</b> to (자동사). consult / check / review는 to 없이 목적어", "Please <b>refer</b> to the attached schedule.", "F-118"),
  ("comply ___ / compatible ___", "둘 다 <b>with</b>", "comply <b>with</b> the rules / compatible <b>with</b> our software", "F-113"),
  ("renowned ___ / aware ___ / capable ___", "<b>for</b> / <b>of</b> / <b>of</b> V-ing", "renowned <b>for</b> its design", "D-120"),
  ("allow · enable · ask · request + 사람 + ___", "<b>to V</b> (5형식)", "allows customers <b>to check</b> balances", "260809-111"),
  ("be permitted / authorized / certified ___", "<b>to V</b>. available to V는 '시간이 되는'", "Only staff are <b>authorized to enter</b>.", "D-123, 251026-103"),
  ("fill in ___ / stand in ___", "<b>for</b> = ~를 대신하다", "Ms. Lee will <b>fill in for</b> him.", "260531-116"),
  ("aimed ___ V-ing / as of ___", "aimed <b>at</b> V-ing / as of + <b>날짜</b>", "changes <b>aimed at</b> improving service", "D-103"),
  ("plenty ___ time / ___ time", "plenty <b>of</b> / <b>ample</b> time", "allow <b>ample</b> time", "D-111"),
  ("be accustomed to / look forward to + ___", "<b>V-ing</b> (to가 전치사)", "accustomed to <b>working</b> late", "x2"),
 ],
 "B. 목적어 유무로 자동사 · 타동사 · 수동 고르기": [
  ("뒤에 목적어 있음 (요금, 제품, 비용)", "타동사 <b>raise · lower · launch · reduce</b><br/>rise · fall · decline · proceed · arrive는 자동사", "<b>raise</b> fares / Sales <b>rose</b> 20%", "F-101, D-110, T11-115"),
  ("has been ___ to (직책)", "수동 가능한 타동사 <b>promoted</b>. resign · retire는 수동 불가", "has been <b>promoted</b> to manager", "D-105"),
  ("사물 주어 + 뒤에 목적어 없음", "<b>수동</b> (will be sent / is provided / was reviewed)", "The report <b>will be sent</b> to you.", "260531-113, -121"),
 ],
 "C. 빈칸 뒤 모양으로 전치사 · 접속사 고르기": [
  ("빈칸 뒤: 명사구 vs 주어+동사", "명사구 → during · despite · because of · upon<br/>절 → while · although · because · as soon as", "<b>Despite</b> the rain / <b>Although</b> it rained", "T11-121, 251026-110"),
  ("빈칸 뒤: V-ing", "<b>before · after · upon</b> + V-ing<br/>by the time · as soon as는 절이 와야 함", "<b>Upon</b> receiving your request", "T14-111, 260531-102"),
  ("as soon as / so that / in case", "~하자마자 / ~하도록(목적) / ~할 경우에 대비해", "enter <b>as soon as</b> the doors open", "T14-121, T11-107"),
  ("until vs by", "계속되는 상태 → <b>until</b> / 한 번 끝내는 마감 → <b>by</b>", "open <b>until</b> 9 / submit <b>by</b> Friday", "T11-137, D-115"),
  ("for · since · within · by", "for + 기간 / since + 시점 / within + 기간(이내) / by + 날짜", "worked <b>for</b> ten years / <b>since</b> 2019", "D-115"),
  ("A, B, ___ C", "병렬 → <b>or · and</b>", "by mail, by e-mail, <b>or</b> in person", "260823-110"),
  ("when · once · after · until 뒤의 절", "미래 일이어도 <b>현재형</b>", "when you <b>exit</b> (will exit ✗)", "prof-c1"),
 ],
 "D. 준동사 주변 품사 (가장 많이 틀린 유형)": [
  ("to ___ V / by ___ V-ing / have ___ p.p. / is ___ p.p.", "<b>부사</b>", "to <b>carefully</b> review / by <b>swiftly</b> responding", "260823-115, 260809-109"),
  ("전치사 + ___ + 목적어", "<b>동명사</b> (명사는 목적어 못 받음)", "by <b>announcing</b> its acquisition", "260809-107"),
  ("be + highly + ___", "<b>형용사</b>", "highly <b>responsive</b>", "260823-105"),
  ("___ enough", "<b>원급</b> 형용사 (비교급 ✗)", "<b>large</b> enough", "260531-105"),
  ("an ___ who", "<b>사람</b> 명사", "an <b>individual</b> who can manage", "F-130"),
  ("감정 분사", "사람이 느낌 → <b>-ed</b> / 사물이 일으킴 → -ing", "<b>satisfied</b> customers", "x2"),
 ],
 "E. 시제 · 수일치": [
  ("Each of + 복수명사 + ___", "<b>단수</b> 동사 (복수명사에 끌리지 말 것)", "Each of the proposals <b>was</b> reviewed.", "T14-114"),
  ("By the time + 과거 / + 현재", "<b>had p.p.</b> / will have p.p.", "By the time he arrived, we <b>had finished</b>.", "F-126"),
  ("Had + 주어 + p.p.", "If 생략 도치 → 주절 <b>would have p.p.</b>", "Had it arrived, we <b>would have started</b>.", "D-127"),
 ],
 "F. 대명사 · 관계사": [
  ("ask / request ___ to V", "목적어 자리 → <b>everyone</b>. whoever는 뒤에 동사가 필요", "asked <b>everyone</b> to leave", "260809-111, 260823-101"),
  ("___ + 명사 + 동사 (빠진 것 없음)", "<b>whose</b>", "Employees <b>whose</b> permits have expired", "T14-125"),
  ("장소 명사, ___ + 완전한 절", "<b>where</b> (시간 명사 뒤는 when)", "the desk, <b>where</b> staff will help you", "tA"),
 ],
 "G. 통째로 외울 어휘 (짝으로)": [
  ("결과 · 계획 · 예측", "tangible <b>results</b> · sales <b>forecast</b> · the <b>findings</b> of the audit(감사 결과)", "", "tA, 260809-122, T14-126"),
  ("빈도 · 범위", "on a seasonal <b>basis</b> · <b>up to</b> + 숫자(최대) · apply <b>exclusively</b> to(~에게만) · narrowed in <b>scope</b>", "", "F-120, T14-130"),
  ("행동 · 공식 표현", "work <b>diligently</b> · issue an <b>apology</b> · go into <b>effect</b> · in <b>recognition</b> of · in <b>writing</b>", "", "F-125, T11-117"),
  ("헷갈리는 짝", "<b>memorable</b>(기억에 남는) vs memorial(추모의) · <b>adapt</b> to(적응) vs adopt(채택) · <b>likelihood</b>(가능성)", "", "260809-129, T11-119"),
 ],
}

QUIZ = [
 ("New staff should familiarize themselves ------- the safety rules.", "with", "to", "A"),
 ("Please ------- to the attached map for directions.", "consult", "refer", "B"),
 ("The software is fully compatible ------- older devices.", "with", "for", "A"),
 ("The app enables users ------- payments online.", "making", "to make", "B"),
 ("Only licensed staff are ------- to operate the crane.", "authorized", "available", "A"),
 ("Mr. Ito will fill in ------- Ms. Grant during her leave.", "for", "with", "A"),
 ("The city will ------- parking fees next spring.", "rise", "raise", "B"),
 ("Prices have ------- sharply since June.", "risen", "raised", "A"),
 ("Your order ------- within three business days.", "will ship you", "will be shipped", "B"),
 ("------- reviewing the contract, Ms. Ruiz signed it.", "After", "As soon as", "A"),
 ("------- the heavy rain, the parade went ahead.", "Despite", "Although", "A"),
 ("Bring an umbrella ------- it rains later today.", "so that", "in case", "B"),
 ("The store will remain open ------- 10 P.M. tonight.", "until", "by", "A"),
 ("Please return the form ------- Friday.", "until", "by", "B"),
 ("She has led the team ------- 2021.", "for", "since", "B"),
 ("We plan to ------- review every application.", "carefully", "careful", "A"),
 ("The firm grew by ------- expanding its online store.", "rapid", "rapidly", "B"),
 ("The company boosted sales by ------- a new product line.", "launching", "launch", "A"),
 ("Our support team is highly ------- to customer requests.", "responsive", "responsively", "A"),
 ("The room is not ------- enough for 50 guests.", "larger", "large", "B"),
 ("We need an ------- who can speak Spanish.", "individual", "individuality", "A"),
 ("Each of the rooms ------- a private balcony.", "has", "have", "A"),
 ("By the time we arrived, the show -------.", "has started", "had started", "B"),
 ("Had she known, she ------- earlier.", "would have called", "will call", "A"),
 ("The manager asked ------- to wear a badge.", "everyone", "whoever", "A"),
 ("Guests ------- rooms face the sea pay extra.", "who", "whose", "B"),
 ("The new rule will go into ------- on May 1.", "effect", "affect", "A"),
 ("The discount applies ------- to new members.", "exclusively", "efficiently", "A"),
 ("The ------- of the audit will be shared next week.", "findings", "features", "A"),
 ("The ceremony was a ------- day for the whole team.", "memorial", "memorable", "B"),
]

def card_table(rows):
    data = [[Paragraph("단서 (이것만 보고 말하기)", CB), Paragraph("규칙", CB), Paragraph("예문", CB), Paragraph("1 2 3", CB)]]
    for cue, rule, ex, src in rows:
        data.append([Paragraph(cue, C), Paragraph(rule, C),
                     Paragraph(ex + (f"<br/><font size=7 color='#555555'>오답 {src}</font>" if src else ""), C),
                     Paragraph("□ □ □", C)])
    t = Table(data, colWidths=[W * 0.26, W * 0.33, W * 0.31, W * 0.10], repeatRows=1)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, colors.black), ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.black),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t

doc = SimpleDocTemplate(str(root / "data/workbook/Cards_1024.pdf"), pagesize=A4, leftMargin=12 * mm, rightMargin=12 * mm,
                        topMargin=12 * mm, bottomMargin=12 * mm, title="오답 규칙 카드 10/24")
s = [Paragraph("오답 규칙 카드 (10/24, 오답 81개 정리)", H1),
     Paragraph("보는 법: 가운데·오른쪽을 손이나 종이로 가리고 <b>왼쪽 단서만 보고 규칙을 말한다</b> → 확인. 바로 맞히면 □ 하나 칠하기. "
               "다른 날 3칸이 다 차면 그 카드는 졸업. 아침 15분, 자기 전 15분.", B), Spacer(1, 4),
     Paragraph("<b>풀 때 단 하나의 규칙</b>: 빈칸 앞뒤 단서를 선지 옆에 먼저 적고, 그 단서로 지운다. 해석은 남은 것끼리만.", B),
     Spacer(1, 6)]
for title, rows in CARDS.items():
    s += [KeepTogether([Paragraph(title, H2), card_table(rows)])]
s.append(PageBreak())
s += [Paragraph("빠른 확인 퀴즈 30 (2지선다, 문항당 10초)", H1),
      Paragraph("단서에 밑줄 → 고르기. 채점은 마지막 장. 틀린 번호의 카드 □는 지우고 다시.", B), Spacer(1, 6)]
for i, (q, a, b, _) in enumerate(QUIZ, 1):
    s.append(Paragraph(f"<b>{i}.</b> {q}&nbsp;&nbsp;&nbsp;(A) {a}&nbsp;&nbsp;&nbsp;(B) {b}", Q))
s.append(PageBreak())
s += [Paragraph("7일 계획 (시험 10/31)", H1)]
pt = Table([[Paragraph("날짜", CB), Paragraph("할 것", CB)]] + [[Paragraph(d, C), Paragraph(t, C)] for d, t in PLAN],
           colWidths=[W * 0.18, W * 0.82])
pt.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, colors.black), ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.black),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
s += [pt, Spacer(1, 14), Paragraph("퀴즈 정답", H2),
      Paragraph("  ".join(f"{i}{a}" for i, (_, _, _, a) in enumerate(QUIZ, 1)), B)]
doc.build(s)
print("cards", sum(len(v) for v in CARDS.values()), "quiz", len(QUIZ))
