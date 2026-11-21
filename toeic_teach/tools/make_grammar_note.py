"""동하 문법 정리노트: 왼쪽 = 문법 규칙(정리노트 형식), 오른쪽 = 형이 실제로 틀린 문제(짧은 단서만)와 왜 틀렸는지.
-> data/workbook/Grammar_Note_v1.pdf"""
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
ROOT = Path(__file__).resolve().parent.parent
F = str(ROOT / "tools/fonts") + "/"
pdfmetrics.registerFont(TTFont("N", F + "NanumGothic-Regular.ttf")); pdfmetrics.registerFont(TTFont("NB", F + "NanumGothic-Bold.ttf"))
registerFontFamily("N", normal="N", bold="NB", italic="N", boldItalic="NB")
st = lambda n, f, s, l, **k: ParagraphStyle(n, fontName=f, fontSize=s, leading=l, **k)
T, H, K, KS = st("t", "NB", 17, 22), st("h", "NB", 12.5, 16, textColor=colors.HexColor("#1a4fa0")), st("k", "N", 9.3, 14), st("ks", "N", 8.3, 12, textColor=colors.HexColor("#555555"))
P = Paragraph
W = landscape(A4)[0] - 24 * mm
R = '<font color="#c0392b"><b>'; E = "</b></font>"

CH = [
 ("1. 품사 자리 (선지가 꼬다리만 다를 때)",
  ["<b>공식: 자리를 먼저 적고 그 품사만 고른다. 해석하지 않는다.</b>",
   "· <b>형용사</b>: 한정사(a/the/its/소유격) + ___ + 명사 / be·remain·seem + ___ / <b>It is ___ to V</b> / make·keep·find + 목적어 + ___",
   "· <b>부사</b>: ___ + 형용사·p.p.·-ing / 주어 + ___ + 동사 / have ___ p.p. / be ___ p.p. / <b>완전한 문장 뒤</b> / When·If ___ p.p.",
   "· <b>명사</b>: 타동사 뒤(목적어) / 전치사 뒤 / 한정사·형용사 뒤 / make·obtain·request + ___",
   "· 꼬리로 품사 판단: -al·-ive·-ous·-able·-ful = 형 / -ly = 부 / -tion·-ment·-ness·-ity·-ance = 명 (예외: approval·proposal·arrival = 명사)",
   "· 복합명사(sales forecast, employee productivity)는 <b>외운 짝일 때만</b>. 아니면 형용사가 기본."],
  [("T5-107", "more ___ qualified workers", "high → highly", "p.p. 앞은 부사. '높은'으로 해석해서 형용사를 고름"),
   ("T5-119", "It is ___ to bring boots", "advise → advisable", "It is 뒤는 형용사. 동사를 넣음"),
   ("T5-127", "improve the process ___.", "more substantial → substantially", "문장이 이미 완전 → 부사"),
   ("T1-101", "range of ___ goods", "region → regional", "'지역의'가 형용사로 안 느껴져 명사를 고름"),
   ("T1-119", "When ___ applied", "consistent → consistently", "When (it is) 생략 구조를 못 봄"),
   ("T1-125", "make menu ___", "substituted → substitutions", "make의 목적어 = 명사"),
   ("11/15", "make it as ___ as possible", "smoothly → smooth", "make + O + 형용사 (5형식)"),
   ("10회 107·127·135", "___ values / improving employee ___ / the ___ Web site", "high·productively·internalize", "부사 / 명사 / 형용사 자리")]),
 ("2. 동사 개수와 꼬리 (형 오답 1위, 37건)",
  ["<b>공식: 접속사(관계사 포함) 개수 + 1 = 동사 개수.</b>",
   "· 동사가 모자라면 → 빈칸 = 동사 (수일치 → 태 → 시제 순서로 고른다)",
   "· 동사가 이미 찼으면 → 빈칸 = 꼬리: <b>to V</b>(목적·수식) / <b>-ing</b>(뒤에 목적어 있음, 능동) / <b>p.p.</b>(뒤에 목적어 없음, 수동)",
   "· 콤마 두 개 사이 삽입구(동격)는 지우고 센다.",
   "· 명사 + 명사 + 동사 = that 생략: The report (that) the board reviewed <b>contained</b> ~",
   "· 콤마 뒤 분사구문: ~, <b>resulting</b> in ~ (접속사 없으면 동사를 또 쓸 수 없다)"],
  [("T4-109", "Questwiz, the newest database, ___ a wide range", "containing → contains", "삽입구를 안 지워서 동사 자리를 못 봄"),
   ("해석 14번", "The auction ___ our program is coming up", "동사로 해석", "진짜 동사 is coming up이 따로 있음 → to benefit"),
   ("t33-111", "The report the board reviewed ___", "to contain → contained", "that 생략 + 진짜 동사 자리"),
   ("x2-107", "Dr. Major ___ the role", "undertake → will undertake", "단수 주어에 원형"),
   ("T5-129", "By this time next year, ___ two plants", "(시제)", "By this time next year → will have p.p.")]),
 ("3. and 병렬 (and 뒤는 앞의 무엇과 짝인가)",
  ["<b>공식: and/or를 보면 '뒤에 온 것과 같은 모양'을 앞에서 찾는다.</b>",
   "· to V and (to) <b>V원형</b> / V-ing and <b>V-ing</b> / p.p. and <b>p.p.</b> / 과거동사 and <b>과거동사</b>",
   "· and 뒤에 [주어 + 동사]가 또 나오면 새 문장, [동사]만 나오면 앞 동사와 병렬",
   "· 명령문 + or = '안 그러면'",
   "· A, B, and C: 세 개가 같은 품사"],
  [("11/15", "were asked to review ~ and ___ in", "filling in → fill in", "to 뒤 동사원형과 짝인데 -ing를 고름"),
   ("11/15", "were delivered ~ and ___ in perfectly", "(fit)", "and 앞 과거동사와 짝 → fit(과거)"),
   ("T2-102", "photography, drawing, ___ other arts", "thus → and", "A, B, and C 나열"),
   ("T1-175", "he's committed and will stick around", "해석 누락", "and 뒤 조동사 = 앞 동사와 짝"),
   ("해석 30번", "verify that ~ and place them", "that절 안으로 해석", "verify ↔ place 명령문 병렬")]),
 ("4. 동사 뒤 모양 (to V / V-ing / 원형)",
  ["· <b>동사 + 목적어 + to V</b>: ask, request, require, encourage, allow, permit, enable, invite, remind, urge → '목적어가 ~하도록' (목적 '위해서' 아님)",
   "· <b>V-ing를 받는 동사</b>: consider, suggest, recommend, avoid, finish, postpone / spend 시간 V-ing / have difficulty V-ing",
   "· <b>전치사 + V-ing</b>: by, before, after, upon, without, instead of / look forward <b>to</b> V-ing, be committed <b>to</b> V-ing, be accustomed <b>to</b> V-ing",
   "· help (O) (to) 원형 / make·have·let + O + 원형",
   "· suggest·recommend·request·insist <b>that</b> S (should) <b>원형</b>"],
  [("er0809-111 외", "ask everyone ___", "3회 오답", "ask + 사람 + to V"),
   ("t21-123 외", "spend time ___", "to analyze → analyzing", "3회 이상 오답"),
   ("10회 142", "by ___ this notice", "to send → sending", "앞의 hope to에 끌림"),
   ("t37-119", "suggest that the meeting ___ postponed", "is → be", "that절 동사원형"),
   ("해석 35번", "asking staff to keep", "'지키기 위해'", "ask O to V를 목적으로 읽음")]),
 ("5. 전치사 vs 접속사 vs 부사",
  ["<b>공식: ① 선지에서 접속부사부터 지운다 ② 빈칸 뒤에 동사가 있나? 있으면 접속사, 없으면 전치사 ③ 뒤가 비었거나 콤마면 부사</b>",
   "· 전치사: despite, in spite of, during, because of, due to, prior to, regarding, except, besides, given",
   "· 접속사: although, though, while, because, once, unless, in case, as soon as, whereas, whenever, given that, except when/that",
   "· 접속부사(P5 정답 불가): however, therefore, furthermore, instead, otherwise",
   "· 전치사 + V-ing도 가능: before attending"],
  [("t37-132", "___ the high cost", "although → despite", "뒤가 명사구"),
   ("t37-125", "___ + 명사구", "otherwise → except", "부사는 명사를 못 이음"),
   ("10회 128", "___ the sales team has an event", "besides → whenever", "뒤가 문장"),
   ("t11-107 외", "___ you need ~", "so that → in case", "in case 3회 오답"),
   ("11/15", "all day ___ when it is reserved", "(except)", "except when")]),
 ("6. 전치사 용법",
  ["· 기간: <b>for / over / during</b> the past three years (+ 현재완료)", "· 마감(한 번에 끝): <b>by</b> Friday / 계속: <b>until</b> 9 P.M. (remain, stay, be open)",
   "· 주제: a class / workshop / seminar / presentation / decision <b>on</b>", "· 범위 전체: <b>across / throughout</b> all branches",
   "· ~중에: <b>among</b> + 복수 명사 / 둘 사이: between A and B", "· 시각 앞 '쯤': around / 맞은편: opposite"],
  [("T1-114", "___ the past three years", "under → for", "기간 + 현재완료"),
   ("T4-102", "Classes ___ using the software", "by → on", "주제의 on"),
   ("T4-130", "seen ___ all business segments", "above → across", "범위 전체"),
   ("T2-123", "are ___ the items featured", "except → among", "among + 복수"),
   ("t33-145", "still ___ Friday", "by → until", "계속 동사 + until")]),
 ("7. 대명사 · 명사절",
  ["· 회사·기관·사물 = <b>its</b> / 사람 = his·her / 복수 = their", "· anyone who + 단수동사 / those who + 복수동사",
   "· <b>whoever</b> + 동사 = '누구든 ~하는 사람' (앞에 선행사 없음, 뒤에 동사 있음)", "· 명사 앞 = 소유격 / 동사·전치사 뒤 단독 = 목적격 / 강조·주어와 같으면 재귀"],
  [("T1-129", "most of ___ plans", "his → its", "회사는 its"),
   ("11/15", "rewarded ___ was involved", "(whoever)", "뒤에 동사가 있으면 whoever"),
   ("T6-118", "___ who is unable", "those → anyone", "who 뒤 is(단수)")]),
 ("8. 어휘: 짝으로 고른다",
  ["· 동사 어휘 → <b>목적어와 뒤 전치사</b>: decline an offer, fill a prescription, detail the changes, conform <b>to</b>, refrain <b>from</b>, comply <b>with</b>, respond <b>to</b>",
   "· 형용사 어휘 → <b>수식받는 명사·뒤 전치사</b>: confident <b>about</b>, linked <b>to</b>, identical <b>to</b>, compatible <b>with</b>",
   "· 명사 어휘 → 동사·수식어: double <b>in volume</b>, on a seasonal <b>basis</b>", "· 부사 어휘 → 특징: arrive <b>promptly</b>, though <b>hesitantly</b>, 숫자 앞 almost·nearly",
   "· 철자 쌍둥이: adopt/adapt, confirm/conform, assure/insure/ensure, cover/coverage"],
  [("T5-112", "arrive ___ at 7:00", "clearly → promptly", "시각 앞 '정각에'"),
   ("T5-124", "took an hour to ___ each change", "respond → detail", "목적어가 바로 옴 → 타동사"),
   ("11/15", ", though ___.", "previously", "previously = 이전에. though → hesitantly"),
   ("T1-118·122", "feel ___ about / doubled in ___", "helpful·economy", "confident about / in volume")]),
]

s = [P("동하 문법 정리노트 v1", T), P("왼쪽은 규칙, 오른쪽은 형이 실제로 틀린 문제야. 문제는 단서 부분만 짧게 적었어. 꼬다리 문제를 풀 때는 답을 고르기 전에 번호 옆에 <b>형 / 부 / 명 / 동</b> 한 글자를 먼저 적어.", K), Spacer(1, 4 * mm)]
for i, (title, rules, errs) in enumerate(CH):
    left = [P(title, H), Spacer(1, 2)] + [P(r, K) for r in rules]
    er = [[P("<b>출처</b>", KS), P("<b>단서</b>", KS), P("<b>형 답 → 정답</b>", KS), P("<b>왜 틀렸나</b>", KS)]] + [[P(a, KS), P(b, K), P(R + c + E, K), P(d, K)] for a, b, c, d in errs]
    et = Table(er, colWidths=[20 * mm, 46 * mm, 36 * mm, W * 0.5 - 108 * mm])
    et.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#cccccc")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2)]))
    t = Table([[left, [P("형이 실제로 틀린 문제", st("x", "NB", 10, 14, textColor=colors.HexColor("#c0392b"))), Spacer(1, 2), et]]], colWidths=[W * 0.5, W * 0.5])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.black), ("LINEAFTER", (0, 0), (0, -1), 0.4, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#fdf6f5")), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    s += [t, Spacer(1, 4 * mm)]
out = ROOT / "data/workbook/Grammar_Note_v1.pdf"
SimpleDocTemplate(str(out), pagesize=landscape(A4), leftMargin=12 * mm, rightMargin=12 * mm, topMargin=11 * mm, bottomMargin=11 * mm, title="동하 문법 정리노트").build(s)
print(out)
