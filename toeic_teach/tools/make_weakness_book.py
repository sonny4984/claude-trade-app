"""동하 약점 유형별 책 v1: 유형 → 형 실제 오답 → 알고리즘 단계 → 변형 문제(전부 새로 쓴 문항) → 정답·해설.
근거: data/rc_algorithm.md, data/progress.json, ETS Vol.3 Test 1 오답 25개, Test 4 P5·P6 오답(사진 표시 판독).
Usage: python3 tools/make_weakness_book.py -> data/workbook/Weakness_Book_v1.pdf"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

ROOT = Path(__file__).resolve().parent.parent
F = str(ROOT / "tools" / "fonts") + "/"
LIB = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("N", F + "NanumGothic-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NB", F + "NanumGothic-Bold.ttf"))
for n, f in [("S", "LiberationSans-Regular"), ("S-B", "LiberationSans-Bold"), ("S-I", "LiberationSans-Italic"), ("S-BI", "LiberationSans-BoldItalic"),
             ("R", "LiberationSerif-Regular"), ("R-B", "LiberationSerif-Bold"), ("R-I", "LiberationSerif-Italic"), ("R-BI", "LiberationSerif-BoldItalic")]:
    pdfmetrics.registerFont(TTFont(n, LIB + f + ".ttf"))
registerFontFamily("S", normal="S", bold="S-B", italic="S-I", boldItalic="S-BI")
registerFontFamily("R", normal="R", bold="R-B", italic="R-I", boldItalic="R-BI")
registerFontFamily("N", normal="N", bold="NB", italic="N", boldItalic="NB")
st = lambda n, f, s, l, **k: ParagraphStyle(n, fontName=f, fontSize=s, leading=l, **k)
T, H, K, KS = st("t", "NB", 20, 26), st("h", "NB", 13.5, 18, spaceAfter=3), st("k", "N", 9.5, 14.5), st("ks", "N", 8.4, 12)
Q, QC, PS = st("q", "S", 10.2, 13.5), st("qc", "S", 10.2, 13, leftIndent=16), st("ps", "R", 10.6, 14, alignment=TA_JUSTIFY, spaceAfter=5)
C, CB = st("c", "N", 8.5, 12), st("cb", "NB", 8.5, 12)
LM = 16 * mm
W = A4[0] - 2 * LM
P = Paragraph
L = "ABCD"
KEY = []  # (id, answer letter, explanation)


def info(rows):
    t = Table([[P(f"<b>{a}</b>", C), P(b, C)] for a, b in rows], colWidths=[26 * mm, W - 26 * mm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e9eef7")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def box(paras):
    t = Table([[[P(x, PS) for x in paras]]], colWidths=[W])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, colors.black), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def q(qid, stem, opts, ans, why):
    KEY.append((qid, L[ans], why))
    return KeepTogether([P(f"<b>{qid}.</b> {stem}", Q)] + [P(f"({L[i]}) {o}", QC) for i, o in enumerate(opts)] + [Spacer(1, 6)])


def chapter(s, no, title, symptom, cases, algo, check):
    s += [PageBreak(), P(f"{no}. {title}", H),
          info([("증상", symptom), ("형 실제 오답", cases), ("알고리즘", algo), ("시험장 한 줄", check)]), Spacer(1, 4 * mm),
          P("변형 문제 (전부 새 문장. 문제 옆에 유형·근거를 적고 풀기)", st("x", "NB", 9.5, 13)), Spacer(1, 2 * mm)]


s = [P("동하 약점 유형별 책 v1", T), Spacer(1, 2 * mm),
     P("10월~11/13 오답 기록, ETS Vol.3 Test 1·4 오답, 해석 진단, RC 알고리즘(강의 슬라이드)과 과외 팁을 합쳐서 <b>틀리는 이유별</b>로 묶었어. "
       "각 장은 <b>증상 → 형이 실제로 틀린 문제 → 알고리즘 단계 → 변형 문제</b> 순서야. 변형 문제는 전부 새로 쓴 문장이고, 형이 틀린 문제와 같은 출제 포인트·같은 함정이야.", K),
     Spacer(1, 4 * mm)]
toc = [["장", "약점 유형", "형 오답 수(확인된 것)", "변형"],
       ["1", "P5 문법: 품사 자리 (형/부/명)", "9", "6"], ["2", "P5 문법: 동사 개수 (접속사 + 1)", "5", "4"],
       ["3", "P5 전/접/부 + 전치사 용법", "9", "6"], ["4", "P5 어휘: 짝(수식어·목적어·전치사) 확인", "8", "6"],
       ["5", "P6: 시제 · 접속부사 · 문장삽입", "9", "8"], ["6", "P7 불명확: 선지 진위판단 (헤더·박스·NOT·범위)", "8", "4"],
       ["7", "P7 명확: 주관식 답 먼저 + 문장삽입", "6", "4"], ["8", "P7 다중지문: 피자 꼬투리 연계", "4+", "3"],
       ["9", "해석 구멍: 꼬리 · 병렬 · 다의어", "매 지문", "8"]]
t = Table([[P(c, CB if i == 0 else C) for c in r] for i, r in enumerate(toc)], colWidths=[10 * mm, W - 80 * mm, 45 * mm, 25 * mm])
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9d9d9"))]))
s += [t, Spacer(1, 4 * mm), P("가장 큰 원인 3개", H),
      P("① <b>확인 없이 서두름</b>: 시간이 남는데 '쉽다'는 느낌으로 넘어감 (1·2·4·7장) &nbsp; ② <b>지문 단어가 보이는 선지를 고름</b>: 명확한 문제에서 선지를 하나씩 봄 (6·7장) &nbsp; "
        "③ <b>긴 문장의 꼬리·병렬·다의어</b> (9장, 모든 파트에 영향)", K), Spacer(1, 3 * mm),
      P("쓰는 법", H),
      P("하루 2장씩. 변형 문제는 <b>해설을 보기 전에</b> 문제 옆에 알고리즘 유형(문법/전접부/어휘, 명/불, 꼬투리)과 근거 단어를 적어. 틀리면 '어느 단계에서 어긋났나'를 한 줄로. "
        "푸는 순서는 과외 팁대로 P5 → 다중지문 → P6 → 단일지문.", K),
      P("※ Test 2 전체와 Test 4의 P7 오답은 사진 표시만으로는 번호가 확실하지 않아서 이번 판에는 넣지 않았어. 틀린 번호를 보내주면 2판에 넣을게.", KS)]

# ---------- 1
chapter(s, 1, "P5 문법: 품사 자리", "선지가 꼬다리만 다른데 해석으로 풀다가 품사를 놓침",
        "T1-101 regional(명사 고름) · T1-119 consistently(형용사) · T1-125 substitutions(p.p.) · T4-103 diverse · 1000제10회 107 highly, 127 productivity, 135 internal · t21-104 inconvenience · t23-110 protective",
        "① 선지 생김새 → 문법 문제 판정 ② 빈칸 앞뒤에서 <b>가장 가까운</b> 동사·전치사·접속사·to·ing·ed 찾기 ③ 두 슬래시 사이만 보기 ④ 한정사 + 형용사 + 명사 순서",
        "명사 앞 = 형용사 / ed·ing·형용사·동사 앞 = 부사 / 동사·전치사 뒤 = 명사. 복합명사는 외운 짝일 때만.")
s += [q("1-1", "The Weston Museum is known for its ------- collection of antique maps.", ["extend", "extensive", "extensively", "extension"], 1, "its + ___ + 명사 collection → 형용사 (T1-101, T4-103)"),
      q("1-2", "When ------- stored, Lorino coffee beans stay fresh for up to six months.", ["correct", "correction", "correcting", "correctly"], 3, "빈칸 뒤 ed(stored) → 부사. When (they are) correctly stored (T1-119)"),
      q("1-3", "Hotel guests may make ------- to their reservations through the mobile app.", ["changes", "changed", "changeable", "to change"], 0, "동사 make 뒤 목적어 = 명사 (T1-125)"),
      q("1-4", "The board ------- values the feedback provided by long-term customers.", ["high", "height", "highly", "higher"], 2, "주어와 동사(values) 사이 = 부사 (10회 107)"),
      q("1-5", "The new scheduling tool is aimed at improving employee -------.", ["productive", "productively", "produce", "productivity"], 3, "improving의 목적어 = 명사. employee productivity 복합명사 (10회 127)"),
      q("1-6", "Updates are posted every Monday on the ------- company Web site.", ["internal", "internally", "internalize", "internals"], 0, "the + ___ + 명사 → 형용사 (10회 135)")]

# ---------- 2
chapter(s, 2, "P5 문법: 동사 개수 (접속사 + 1 = 동사)", "빈칸이 동사 자리인지 꼬리 자리인지 안 세고 고름",
        "T4-109 contains(containing 고름) · 해석 14번 The auction (to benefit ~) is coming up · x2-107 will undertake · t33-111 contained · sa-21 resulting in",
        "동사가 의심되면 <b>접속사 개수 + 1 = 동사 개수</b>. 동사가 모자라면 동사, 이미 찼으면 to V / -ing / p.p. 꼬리",
        "문장에서 동사에 동그라미부터. 콤마로 묶인 삽입구(동격)는 빼고 센다.")
s += [q("2-1", "Brightway, the city's largest bicycle-sharing service, ------- more than 300 stations.", ["operating", "operates", "to operate", "operation"], 1, "삽입구 빼면 주어 + ___ + 목적어. 접속사 0 → 동사 1개 필요 (T4-109)"),
      q("2-2", "The fund-raiser ------- the children's hospital will be held on May 9.", ["benefits", "will benefit", "to benefit", "has benefited"], 2, "동사 will be held가 이미 있음 → 꼬리 to benefit (해석 14번)"),
      q("2-3", "The report that Ms. Ito submitted last week ------- several errors.", ["containing", "to contain", "contained", "container"], 2, "접속사 that 1개 + 1 = 동사 2개. submitted + ___ → 동사 (t33-111)"),
      q("2-4", "Sales rose sharply in March, ------- in record profits for the quarter.", ["result", "resulted", "results", "resulting"], 3, "접속사 없음, 동사 rose 이미 있음 → 분사구문 -ing (sa-21)")]

# ---------- 3
chapter(s, 3, "P5 전/접/부 + 전치사 용법", "빈칸 뒤가 명사구인지 문장인지 안 보고 뜻으로 고름. 전치사 용법을 감으로 찍음",
        "T1-114 for(under 고름) · T4-102 on · T4-130 across · t37-125 except · t37-132 despite · 10회 128 whenever · 10회 142 by sending · t11-107 in case · t33-145 until",
        "① 전/접이 1순위, 접속부사·쓰레기부사 제거 ② 전/접 혼합 → 뒤가 명사구면 전치사, 문장이면 접속사 ③ 전치사 통일 → 용법 ④ 접속사 통일 → 해석",
        "뒤에 동사가 있나? / 기간 = for·over·during, 마감 = by, 계속 = until, 주제 = on, 범위 전체 = across·throughout")
s += [q("3-1", "------- the road construction, the bakery on Elm Street stayed open all week.", ["Although", "Despite", "However", "Even"], 1, "뒤가 명사구 → 전치사 (t37-132)"),
      q("3-2", "Please save all your receipts ------- the accounting office requests them.", ["in case", "because of", "during", "therefore"], 0, "뒤가 문장 → 접속사 in case (t11-107)"),
      q("3-3", "Average rainfall in the region ------- the past decade has been below normal.", ["under", "at", "over", "to"], 2, "the past decade + 현재완료 → over/for (T1-114)"),
      q("3-4", "Workshops ------- using the new payroll system will be offered next month.", ["at", "by", "to", "on"], 3, "주제의 on: a workshop on ~ (T4-102, t21-112)"),
      q("3-5", "Strong sales growth was reported ------- all three of the company's divisions.", ["above", "across", "into", "prior to"], 1, "여러 부문 '전체에 걸쳐' = across (T4-130)"),
      q("3-6", "The store will remain open ------- 9 P.M. on weekdays during the holiday season.", ["by", "within", "until", "since"], 2, "remain(계속) + until. by는 완료 마감 (t33-145)")]

# ---------- 4
chapter(s, 4, "P5 어휘: 짝 확인", "네 선지를 해석해 보고 그럴듯한 걸 고름. 수식받는 명사·목적어·뒤 전치사를 안 봄",
        "T1-102 city · T1-118 confident about · T1-122 in volume · T1-138 a superb · T4-106 workshop · T4-108 circle · t37-104 refrain from · t37-140 identical to",
        "동사 어휘 → 목적어 / 형용사 어휘 → 수식받는 명사 / 명사 어휘 → 수식어·동사 / 부사 어휘 → 특징 있는 부사. 안 될 때만 해석. 모르는 단어 vs 아는 단어면 아는 단어",
        "빈칸 뒤 전치사, and로 묶인 짝, 빈칸 앞 관사(a / the)에 동그라미")
s += [q("4-1", "Property values are rising in the town and ------- communities.", ["delayed", "neighboring", "optional", "partial"], 1, "and로 묶인 짝 town ↔ communities → 이웃한 (T1-102)"),
      q("4-2", "Investors feel ------- about the firm's long-term prospects.", ["useful", "accurate", "optimistic", "durable"], 2, "feel ___ about → 사람 감정 (T1-118)"),
      q("4-3", "Over the past two years, the company's online orders have tripled in -------.", ["number", "reason", "manner", "control"], 0, "tripled in number/volume/size (T1-122)"),
      q("4-4", "Dr. Reyes is regarded as a ------- surgeon by her colleagues.", ["most", "best", "brilliant", "brilliantly"], 2, "a + 형용사. 최상급은 the 필요 (T1-138)"),
      q("4-5", "Employees are asked to ------- from making personal calls during work hours.", ["prohibit", "refrain", "prevent", "avoid"], 1, "목적어 없음 + from → 자동사 refrain (t37-104)"),
      q("4-6", "This weekend, Lumen Studios invites the public to a free pottery -------.", ["ticket", "picture", "action", "workshop"], 3, "invite A to + 행사. 수식어 pottery + free (T4-106)")]

# ---------- 5
chapter(s, 5, "P6: 시제 · 접속부사 · 문장삽입", "빈칸 문장만 보고 풂. 문장삽입에서 주제만 같은 선지, 지문과 모순되는 선지를 고름",
        "T1-134(모순 선지) · T4-131 시제 · T4-135 advertised · T4-136 · T4-144 · t37-133/136/139 · 10회 133 · t33-143 Even so",
        "동사자리 = 99% 시제(앞뒤 문장으로) / 접속부사 = 자리 확인 → 역접·인과·추가 / 문장삽입 = 대명사·지시어·the·also 있는 선지 1순위 → 앞에서 받아주는 말 찾기 + 지문과 모순 확인",
        "우선 읽는다. 문법으로 풀리는 건 바로 받아먹는다.")
s += [P("Questions 5-1 to 5-4 refer to the following e-mail.", Q), Spacer(1, 3),
      box(["<b>To:</b> All Customers &nbsp; <b>From:</b> Norvik Online Banking &nbsp; <b>Subject:</b> Service interruption",
           "As some of you may have noticed, our mobile app <b>---5-1---</b> unavailable since early this morning. The problem began when a routine software update failed. <b>---5-2---</b> We expect service to be restored within twelve hours.",
           "<b>---5-3---</b>, customers can still check their balances and make transfers at any Norvik branch or through our Web site. We apologize for the <b>---5-4---</b>."]), Spacer(1, 6),
      q("5-1", "", ["was", "has been", "will be", "had been"], 1, "since early this morning + 아직 복구 전 → 현재완료 (T4-131)"),
      q("5-2", "", ["Our technical team is working to correct it now.", "The app was first released three years ago.", "Many customers prefer to visit a branch in person.", "It can be downloaded free of charge."], 0,
        "it = the problem(받아주는 말) + 뒤 '곧 복구' 와 연결. D의 It은 app을 받지만 흐름과 무관 (T4-132 유형)"),
      q("5-3", "", ["As a result", "For example", "In the meantime", "Otherwise"], 2, "복구될 때까지 '그동안' (T4-134 유형)"),
      q("5-4", "", ["convenient", "inconvenience", "inconvenient", "conveniently"], 1, "the + 명사 (t21-104)"),
      P("Questions 5-5 to 5-8 refer to the following information.", Q), Spacer(1, 3),
      box(["Kelmar Tools guarantees that its products will perform as <b>---5-5---</b> for two years from the date of purchase. <b>---5-6---</b> This <b>---5-7---</b> covers only products bought from authorized Kelmar dealers. "
           "Items returned because of damage should be shipped in their <b>---5-8---</b> packaging whenever possible."]), Spacer(1, 6),
      q("5-5", "", ["describing", "description", "described", "describes"], 2, "as + p.p. (as described/advertised) (T4-135)"),
      q("5-6", "", ["For some professional models, this period may be extended.", "Kelmar Tools has dealers in twelve countries.", "A receipt was printed at that time.", "Free samples are available at most stores."], 0,
        "this period = two years(받아주는 말). 뒤 문장의 This warranty와도 이어짐 (T4-136)"),
      q("5-7", "", ["agenda", "warranty", "sale", "requirement"], 1, "앞 문장 guarantees ~ two years를 받는 명사"),
      q("5-8", "", ["originally", "originality", "origin", "original"], 3, "their + ___ + 명사 → 형용사")]

# ---------- 6
chapter(s, 6, "P7 불명확 문제: 선지 진위판단", "What is -ed about / NOT 문제에서 지문 단어가 그대로 보이는 선지를 고름. 헤더·박스를 안 읽음. 범위가 바뀐 선지를 못 거름",
        "T1-151(헤더 날짜) · T1-161 · T1-162 NOT(whether or not) · T1-174 · T1-176 NOT · T1-178(아래 박스) · T1-180 · t23-165",
        "불명확(What is -ed about ~?, 목적, NOT) → 해당 문단 전체 + <b>선지 4개 모두 ✓✗</b>. 숫자정보 >>> 고유명사. 명사의 범위 확인(과외 팁)",
        "정답은 표현이 바뀐다(Jan 10–12 → several days). 지문 단어 그대로인 선지는 주어·범위부터 의심")
s += [P("Questions 6-1 to 6-4 refer to the following notice.", Q), Spacer(1, 3),
      box(["<b>Pinehurst Farmers Market: Vendor Information</b><br/>Season: June 6–September 26 &nbsp;|&nbsp; Saturdays, 8:00 A.M.–1:00 P.M. &nbsp;|&nbsp; Location: Town Hall parking lot",
           "All vendors must complete a registration form and pay a seasonal fee of $120. Vendors who sell prepared food must also submit a copy of their health permit. Tables may be rented from the market office for $5 per week, or vendors may bring their own.",
           "The market operates in all weather, so vendors are responsible for covering their goods. Please note that we already have more bakers than we can place this season; other food producers are especially encouraged to apply.",
           "<b>Questions? Stop by the market office on any Friday afternoon.</b>"]), Spacer(1, 6),
      q("6-1", "What is indicated about the market?", ["It is open every day.", "It runs for several months.", "It is held inside Town Hall.", "It is new this year."], 1, "헤더 June 6–September 26 → several months. C는 Town Hall 단어 재사용(parking lot) (T1-151)"),
      q("6-2", "What is NOT required of all vendors?", ["Paying a fee", "Filling out a form", "Renting a table", "Protecting their products from the weather"], 2, "may be rented, or bring their own = 선택 (T1-162)"),
      q("6-3", "What is suggested about bakers?", ["They pay a lower fee.", "They must rent two tables.", "They need a health permit only in summer.", "They may not be offered a space."], 3, "more bakers than we can place → 자리를 못 받을 수 있음 (T1-163의 근거 문장 구조)"),
      q("6-4", "How can vendors get more information?", ["By visiting an office", "By calling a town official", "By attending a Saturday meeting", "By checking a Web site"], 0, "맨 아래 굵은 줄 Stop by the market office (T1-178). 이건 명확 문제: 주관식 답 먼저")]

# ---------- 7
chapter(s, 7, "P7 명확 문제: 주관식 답 먼저 + 문장삽입", "명확한 문제인데 선지를 하나씩 맞나 틀리나 보다가 함정에 걸림. 삽입 문장의 대명사가 가리키는 말을 안 찾음",
        "T1-152(task 3) · T1-163(jewelry) · T1-175(stick around) · T1-186 · T1-164(they = photographs) · t23-163/167",
        "명확 → 나머지는 무시, 요구사항만 읽다가 '나왔다' → 읽기 중지 → <b>머릿속 주관식 답</b> → 선지에서 위치만 찾기. 문장삽입은 미리 잡고 만날 때마다 시도",
        "'가장 ~한 것'은 번호·이름부터 적는다. 누군가에게 하는 말(you, your)은 그 사람 이야기")
s += [P("Questions 7-1 to 7-4 refer to the following e-mail.", Q), Spacer(1, 3),
      box(["<b>To:</b> Marketing Team &nbsp; <b>From:</b> Olga Brandt &nbsp; <b>Subject:</b> Survey results",
           "Hi all,", "The results of last month's customer survey are in. — [1] —. Respondents rated four features of our delivery service: speed, packaging, tracking, and price. Tracking received the lowest score, with many customers saying that updates arrived hours late. — [2] —.",
           "Sven, since your team built the tracking page, could you look into what is causing the delay? — [3] —. Above all, I want to be sure the fix is in place before the holiday rush, so please plan on reporting back by October 15. — [4] —.",
           "Olga"]), Spacer(1, 6),
      q("7-1", "Which feature did customers rate the lowest?", ["Speed", "Packaging", "Price", "Tracking"], 3, "주관식 답: Tracking. 4개가 연달아 나온 '지문 속 선지', 설명이 붙은 것이 정답 (T1-152)"),
      q("7-2", "What is Sven asked to do?", ["Design a new survey", "Investigate a problem", "Hire additional staff", "Contact customers directly"], 1, "주관식 답: 지연 원인 조사 → look into = investigate"),
      q("7-3", "What is most important to Ms. Brandt?", ["Finishing before a busy period", "Reducing delivery prices", "Receiving a higher survey score", "Redesigning the packaging"], 0, "Above all ~ before the holiday rush (T1-175)"),
      q("7-4", "In which of the positions marked [1], [2], [3], and [4] does the following sentence best belong?<br/>\"They were completed by more than 2,000 customers.\"", ["[1]", "[2]", "[3]", "[4]"], 0,
        "They = the results / survey → 첫 문장 바로 뒤 (T1-164)")]

# ---------- 8
chapter(s, 8, "P7 다중지문: 피자 꼬투리 연계", "지문 하나 안에서만 답을 찾음. 표의 숫자·고유명사를 다음 지문과 못 이음",
        "T1-187(책 제목 + 무료 발송) · T1-190(책 내용 → 표 가격) · T1-193(허가 보류 → 봄 완공) · t16-177/180/188 · t23-178",
        "첫 지문은 단일지문처럼. 내려가기 전 <b>안 쓰인 빈 공간(꼬투리)</b>에 표시: 하단 > 상단 > 중간, 숫자 문장 우선. 다음 지문에서 재출현하면 즉시 풀이. 이중 1개 / 삼중 2개",
        "선지가 표의 항목 4개면 연계. 표의 '조건' 줄(per item, 이상, 제외)을 꼭 본다")
s += [P("Questions 8-1 to 8-3 refer to the following price list and e-mail.", Q), Spacer(1, 3),
      box(["<b>Castell Print Shop: Poster Printing</b>",
           "Small (A3) — $4 each &nbsp;|&nbsp; Medium (A2) — $7 each &nbsp;|&nbsp; Large (A1) — $12 each &nbsp;|&nbsp; Extra large (A0) — $20 each",
           "Orders of 50 or more posters of the same size receive 10 percent off. Orders are normally ready in three business days; next-day service is available for an additional $15 per order."]), Spacer(1, 4),
      box(["<b>To:</b> orders@castellprint.com &nbsp; <b>From:</b> Imani Cole &nbsp; <b>Date:</b> Monday, April 6",
           "Hello,", "I would like to order 60 posters for our spring concert. The attached file is designed for A2 paper. We need to hang them around town on Wednesday morning, so I hope they can be ready by tomorrow afternoon. Please let me know the total.",
           "Imani Cole, Riverside Youth Orchestra"]), Spacer(1, 6),
      q("8-1", "What is the price of one of the posters Ms. Cole wants, before any discount?", ["$4", "$7", "$12", "$20"], 1, "연계: 이메일 A2 → 표 Medium $7 (T1-190)"),
      q("8-2", "What is suggested about Ms. Cole's order?", ["It will be delivered to a concert hall.", "It will be printed in two sizes.", "It qualifies for a reduced price.", "It was placed in person."], 2, "연계: 60장 같은 크기 + '50 or more ~ 10 percent off' (꼬투리 = 조건 줄)"),
      q("8-3", "What will Ms. Cole most likely pay in addition to the cost of the posters?", ["A design fee", "A delivery charge", "A deposit", "A fee for faster service"], 3, "연계: ready by tomorrow → next-day service $15 (T1-187의 '조건 문장' 유형)")]

# ---------- 9
chapter(s, 9, "해석 구멍: 꼬리 · 병렬 · 다의어", "긴 문장에서 꼬리(in order to, showing, p.p.)를 빠뜨림 · and 뒤 동사를 앞 동사와 못 묶음 · 비슷한 단어로 바꿔 읽음 · 한 뜻만 아는 단어",
        "improve &amp; protect · verify &amp; place · ask staff to keep · The auction (to benefit) is · he's committed and will stick around · work = 작품(4회) · applications→지원자 · potter→시인 · discouraged→독려",
        "동사에 별표 → and/or 뒤가 무엇과 짝인지 화살표 → 꼬리는 괄호 → 모르는 단어는 ??로 두고 구조만",
        "해석이 어색하면: ① 전치사 빠뜨렸나 ② 이 단어 두 번째 뜻 ③ 철자 끝까지")
sent = ["Applicants must submit three samples of their work in order to be considered for the award.",
        "Please review the attached schedule and let me know which session you prefer.",
        "The committee asked all vendors to keep their receipts as proof of payment.",
        "The grant, designed to help local artists expand their audience, will be awarded in May.",
        "Mr. Doyle wants assurances that the supplier is reliable and will deliver on time.",
        "We received far more applications from designers than we can accept this year.",
        "Since you propose to share a booth with a local potter, please indicate how you plan to use the space jointly.",
        "Store the samples in a dry place, or they may lose their color."]
ans9 = ["지원자는 / <b>작품</b> 샘플 3개를 제출해야 한다 / (수상 후보로 고려되려면) — work = 작품, in order to = ~하려면",
        "첨부된 일정을 검토하고 / (그리고) 알려 주세요 / 어느 세션을 선호하는지 — review ↔ let 명령문 병렬",
        "위원회는 요청했다 / 모든 판매자에게 / 영수증을 보관해 달라고 / 결제 증빙으로 — ask O to V, keep = 보관",
        "그 보조금은 (지역 예술가들이 관객을 넓히도록 돕기 위해 만들어진) / 5월에 수여된다 — 진짜 동사 will be awarded",
        "도일 씨는 확답을 원한다 / (공급업체가 믿을 만하고 / 제때 납품할 것이라는) — is ↔ will deliver 병렬",
        "우리는 받았다 / 훨씬 더 많은 <b>지원서</b>를 / 디자이너들로부터 / 올해 선정할 수 있는 것보다 — far + 비교급, applications",
        "당신이 지역 <b>도예가</b>와 부스를 같이 쓰자고 <b>제안했으니</b> / 그 공간을 <b>공동으로</b> 어떻게 쓸지 알려 주세요 — since = ~이므로",
        "샘플을 건조한 곳에 보관하세요 / <b>안 그러면</b> 색이 바랠 수 있어요 — 명령문, or"]
for i, x in enumerate(sent, 1):
    s += [P(f"<b>9-{i}.</b> {x}", Q), Spacer(1, 16)]
    KEY.append((f"9-{i}", "", ans9[i - 1]))

# ---------- answers
s += [PageBreak(), P("정답과 해설", H), P("답만 맞추지 말고 '알고리즘 어느 단계'로 풀었는지 확인해.", KS), Spacer(1, 3 * mm)]
rows = [[P(h, CB) for h in ("번호", "정답", "알고리즘대로 볼 곳 (같은 유형의 형 오답)")]] + [[P(a, CB), P(f"<b>{b}</b>", C), P(c, C)] for a, b, c in KEY]
t = Table(rows, colWidths=[14 * mm, 12 * mm, W - 26 * mm], repeatRows=1)
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9d9d9")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]), ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
s += [t, Spacer(1, 5 * mm), P("시험장 체크리스트 (11/15)", H)]
for line in ["순서: P5 → 다중지문(176~200) → P6 → 단일지문. 파트가 끝날 때마다 바로 마킹.",
             "P5: 문장 읽기 전에 선지 생김새 → 빈칸 앞뒤 가장 가까운 것. 동사가 의심되면 접속사 + 1.",
             "P6: 일단 읽는다. 문장삽입은 대명사·the·also 선지부터, 받아주는 말 + 모순 확인.",
             "P7: 문제만 먼저. 명확 = 주관식 답 먼저 / 불명확 = 선지 ✓✗. 헤더·맨 아래 박스도 근거.",
             "다중지문: 내려가기 전에 꼬투리(안 쓰인 숫자·이름·조건 줄) 표시. 이중 1개, 삼중 2개.",
             "'쉽다'는 느낌 = 근거 줄 한 번 더. 시간은 남는다.",
             "LC: 세트 3번째 문제는 끝까지 듣고 마킹. 놓치면 찍고 다음 선독."]:
    s.append(P("□ " + line, K))
out = ROOT / "data" / "workbook" / "Weakness_Book_v1.pdf"
SimpleDocTemplate(str(out), pagesize=A4, leftMargin=LM, rightMargin=LM, topMargin=14 * mm, bottomMargin=14 * mm, title="동하 약점 유형별 책 v1").build(s)
from collections import Counter
print(out, len(KEY), Counter(k[1] for k in KEY))
