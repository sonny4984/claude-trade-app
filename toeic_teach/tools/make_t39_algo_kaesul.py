"""TEST 39 알고리즘 해설지: 문항마다 data/rc_algorithm.md의 단계 그대로 (유형 판정 → 볼 곳 → 풀이 → 소거 → 형 과거 오답).
Usage: python3 tools/make_t39_algo_kaesul.py -> data/workbook/RC_Test39_알고리즘해설.pdf"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

ROOT = Path(__file__).resolve().parent.parent
F = str(ROOT / "tools/fonts") + "/"
pdfmetrics.registerFont(TTFont("N", F + "NanumGothic-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NB", F + "NanumGothic-Bold.ttf"))
registerFontFamily("N", normal="N", bold="NB", italic="N", boldItalic="NB")
st = lambda n, f, s, l, **k: ParagraphStyle(n, fontName=f, fontSize=s, leading=l, **k)
T, H, K, KS, C, CB = st("t", "NB", 17, 23), st("h", "NB", 12.5, 17), st("k", "N", 9.5, 14.5), st("ks", "N", 8.3, 12), st("c", "N", 8.8, 13), st("cb", "NB", 8.8, 13)
LM = 15 * mm
W = A4[0] - 2 * LM
P = Paragraph
BLUE, GREY = colors.HexColor("#e9eef7"), colors.HexColor("#f4f4f4")


def item(no, ans, typ, steps, elim, past):
    rows = [[P(f"<b>{no}</b>", st("n", "NB", 12, 15)), P(f"정답 <b>{ans}</b> &nbsp;|&nbsp; <b>유형 판정:</b> {typ}", C)],
            [P("알고리즘<br/>풀이", CB), P("<br/>".join(f"{i}. {x}" for i, x in enumerate(steps, 1)), C)],
            [P("소거", CB), P(elim, C)],
            [P("형 과거 오답", CB), P(past, C)]]
    t = Table(rows, colWidths=[20 * mm, W - 20 * mm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), BLUE), ("BACKGROUND", (0, 1), (0, -1), GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return KeepTogether([t, Spacer(1, 3.5 * mm)])


def setbox(title, lines):
    t = Table([[[P(f"<b>{title}</b>", C)] + [P("· " + x, C) for x in lines]]], colWidths=[W])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, colors.HexColor("#1a4fa0")), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7f9fd")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return [t, Spacer(1, 3.5 * mm)]


s = [P("TEST 39 알고리즘 해설", T), Spacer(1, 2 * mm),
     P("형이 보내준 RC 알고리즘(강의 슬라이드)과 과외 팁의 <b>단계 이름 그대로</b> 풀이를 썼어. 문항마다 ① 유형 판정 ② 알고리즘 순서대로 한 풀이 ③ 선지 소거 ④ 같은 유형의 형 과거 오답 순서야.", K), Spacer(1, 3 * mm)]
ov = [["파트", "알고리즘 요약"],
      ["Part 6", "우선 읽는다 + 문법으로 풀리는 건 받아먹는다. <b>파트5 유형</b>(문법: 선 문법 후 해석 / 동사자리 = 99% 시제 / 어휘 = 99% 해석) · <b>접속부사</b>(자리 [. ___ ,] 확인 → 역접·인과·추가) · "
       "<b>문장삽입</b>(대명사·지시어·정관사 The·also 있는 선지 1순위 → 앞에서 '받아주는 말' / 없으면 문단 통일성)"],
      ["Part 7 단일", "<b>대전제:</b> 99%는 위에서부터 문항 순서대로 풀린다 (예외: 목적, 문장삽입). ① 왼쪽 문제만 잡는다 ② 문단 개수 파악, 한 문단당 한 문제 목발보행 ③ 첫 문단 읽고 바로 첫 문제 ④ 풀리면 다음 문제, 안 풀리면 한 덩어리만 더. "
       "<b>불명확</b>(What is -ed about, 목적, NOT) → 문단 전체 + 선지 진위판단 / <b>명확</b> → 요구사항만 읽다가 '나왔다' → 주관식 답 → 선지에서 위치만"],
      ["정답 위치", "<b>숫자정보 &gt;&gt;&gt; 고유명사 &gt;&gt;&gt;&gt; 기타.</b> 여러 개가 연달아 나오면(2~6개, 4개에 가까울수록) '지문 속 선지'. 그중 설명이 붙은 것(딸기)이 정답"],
      ["Part 7 다중", "<b>대전제:</b> 정답 근거는 지문 전체에 균일하게 분포, 안 쓰인 빈 공간은 반드시 다시 채우러 온다. 첫 지문은 단일지문처럼 → 내려가기 전 <b>피자 꼬투리</b>(하단 &gt; 상단 &gt; 중간, 숫자 문장 우선) 확인 → "
       "재출현하면 즉시 풀이. 선지가 다른 지문 내용이면 강제연계. 이중 1개 / 삼중 2개"],
      ["과외 팁", "소거법 · 순서 P5 → 다중 → P6 → 단일 · 모르는 단어 vs 아는 단어면 아는 단어 · 명사의 범위 확인 · 명사가 2개면 첫 번째 명사"]]
t = Table([[P(c, CB if i == 0 else C) for c in r] for i, r in enumerate(ov)], colWidths=[24 * mm, W - 24 * mm])
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9d9d9")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
s += [t, Spacer(1, 3 * mm),
      P("정답표: 131 D · 132 D · 133 C · 134 C · 135 A · 136 A · 137 B · 138 D · 151 C · 152 D · 172 C · 173 A · 174 A · 175 D · 176 D · 177 C · 178 A · 179 C · 180 C · "
        "186 C · 187 B · 188 D · 189 B · 190 C · 191 A · 192 D · 193 A · 194 A · 195 D", KS)]

# ---------------- Part 6
s += [PageBreak(), P("PART 6 · 131–134 (공지)", H)]
s += setbox("세트 읽는 법", ["처음부터 읽으면서 빈칸을 만날 때마다 '문법으로 바로 풀리나?'를 본다.", "문장삽입(134)은 맨 끝이라 지문을 다 읽은 뒤에 푼다."])
s += [item(131, "D cleanliness", "파트5 유형 → <b>문법 문제</b> (선지가 clean의 꼬다리만 다름)",
           ["빈칸 앞뒤에서 가장 가까운 것: 앞 <b>전치사 of</b>, 뒤 <b>전치사 to</b>.", "두 슬래시 사이 = <b>of / ___ / to</b> → 전치사 뒤 = 명사 자리.", "-ness = 명사 → cleanliness."],
           "clean(형/동), cleanly(부), cleaned(p.p.)는 전치사 뒤에 단독으로 못 옴.", "T1-101 regional, T1-125 substitutions (꼬다리 문제를 해석으로 풀다 틀림)"),
      item(132, "D During", "파트5 유형 → <b>전/접/부 문제</b>, 선지가 전부 전치사 → <b>전치사 통일 = 용법</b>",
           ["빈칸 뒤 = this period(명사구, 기간).", "기간 명사 앞에서 '~동안' = During."],
           "Among(셋 이상 사이), Between(둘 사이), Without(~없이)은 기간과 안 맞음.", "T1-114 for the past three years (전치사 용법)"),
      item(133, "C apologize", "파트5 유형 → <b>어휘 문제</b> (품사 같고 생김새 다름) → 동사 어휘 = 목적어·전치사 확인",
           ["빈칸 뒤: <b>for</b> any inconvenience → 목적어 없이 for가 붙는 자동사.", "apologize for = ~에 대해 사과하다."],
           "organize·recognize·summarize는 목적어가 바로 와야 하는 타동사.", "t37-104 refrain from (자동사 + 전치사 짝)"),
      item(134, "C (문의는 프런트로)", "<b>문장삽입</b>",
           ["삽입할 문장에 대명사·지시어·정관사·also가 있나? → 'these days', 'the second-floor showers', 'the lobby' 선지가 1순위 후보.",
            "받아주는 말 + <b>지문과 모순 여부</b> 확인: '2층 샤워실을 쓰지 마라' ↔ 지문 'should use the showers on the second floor' → <b>모순</b>.",
            "'로비 페인트칠' → 지문에 없는 사실.", "남은 것 중 문단 통일성: 사과 문장 뒤 공지의 마무리 = 문의처 안내."],
           "트레이너 지원 안내는 주제(청소 공지)와 무관.", "T1-134 (north lobby 접근 금지 = 모순 선지를 고름)")]
s += [P("PART 6 · 135–138 (후기)", H),
      item(135, "A quickly", "파트5 유형 → <b>문법 문제</b>",
           ["가장 가까운 것: 앞 <b>ed</b>(repaired) + as ___ as.", "repaired(동사)를 꾸미는 자리 → 부사. as + 부사 + as possible."],
           "quicken(동), quickest(최상급), quickness(명) 탈락.", "T1-119 consistently applied"),
      item(136, "A even though", "파트5 유형 → 전/접/부, 뒤가 <b>문장</b>(several customers were waiting) → 접속사 → 접속사끼리는 <b>해석</b>",
           ["앞: 바로 봐 줬다 / 뒤: 손님 여럿이 기다리고 있었다 → 양보 '~인데도'."],
           "such as·as far as는 뜻이 안 맞고, whether(~인지)는 명사절.", "t16-141 although (in case 고름, 3회)"),
      item(137, "B (그 바퀴는 그 뒤로 완벽하다)", "<b>문장삽입</b>",
           ["정관사 <b>The wheel</b> → 앞에서 받아주는 말 = my bicycle's rear wheel ✓.", "바로 앞 '다음 날 아침에 다 됐다' → 수리 결과로 자연스럽게 이어짐."],
           "'월요일 휴무', '3년 전에 샀다', '헬멧도 팔았다'는 받아주는 말이 없거나 흐름과 무관.", "T4-136, t37-133 (This rate가 받는 말)"),
      item(138, "D skilled", "파트5 유형 → 어휘 문제지만 <b>수식어 순서(한정사 + 형용사 + 명사)</b>부터",
           ["빈칸 앞 한정사 <b>a</b> → 최상급 best는 the가 필요 → 탈락.", "문맥: 칭찬 → former(전직), temporary(임시) 탈락 → skilled."],
           "뜻이 둘 다 될 때는 관사로 가른다.", "T1-138 a superb tailor (best 고름)")]

# ---------------- 151-152
s += [PageBreak(), P("PART 7 · 151–152 (보고서)", H)]
s += setbox("세트 읽는 법 (단일지문 알고리즘)", ["① 문제만 잡기: 151 What is true about the test? = <b>불명확</b> / 152 What did testers have difficulty doing? = <b>명확</b>.",
                                    "② 문단 파악: 헤더(날짜·인원) / Overview / Initial findings. 헤더의 <b>숫자정보</b>는 출제 1순위.",
                                    "③ Overview의 task 1~4 = 고유 항목 4개가 연달아 = <b>지문 속 선지</b>."])
s += [item(151, "C (하루 넘게 진행)", "<b>불명확</b> (What is true about ~) → 해당 부분 전체 + 선지 4개 진위판단",
           ["헤더의 숫자정보부터: Test period: <b>March 24–26</b> → 3일 → 'lasted more than one day' ✓.", "정답은 숫자를 일반적인 말로 바꿔 씀 (24–26 → more than one day)."],
           "'두 버전 비교' ✗ (Parkwise 3.1 하나) / 'in a parking garage' ✗ (parking garage는 과제 내용 = 단어 재사용) / 'questionnaire' ✗ (과제 수행이지 설문 아님).",
           "T1-151 (concert 단어를 보고 '콘서트에서 진행' 고름)"),
      item(152, "D Extending a booking", "<b>명확</b> → 주관식 답 먼저",
           ["요구사항 '어려웠던 것'만 찾으며 읽기 → Initial findings: <b>Task 4</b> caused the most trouble. '나왔다' → 읽기 중지.",
            "Task 4가 뭔지 번호로 확인: added time to an existing reservation.", "주관식 답 '예약 시간 연장' → 선지에서 위치만 찾기: Extending a booking."],
           "Finding a garage(task 1), Reserving a space(task 2), Making a payment(task 3) = 번호 바꿔치기 함정.", "T1-152 (task 2와 3을 혼동)")]

# ---------------- 172-175
s += [P("PART 7 · 172–175 (온라인 채팅)", H)]
s += setbox("세트 읽는 법", ["문제 잡기: 172 업종(명확) / 173 의도 / 174 What is indicated about Ms. Okoye(불명확) / 175 Mr. Lund가 알고 싶은 것(명확).",
                        "채팅은 위에서부터 문항 순서대로 풀림. 의도 문제는 그 시각 <b>바로 앞 대사</b>가 근거."])
s += [item(172, "C An architecture firm", "<b>명확</b>",
           ["요구사항 '업종' → 10:03 'our <b>building plans</b>', 10:05 '<b>architecture</b> … our hotel projects'.", "주관식 답: 건축 설계 회사."],
           "furniture, theater(stage), hotel은 지문 단어 재사용. hotel은 고객의 프로젝트.", "T1-172"),
      item(173, "A (요청을 기꺼이 하겠다)", "<b>의도 파악</b>",
           ["10:07 바로 앞(10:06): '두 번째 면접을 잡아 줄래? 바쁜 날에 무리한 부탁이 아니면 좋겠는데'.", "No trouble at all = 전혀 문제없다 → 부탁을 하겠다는 뜻."],
           "'연락이 쉬웠다', '면접이 순조로웠다'는 trouble 단어에 끌리는 선지.", "t16-174, t34-149 (의도: 바로 앞 문장)"),
      item(174, "A (여러 분야 경력)", "<b>불명확</b> → 선지 진위판단",
           ["10:05 'worked in <b>furniture design and stage design as well as architecture</b>' → 여러 분야 ✓.", "분야 3개가 연달아 = 숫자·고유명사급 정보."],
           "'호텔 설계 경험' ✗ (호텔은 회사 일) / 'Ms. Park과 일했다' ✗ / '혼자 일한 적 없다' ✗ (freelance work와 반대).", "T1-174 varied work history"),
      item(175, "D (회사에 계속 다닐 것인지)", "<b>명확</b>",
           ["요구사항 'Mr. Lund가 알고 싶은 것' → 10:09에서 Mr. Lund 등장. '나왔다'.",
            "병렬 주의: Mr. Lund <b>will ask</b> why ~ / He'<b>ll also want</b> to be sure she isn't planning to move on after a year or two.",
            "주관식 답: 1~2년 뒤에 안 떠날지 → stay with the company."],
           "'바로 시작 가능', '팀 관리 경험'은 근거 없음. 'Thursday'는 면접 일정(단어 재사용).", "T1-175 (and will stick around 병렬을 놓쳐 C 고름)")]

# ---------------- 176-180
s += [PageBreak(), P("PART 7 · 176–180 (기사 + 편지, 이중지문)", H)]
s += setbox("세트 읽는 법 (다중지문 알고리즘)", ["문제를 잡을 때 <b>몇 번째 지문</b>인지도 잡기: 176·177·178 = 기사 / 179·180 = 편지.",
                                    "첫 지문은 단일지문처럼. 내려가기 전 <b>피자 꼬투리</b>: 맨 위 'June issue', 맨 아래 굵은 줄(독자 팁 모집). 하단이 발견 확률 1위.",
                                    "이중지문 연계는 1개 → 여기서는 179."])
s += [item(176, "D Buying a monthly pass", "<b>불명확 (NOT)</b> → 선지 4개 모두 ✓✗",
           ["Comfort: 'a seat away from the doors' ✓", "Health: 'Get off one stop early and walk' → Walking part of the way ✓ (표현 바뀜)", "Productivity: 'recorded books or language lessons' ✓", "정기권은 어디에도 없음 ✗ → 정답."],
           "지문 단어와 다르다고 지우지 말 것. 뜻이 같으면 ✓.", "T1-176 (during이 다르다는 이유로 B를 NOT으로 고름)"),
      item(177, "C (파일을 미리 저장해야 하는 이유)", "<b>명확</b>",
           ["문제의 키워드 unreliable connections 위치 찾기 → 'Save documents ~ before you leave home, <b>since</b> connections are often unreliable'.", "since = 이유 → 주관식 답: 미리 저장하라는 이유."],
           "다른 노선 추천, 지연 경고, 재택 권유는 근거 없음.", "since를 '~이후로'로 읽은 적 있음 (해석 5번 문장)"),
      item(178, "A (독자 제안을 실을 계획)", "<b>불명확</b>",
           ["본문에서 안 풀림 → 피자 꼬투리(맨 아래 굵은 줄): 'Send it to us, and we will <b>print the best ones in our July issue</b>'.", "→ 독자 제안 게재 ✓."],
           "'열차에서 무료 배포', '철도 회사 발행', '7월호 뒤 폐간'은 근거 없음(July 단어 재사용).", "T1-178 (맨 아래 박스를 안 읽음)"),
      item(179, "C (최근 호를 읽었다)", "<b>불명확 + 연계</b> (이중지문 연계 1개)",
           ["편지 첫 문장: 'Your article on commuting described my mornings exactly'.", "꼬투리 재출현: 기사 = Midlands Commuter <b>June issue</b>의 통근 기사 → 그 호를 읽음."],
           "'전문 작가' ✗ / '창업자' ✗ (the company I <b>work for</b> = 직원) / '재택근무' ✗ (통근한다).", "T1-179"),
      item(180, "C (들고 다니기 쉽다)", "<b>불명확</b>",
           ["숫자정보: 'weighs just <b>400 grams</b> and folds flat enough to <b>fit in a coat pocket</b>' → easy to carry."],
           "가격·계절 한정·재활용 소재는 언급 없음 ('every season'은 신제품 추가 시기).", "T1-180 packable")]

# ---------------- 186-190
s += [PageBreak(), P("PART 7 · 186–190 (주문 확인서 + 공지 + 이메일, 삼중지문)", H)]
s += setbox("세트 읽는 법", ["문제별 지문: 186 주문서 / 187 Mr. Reyes(불명확, 연계 의심) / 188 공지 / 189·190 이메일.",
                        "주문서의 꼬투리 = <b>표의 책 4권과 가격(숫자 4개 = 지문 속 선지)</b>, '결제는 당일 카드'. 표는 줄줄 읽지 말고 눈알굴리기, 항목 이름만 기억.",
                        "삼중지문 연계는 2개 → 187, 190."])
s += [item(186, "C Gardening", "<b>명확</b>", ["주문서 첫 문단: 'Ms. Okafor's <b>gardening guides</b>' + 책 제목(Vegetables, Soil, Pruning, Herbs)."],
           "Cooking(Herbs·Harvests에 끌림), Bookbinding(책에 끌림)은 단어 연상 함정.", "T1-186 graphic-design books"),
      item(187, "B (책 한 권을 무료 우편으로 받는다)", "<b>불명확 + 연계 1</b>",
           ["Mr. Reyes에 관한 사실은 여러 개 → 선지 진위판단.", "꼬투리 재출현: 공지의 <b>Soil Basics</b> = 표에서 Mr. Reyes가 주문한 책.", "공지: 'sent to your home <b>at no cost to you</b>' → 무료 우편 ✓."],
           "'워크숍 전에 결제' ✗ → 결제는 당일(registration table) + 그 책은 <b>when it ships</b>(발송 시). 'Ms. Fischer와 참석', '강연'은 근거 없음.",
           "T1-187 (charge your card를 '이미 결제'로 읽어 D 고름)"),
      item(188, "D To explain a problem", "<b>불명확 (목적)</b>", ["공지 첫 문장: 책이 제때 도착하지 않았다 → 문제 설명. 목적은 첫 문장에서 풀리면 바로 답."],
           "자원봉사자 모집, 신간 광고, 일정 변경은 없음.", "T1-188"),
      item(189, "B (용기를 놓을 위치)", "<b>명확</b>", ["이메일: 'I would like to <b>rethink where the containers will go</b>' → 주관식 답: 화분 위치.", "선지의 바뀐 표현: placement of some containers."],
           "'회의 날짜'(Friday 재사용), '식물 가격'(order any plants 재사용), '정원 크기'는 범위·대상이 다름.", "T1-189"),
      item(190, "C $15.00", "<b>명확 + 연계 2</b> (선지가 표의 숫자 4개 = 강제연계)",
           ["이메일에서 '빌려준 책'의 설명: 'raising <b>vegetables where room is limited</b>'.", "표에서 내용이 맞는 제목: <b>Small Spaces, Big Harvests: Growing Vegetables on a Balcony</b>.", "그 줄의 Member price = <b>$15.00</b>."],
           "$12.00(Soil Basics), $18.00(Pruning·Herbs 합계), $9.00(Herbs 한 권). Price($20)와 Member price 열을 헷갈리지 말 것.",
           "T1-190 (책 내용과 제목을 안 이어서 $16.00 고름)")]

# ---------------- 191-195
s += [PageBreak(), P("PART 7 · 191–195 (기사 + 이메일 + 표, 삼중지문)", H)]
s += setbox("세트 읽는 법", ["문제별 지문: 191·192 기사 / 193 이메일(Corvin에 관해 = 연계 의심) / 194 이메일 / 195 표(선지 = 유닛 4개 = 강제연계).",
                        "기사의 꼬투리: <b>날짜 9 November</b>, 'building permit … <b>suspended</b>', Dock Street warehouses.",
                        "이메일의 꼬투리: <b>3 March</b>, 'finished in June', '<b>at least 100 square metres</b>'."])
s += [item(191, "A (프로젝트 진행 상황 알림)", "<b>불명확 (목적)</b>", ["제목 'Plan Stalls' + 첫 문장 'has run into further delays' → 프로젝트 근황."],
           "상점의 장점 설명, 새 정책 발표, 입찰 초대는 아님.", "T1-191"),
      item(192, "D (이전 건물 작업을 꼼꼼히 했다)", "<b>명확</b>",
           ["Ms. Lindqvist의 말 중 Corvin 칭찬 부분만: 'how <b>carefully</b> the company <b>restored the Dock Street warehouses</b>'.", "주관식 답: 예전 복원 작업의 질."],
           "낮은 임대료, 환경 기준, 도로 비용 부담은 근거 없음(road는 협상 주제 = 단어 재사용).", "T1-192"),
      item(193, "A (필요한 허가를 받았다)", "<b>불명확 + 연계 1</b>",
           ["이메일(3 March): 'your work on Harbor Mill <b>will be finished in June</b>' → 공사가 진행 중.", "꼬투리 재출현: 기사(9 November)에서는 building permit이 <b>suspended</b>.", "보류 → 공사 진행 = 그 사이 허가가 나왔다."],
           "'사무실 이전', '페리 터미널 소유', '신생 회사'는 근거 없음.", "T1-193 (날짜 두 개를 안 이어서 B 고름)"),
      item(194, "A (배송을 받을 장소)", "<b>명확</b>", ["이메일의 질문 문장만: 'Is there a <b>delivery area</b> behind the building ~?'"],
           "'페리 터미널까지 거리'(이미 옆이라고 앎), '다른 세입자', '완공일'(이미 6월이라고 들음)은 묻지 않음.", "T1-194"),
      item(195, "D G4", "<b>명확 + 연계 2</b> (숫자정보)",
           ["이메일 조건: ground-floor + <b>at least 100 square metres</b>.", "표에서 100 이상: G2(105), G4(110).", "조건 줄 확인(명사의 범위): G2는 <b>Leased</b> → 탈락 → Available인 G4."],
           "G1(60)·G3(75)은 면적 미달. G2는 면적만 맞고 이미 임대됨 = 한정어 함정.", "T1-195, t23-178 (좌석·기간 조건을 하나만 봄)")]

s += [Spacer(1, 3 * mm), P("이 세트에서 가져갈 것", H)]
for x in ["P6 문장삽입: 대명사·the 선지를 먼저 보되 <b>지문과 모순</b>이면 바로 탈락 (134).",
          "불명확 문제의 근거는 <b>헤더·맨 아래 줄</b>에도 있다 (151, 178).",
          "명확 문제는 <b>주관식 답 먼저</b>. 번호·이름이 연달아 나오면 번호로 확인 (152, 175).",
          "다중지문: 날짜·숫자·책 제목 같은 꼬투리를 다음 지문과 잇는다. 표에서는 <b>조건 열(Leased, Member price)</b>까지 본다 (187, 190, 193, 195)."]:
    s.append(P("□ " + x, K))
out = ROOT / "data/workbook/RC_Test39_알고리즘해설.pdf"
SimpleDocTemplate(str(out), pagesize=A4, leftMargin=LM, rightMargin=LM, topMargin=13 * mm, bottomMargin=13 * mm, title="TEST 39 알고리즘 해설").build(s)
print(out)
