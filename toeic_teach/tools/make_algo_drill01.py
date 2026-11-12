"""알고리즘 드릴 01: P5 10 + P6 1지문 + P7 단일 2 + 이중 1 + 삼중 1 (31문항). 전부 새로 쓴 문항.
동하 오답 유형(data/progress.json, 11/10~12 해석 진단)과 data/rc_algorithm.md 단계에 맞춰 설계.
Usage: python3 tools/make_algo_drill01.py -> data/workbook/Algo_Drill_01.pdf, _Answers.pdf"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "tools" / "fonts"
pdfmetrics.registerFont(TTFont("N", str(F / "NanumGothic-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NB", str(F / "NanumGothic-Bold.ttf")))
pdfmetrics.registerFontFamily("N", normal="N", bold="NB", italic="N", boldItalic="NB")
st = lambda n, f="N", s=10, l=14, c=colors.black: ParagraphStyle(n, fontName=f, fontSize=s, leading=l, textColor=c)
T, H, B, Q, S, C, CB = st("t", "NB", 16, 21), st("h", "NB", 12, 16), st("b", "N", 10, 15), st("q", "N", 10, 14.5), st("s", "N", 8, 11, colors.HexColor("#666666")), st("c", "N", 8.6, 12.5), st("cb", "NB", 8.6, 12.5)
LM = 14 * mm
W = A4[0] - 2 * LM
P = Paragraph

P5 = [
    (101, "Hartwell Bank offers ------- advice to small-business owners at no cost.", ["finance", "finances", "financial", "financially"], 2,
     "문법(꼬다리)", "빈칸 뒤 명사 advice → 한정사+<b>형용사</b>+명사. -al = 형용사", "복합명사 함정(finance advice). 외운 짝이 아니면 형용사가 기본 (101 regional과 같은 유형)"),
    (102, "When ------- installed, the new filters can reduce energy costs by up to 20 percent.", ["proper", "property", "properties", "properly"], 3,
     "문법(꼬다리)", "빈칸 뒤 <b>ed</b>(installed) → 그 앞 = 부사. When (they are) properly installed", "When 뒤 S+be 생략 (119 consistently applied와 같은 유형)"),
    (103, "Ms. Alvarez asked the vendors ------- their invoices by the end of the week.", ["submit", "submitted", "to submit", "submitting"], 2,
     "문법(꼬다리)", "빈칸 앞 동사 asked + 목적어 the vendors → <b>ask O to V</b>. 접속사 0개 + 1 = 동사 1개(asked)라 동사 형태 탈락", "ask + 사람 + to V = '사람에게 ~해 달라고' (4회 이상 오답 유형)"),
    (104, "------- the heavy snow, the product launch took place as scheduled.", ["Despite", "Although", "However", "Even"], 0,
     "전/접/부", "접속부사 However 탈락 → 전/접 혼합 → 빈칸 뒤 <b>명사구</b>(the heavy snow) → 전치사", "Although는 뒤에 문장이 와야 함 (despite/although 반복 오답)"),
    (105, "Please keep your receipt ------- you need to return the item.", ["in case", "due to", "despite", "therefore"], 0,
     "전/접/부", "접속부사 therefore 탈락 → 전/접 혼합 → 빈칸 뒤 <b>문장</b>(you need ~) → 접속사 in case", "due to, despite는 전치사. in case = ~할 경우에 대비해"),
    (106, "Customers may make ------- to their orders until noon on the day of delivery.", ["adjust", "adjusted", "adjustments", "adjustable"], 2,
     "문법(꼬다리)", "빈칸 앞 동사 make → 목적어 = <b>명사</b>. make adjustments to", "make를 사역동사로 보면 목적어가 없어 뜻이 안 됨 (125 substitutions와 같은 유형)"),
    (107, "The company's exports have doubled in ------- over the past three years.", ["value", "opinion", "manner", "position"], 0,
     "어휘(명사)", "명사 어휘 → 동사 확인: doubled <b>in</b> + 양·크기·가치 (in value / volume / size / number)", "over the past three years + 현재완료도 같이 확인 (114, 122 유형)"),
    (108, "Although Kestrel Airlines raised fares last month, ------- flights remain fully booked.", ["it", "itself", "his", "its"], 3,
     "문법(꼬다리)", "빈칸 뒤 명사 flights → 소유격 자리. 가리키는 대상 = 회사 → <b>its</b>", "his는 사람 (129 유형)"),
    (109, "Mr. Doyle is widely regarded as a ------- negotiator.", ["best", "most", "skilled", "skillfully"], 2,
     "어휘+수식어 순서", "한정사 <b>a</b> + 형용사 + 명사. 최상급 best는 the가 필요 → 탈락", "뜻이 둘 다 되면 관사로 가른다 (138 a superb tailor 유형)"),
    (110, "All product packaging must ------- to the new safety regulations.", ["confirm", "conform", "contain", "conduct"], 1,
     "어휘(동사)", "동사 어휘 → 목적어 확인: 목적어 없음 + <b>to</b> → 자동사 conform to(~에 부합하다)", "철자 쌍둥이 confirm / conform (단어장 1번 유형)"),
]

P6_TEXT = ("<b>To:</b> All Tenants, Marlow Business Center<br/><b>Subject:</b> Elevator maintenance<br/><br/>"
           "The east elevators will be out of service from Monday, June 3, through Wednesday, June 5, while technicians <b>-----131-----</b> the control system. "
           "During this period, please use the west elevators or the main stairwell. <b>-----132-----</b>, deliveries of large items should be scheduled for Thursday or later, "
           "since the freight elevator is part of the east bank. We recognize that this work may cause some <b>-----133-----</b>, and we thank you for your patience. <b>-----134-----</b>")
P6 = [
    (131, "", ["replace", "replaced", "have replaced", "replacing"], 0, "파트5 유형: 동사자리 = 시제",
     "while + S + ___ → 동사 자리(replacing 탈락). 주절이 will be(미래 일정) → 시간절은 <b>현재형</b>", "시간·조건절은 미래를 현재로 (m1-133 유형)"),
    (132, "", ["However", "In addition", "For example", "Otherwise"], 1, "접속부사 (통일 → 종류)",
     "앞: 서쪽 엘리베이터를 써라 / 뒤: 큰 물건 배송은 목요일 이후로 → 안내가 하나 더 = <b>추가</b>", "역접·예시·조건 아님. 90%는 역접/인과/추가"),
    (133, "", ["inconvenience", "convenient", "attention", "permission"], 0, "파트5 유형: 어휘",
     "cause some ___ → 동사 cause의 목적어(명사) + 뒤 'thank you for your patience' → 불편", "convenient는 형용사라 자리부터 탈락"),
    (134, "", ["The west elevators will also be closed on those days.", "Questions may be directed to the building office at extension 204.",
               "They were installed more than twenty years ago.", "Please use the east elevators during this time."], 1, "문장삽입",
     "대명사·also가 있는 A, C가 1순위 후보 → A는 지문(서쪽을 쓰라)과 <b>모순</b>, C의 They는 받아주는 말은 있어도 감사 인사 뒤에 주제가 안 맞음. D도 모순 → 마무리 문장 B",
     "1순위 후보라도 '받아주는 말 + 모순 여부'를 확인 (134 north lobby 유형)"),
]

SETS = [
    dict(head="Questions 147-149 refer to the following notice.",
         text=["<b>Riverside Community Center: Spring Workshop Series</b><br/>Dates: March 4–6 &nbsp;|&nbsp; Location: Room 12 &nbsp;|&nbsp; Fee: $15 per session (free for members)",
               "Our spring workshop series returns with four sessions led by local professionals. Session 1 covers basic bread baking. Session 2 introduces container gardening. "
               "Session 3 teaches bicycle repair. Session 4, added this year at the request of many members, shows participants how to edit photos on a smartphone.<br/><br/>"
               "Participants in Session 3 must bring their own bicycle; all other materials are provided. Space is limited to 12 people per session, so early registration is recommended. "
               "To sign up, stop by the front desk or call 555-0142."],
         qs=[(147, "What is indicated about the workshop series?", ["It is held over several days.", "It is free for all participants.", "It is being offered for the first time.", "It takes place at a bicycle shop."], 0,
              "불명확 (What is -ed about)", "선지 진위판단. A ✓ 헤더 <b>March 4–6</b> / B ✗ 회원만 무료 / C ✗ returns / D ✗ Room 12",
              "근거가 본문이 아니라 <b>헤더(숫자정보)</b>. 정답은 표현이 바뀜(3/4–6 → several days) (151 유형)"),
             (148, "Which session is new this year?", ["Bread baking", "Container gardening", "Bicycle repair", "Photo editing"], 3,
              "명확", "주관식 답 먼저: 'added this year' = Session 4 = 사진 편집 → 선지에서 찾기",
              "고유명사 4개 연달아 = 지문 속 선지. 설명이 붙은 것(딸기)이 정답"),
             (149, "What is NOT mentioned about the sessions?", ["The maximum number of participants", "The cost for nonmembers", "The names of the instructors", "The location"], 2,
              "불명확 (NOT)", "A ✓ 12 people / B ✓ $15 / C ✗ local professionals뿐, 이름 없음 / D ✓ Room 12",
              "NOT은 선지 4개 전부 ✓✗. '언급은 됐지만 묻는 조건이 아닌 것' 주의 (162 유형)")]),
    dict(head="Questions 150-153 refer to the following e-mail.",
         text=["<b>To:</b> Daniel Osei &nbsp; <b>From:</b> Priya Nair, Harborview Art Market &nbsp; <b>Date:</b> April 9<br/><b>Subject:</b> Your vendor application",
               "Dear Mr. Osei,<br/><br/>Thank you for applying to sell at the Harborview Art Market. —[1]— All vendors must pay a $40 booth fee, whether or not they choose to rent a table from us. "
               "In addition, we ask that you send three photographs of your work so that our committee can review it. —[2]—<br/><br/>"
               "The market is held on the pier every Saturday from May through September, rain or shine, so vendors must bring a canopy to cover their goods. —[3]—<br/><br/>"
               "Please be aware that we already have a large number of ceramics vendors this season. Because your application arrived early, however, we expect to be able to offer you a booth. —[4]—<br/><br/>"
               "Sincerely,<br/>Priya Nair"],
         qs=[(150, "What is suggested about the art market?", ["It is open year-round.", "It takes place outdoors.", "It is new this season.", "It charges admission to visitors."], 1,
              "불명확 (suggested)", "A ✗ May through September / B ✓ on the pier + rain or shine + canopy / C, D 근거 없음",
              "여러 단서를 이어야 나오는 추론 (161 유형)"),
             (151, "What is NOT required of vendors?", ["Paying a booth fee", "Sending photographs", "Renting a table", "Bringing a canopy"], 2,
              "불명확 (NOT)", "A ✓ must pay / B ✓ we ask that you send / C ✗ <b>whether or not</b> = 선택 / D ✓ must bring",
              "지문에 '나오지만' 요구 사항이 아닌 것 (162 유형)"),
             (152, "What does Mr. Osei most likely sell?", ["Photographs", "Canopies", "Paintings", "Ceramics"], 3,
              "명확", "주관식 답 먼저: 마지막 문단은 Mr. Osei에게 하는 말 → 'ceramics vendors가 많지만 <b>you</b>에게 부스를 줄 수 있다' → 도자기",
              "많이 나온 단어(photographs) ≠ 정답 (163 유형)"),
             (153, "In which of the positions marked [1], [2], [3], and [4] does the following sentence best belong?<br/>\"They should show the items you plan to sell.\"", ["[1]", "[2]", "[3]", "[4]"], 1,
              "문장삽입", "대명사 <b>They</b> → 받아주는 말 = three photographs → 바로 뒤 [2]", "삽입 문장의 대명사가 가리키는 명사 바로 뒤 (164 유형)")]),
    dict(head="Questions 154-158 refer to the following e-mail and notice.",
         text=["<b>To:</b> Hana Seo, Calder Design &nbsp; <b>From:</b> Brightleaf Office Supply &nbsp; <b>Date:</b> October 2<br/><b>Subject:</b> Order #40718",
               "Dear Ms. Seo,<br/><br/>Thank you for your order. Items in stock will ship within two business days. Orders over $150 qualify for free standard shipping. "
               "Please note that the Model K desk lamp is currently out of stock; see the notice on our Web site for details.",
               ("TABLE", [["Item", "Quantity", "Unit Price", "Total"], ["Ergo desk chair (Model R)", "1", "$129.00", "$129.00"], ["Desk lamp (Model K)", "2", "$24.00", "$48.00"],
                          ["Paper trays (set of 3)", "1", "$18.00", "$18.00"], ["", "", "Order total", "$195.00"]]),
               "<b>Notice to Customers</b><br/><br/>Due to a supplier delay, the Model K desk lamp will not be available until October 20. Customers who have already ordered it may "
               "(1) wait and receive it by express delivery at no additional charge, or (2) replace it with the Model L lamp, which costs $6.00 more per lamp. "
               "Customers who choose neither option by October 10 will automatically receive a refund for the lamps. To tell us your choice, call customer service at 555-0199."],
         qs=[(154, "What is the purpose of the e-mail?", ["To confirm an order", "To request payment", "To announce a sale", "To apologize for a damaged item"], 0,
              "불명확 (목적)", "첫 문단 + 표 = 주문 확인", "목적은 안 풀리면 마지막으로 미룬다"),
             (155, "What is indicated about Ms. Seo's order?", ["It was placed by phone.", "It includes two chairs.", "It qualifies for free standard shipping.", "It will be shipped from overseas."], 2,
              "불명확", "C ✓ over $150 무료 + Order total <b>$195.00</b> (지문 1 안에서 숫자 2개 연결) / B ✗ 의자 1개, 램프가 2개", "숫자정보 >>> 고유명사. 수량 바꿔치기 함정"),
             (156, "According to the notice, why is the Model K lamp unavailable?", ["It has been discontinued.", "A supplier is behind schedule.", "It was recalled for safety reasons.", "Its price has changed."], 1,
              "명확", "주관식 답: supplier delay → 선지에서 바뀐 표현(behind schedule) 찾기", "패러프레이징"),
             (157, "If Ms. Seo chooses the Model L lamp, how much more will she pay in total?", ["$6.00", "$12.00", "$24.00", "$48.00"], 1,
              "명확 + <b>연계</b>", "공지 '$6.00 more <b>per lamp</b>' × 표의 Quantity <b>2</b> = $12.00",
              "피자 꼬투리 = 표의 수량 2 (지문 1에서 아직 안 쓰인 숫자). 이중지문 연계 1개"),
             (158, "What will happen if Ms. Seo does not respond by October 10?", ["Her entire order will be canceled.", "She will be charged for express delivery.", "She will receive a refund for the lamps.", "The lamps will be shipped on October 20."], 2,
              "명확", "주관식 답: neither option by October 10 → refund <b>for the lamps</b>", "A는 범위 부풀리기(램프만 → 전체 주문)")]),
    dict(head="Questions 159-163 refer to the following article, e-mail, and chart.",
         text=["<b>Maple Street Branch to Close for Renovations</b><br/><br/>LINDALE (September 3)—The Lindale Public Library will close its Maple Street branch for renovations beginning October 1. "
               "During the six-month project, the building will gain a children's reading room and four meeting rooms that community groups can reserve. "
               "Library director Omar Haddad said that the meeting rooms will be free for nonprofit organizations, while businesses will pay a fee of $30 per hour. "
               "\"Our old branch had no space for groups to gather,\" Mr. Haddad noted. The branch is expected to reopen in April.",
               "<b>To:</b> Omar Haddad &nbsp; <b>From:</b> Elena Marsh &nbsp; <b>Date:</b> April 12 &nbsp; <b>Subject:</b> Meeting room<br/><br/>Dear Mr. Haddad,<br/><br/>"
               "Congratulations on the reopening. I am writing on behalf of the Lindale Garden Society, a nonprofit volunteer group. We would like to reserve a meeting room for our monthly meeting "
               "on the first Tuesday of each month from 6 to 8 P.M. We usually have about 25 members attending, and we need a projector for presentations. Could you tell me which room would suit us?<br/><br/>Elena Marsh",
               ("TABLE", [["Maple Street Branch Meeting Rooms", "Seats", "Projector"], ["Room A", "10", "No"], ["Room B", "20", "Yes"], ["Room C", "30", "Yes"], ["Room D", "40", "No"]]),
               "Rooms may be reserved up to two months in advance. All rooms close at 8:30 P.M."],
         qs=[(159, "What is the article mainly about?", ["Changes to a library branch", "The hiring of a new director", "An increase in library fees", "A new children's book"], 0,
              "불명확 (주제)", "제목 + 첫 문장: 지점 보수 공사", ""),
             (160, "What is suggested about the Maple Street branch before the renovation?", ["It was open only on weekdays.", "It charged an admission fee.", "It was located on a different street.", "It did not have meeting rooms."], 3,
              "불명확", "D ✓ 'Our old branch had <b>no space for groups to gather</b>' + 공사로 meeting rooms가 생김", "인용문이 근거"),
             (161, "What is suggested about the Lindale Garden Society?", ["It will not be charged for the room.", "It meets every week.", "It was founded in April.", "It has 40 members."], 0,
              "불명확 + <b>연계 1</b>", "이메일 'a <b>nonprofit</b> volunteer group' + 기사 'free for nonprofit organizations'",
              "피자 꼬투리 = 기사의 요금 문장(비영리 무료 / 기업 $30). B ✗ monthly"),
             (162, "Which room will the Lindale Garden Society most likely be assigned?", ["Room A", "Room B", "Room C", "Room D"], 2,
              "명확 + <b>연계 2</b>", "이메일 <b>25명 + projector</b> → 표: 30석 + Yes = Room C", "선지 4개가 표에 연달아 = 지문 속 선지. D는 좌석만 맞고 프로젝터 No"),
             (163, "According to the chart, what is true about all the meeting rooms?", ["They have projectors.", "They close at the same time.", "They seat at least 20 people.", "They must be reserved by phone."], 1,
              "불명확", "B ✓ <b>All rooms close at 8:30 P.M.</b> (표 아래 줄) / A ✗ A·D는 No / C ✗ A는 10석", "표 밖 한 줄(하단)이 근거 (178 유형)")]),
]
L = "ABCD"


def tbl(rows):
    t = Table([[P(c, C) for c in r] for r in rows], colWidths=[W * 0.46 - 8 * mm] + [(W * 0.54) / (len(rows[0]) - 1)] * (len(rows[0]) - 1))
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def box(parts):
    cells = [[tbl(x[1]) if isinstance(x, tuple) else P(x, B)] for x in parts]
    t = Table(cells, colWidths=[W])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, colors.black), ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.grey),
                           ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def qblock(n, stem, opts, p7=False):
    tag = "□명 □불 &nbsp; O △ ?" if p7 else "O △ ?"
    rows = [[P(f"<b>{n}.</b> {stem}", Q), P(tag, S)]] + [[P(f"({L[i]}) {o}", Q), ""] for i, o in enumerate(opts)]
    t = Table(rows, colWidths=[W - 34 * mm, 34 * mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1), ("LEFTPADDING", (0, 1), (0, -1), 14)]))
    return KeepTogether([t, Spacer(1, 3 * mm)])


out = ROOT / "data" / "workbook"
doc = SimpleDocTemplate(str(out / "Algo_Drill_01.pdf"), pagesize=A4, leftMargin=LM, rightMargin=LM, topMargin=12 * mm, bottomMargin=12 * mm, title="알고리즘 드릴 01")
s = [P("알고리즘 드릴 01 (31문항 · 권장 25분)", T), Spacer(1, 2 * mm),
     P("<b>푸는 법</b> · P5: 문장 보기 전에 <b>선지 생김새</b>로 문법 / 전·접·부 / 어휘 판정 → 빈칸 앞뒤에서 가장 가까운 것 · "
       "P6 문장삽입: 대명사·also 있는 선지 1순위 → 받아주는 말 · P7: 문제만 먼저 잡고 <b>명/불</b> 체크. 명확 = 주관식 답 먼저, 불명확 = 선지 ✓✗ · "
       "다중지문: 내려가기 전에 <b>피자 꼬투리</b>(안 쓰인 숫자·고유명사)에 표시 · 문항마다 확신도 <b>O △ ?</b>", B), Spacer(1, 2 * mm),
     P("시작 ____ : ____ &nbsp;&nbsp; P5 끝 ____ : ____ &nbsp;&nbsp; P6 끝 ____ : ____ &nbsp;&nbsp; 153 끝 ____ : ____ &nbsp;&nbsp; 끝 ____ : ____", B), Spacer(1, 4 * mm), P("PART 5", H), Spacer(1, 2 * mm)]
for n, stem, opts, *_ in P5:
    s.append(qblock(n, stem, opts))
s += [PageBreak(), P("PART 6", H), P("Questions 131-134 refer to the following notice.", B), Spacer(1, 2 * mm), box([P6_TEXT]), Spacer(1, 3 * mm)]
for n, stem, opts, *_ in P6:
    s.append(qblock(n, stem, opts))
s += [PageBreak(), P("PART 7", H)]
for i, st_ in enumerate(SETS):
    if i:
        s.append(PageBreak())
    s += [P(st_["head"], B), Spacer(1, 2 * mm)]
    for part in st_["text"]:
        s += [box([part]), Spacer(1, 2.5 * mm)]
    for n, stem, opts, *_ in st_["qs"]:
        s.append(qblock(n, stem, opts, True))
doc.build(s)

# ---- answers ----
doc = SimpleDocTemplate(str(out / "Algo_Drill_01_Answers.pdf"), pagesize=A4, leftMargin=LM, rightMargin=LM, topMargin=12 * mm, bottomMargin=12 * mm, title="알고리즘 드릴 01 정답·해설")
allq = P5 + P6 + [q for st_ in SETS for q in st_["qs"]]
a = [P("알고리즘 드릴 01: 정답과 알고리즘 해설", T), Spacer(1, 2 * mm), P("채점 전에 보지 마. 다 풀고 열어.", S), Spacer(1, 3 * mm)]
key = [[P(f"<b>{q[0]}</b> {L[q[3]]}", C) for q in allq[i:i + 8]] + [""] * (8 - len(allq[i:i + 8])) for i in range(0, len(allq), 8)]
kt = Table(key, colWidths=[W / 8] * 8)
kt.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey)]))
a += [kt, Spacer(1, 4 * mm), P("해설 읽는 법: <b>유형 → 알고리즘대로 볼 곳 → 함정</b>. 틀린 문제는 '어느 단계에서 어긋났나'를 한 줄로 적어.", B), Spacer(1, 3 * mm)]
rows = [[P(h, CB) for h in ("번호", "정답", "알고리즘 유형", "알고리즘대로 볼 곳", "함정 / 형 과거 오답")]]
for q in allq:
    rows.append([P(str(q[0]), CB), P(f"<b>{L[q[3]]}</b>", C), P(q[4], C), P(q[5], C), P(q[6], C)])
t = Table(rows, colWidths=[11 * mm, 10 * mm, 30 * mm, 72 * mm, W - 123 * mm], repeatRows=1)
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9d9d9")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
a += [t, Spacer(1, 4 * mm), P("채점 후 분류", H),
      P("· <b>O인데 틀림</b> = 함정·서두름 (제일 중요) · <b>△인데 틀림</b> = 선지 비교 · <b>?인데 틀림</b> = 어휘·해석 · <b>명/불 판정이 틀린 문제</b>는 따로 표시", B)]
doc.build(a)
from collections import Counter
print(len(allq), "items", Counter(L[q[3]] for q in allq))
