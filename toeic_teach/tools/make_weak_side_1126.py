"""11/26 약점 메우기 103-137 (21/35): 오답 14 + 질문 6: 왼쪽 문제, 오른쪽 자세한 해설(동하 메모 질문에 답) -> data/workbook/Weak_Side_1126.pdf"""
import random, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from weak_fill_items import CH
pdfmetrics.registerFont(TTFont("S", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("SB", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("K", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("S", normal="S", bold="SB", italic="S", boldItalic="SB")
registerFontFamily("K", normal="K", bold="K", italic="K", boldItalic="K")
st = lambda f, s, l, c="#000000": ParagraphStyle("x", fontName=f, fontSize=s, leading=l, textColor=colors.HexColor(c))
L = "ABCD"
items = []
for ci, (title, tip, its) in enumerate(CH):
    for ii, (stem, opts, rule, src) in enumerate(its):
        order = list(range(4)); random.Random(1000 * ci + ii + 7).shuffle(order)
        items.append((stem, [opts[i] for i in order], order.index(0)))


MINE = {106: None, 107: "as", 108: "at", 109: "at", 110: "at", 112: "since", 114: "in case", 115: "unless", 116: "into", 117: "onto",
        123: "during", 131: "None", 132: "anyone", 135: None,
        113: "throughout", 122: "in", 126: "besides", 127: "in spite of", 130: "those", 136: "whom"}
EX = {
 106: ["<b>해석</b> 그 회사의 사명은 이익을 <b>넘어</b> 지역사회 봉사까지 포함하도록 확장된다.",
       "<b>선지</b> among ~사이에(여럿) / before ~전에 / <b>beyond ~을 넘어서</b> / through ~을 통해",
       "<b>핵심</b> extend <b>beyond</b> A to include B = A를 넘어 B까지 넓히다. 이익(profit)에서 끝나지 않고 그 너머로 간다는 뜻.",
       "<b>네 메모 '뭐가 들어가도 틀린 느낌'</b> → 이건 뜻이 아니라 <b>짝</b>이야. extend beyond / go beyond / beyond expectations(기대 이상).",
       "beyond에 X를 쳤어. 정답을 지울 땐 이유 한 단어라도 붙이기."],
 107: ["<b>해석</b> 모든 불만 사항은 <b>서면으로</b> 제출되어야 한다.",
       "<b>선지</b> to ~에게 / <b>in ~으로(방식)</b> / for ~을 위해 / as ~로서",
       "<b>핵심</b> <b>in writing</b> 서면으로 ↔ <b>in person</b> 직접(대면으로). 방식은 in: in cash 현금으로, in English 영어로.",
       "as는 '~로서(자격)': work as a manager. writing(글쓰기)이 자격이 될 순 없어."],
 108: ["<b>해석</b> 직원 파티는 12월 12일 금요일<b>에</b> 열린다.",
       "<b>선지</b> at 시각 / <b>on 요일·날짜</b> / to ~로 / in 월·연도·계절",
       "<b>핵심 시간 전치사 3단</b> at + 시각(at 3 P.M., at noon) / <b>on + 요일·날짜</b>(on Friday, on December 12) / in + 월·연도·계절(in May, in 2027).",
       "Friday, December 12 = 요일 + 날짜 → 무조건 on."],
 109: ["<b>해석</b> Kim 박사는 재생에너지의 최근 동향<b>에 관해</b> 강연할 것이다.",
       "<b>선지</b> <b>on ~에 관한(주제)</b> / to ~에게 / by ~에 의해 / at ~에서",
       "<b>핵심</b> lecture / talk / report / decision / information / seminar <b>on</b> + 주제 = ~에 관한. (about과 같은 뜻)",
       "TEST 21·26에서도 틀린 포인트야 (3회째). 짝 카드에 추가."],
 110: ["<b>해석</b> 그 가게는 평일 오전 9시<b>부터</b> 오후 8시까지 영업한다.",
       "<b>선지</b> on / at / since ~이후로 / <b>from ~부터</b>",
       "<b>핵심</b> 뒤에 <b>until</b> 8 P.M.이 있어 → 짝 <b>from A until(to) B</b>. 빈칸 뒤쪽 단어까지 보기.",
       "at 9 A.M.만 보면 at이 끌리지만, until이 짝을 정해 줘."],
 112: ["<b>해석</b> 성과 평가는 매 분기 말<b>에</b> 이루어진다.",
       "<b>선지</b> <b>at</b> / onto ~위로 / since ~이후로 / until ~까지",
       "<b>핵심</b> <b>at the end of</b> / at the beginning of = 덩어리로 외우기.",
       "<b>네 메모 '~이후로?'</b> → since는 '그때 이후로 쭉'이라 현재완료랑 써 (has worked since 2020). 여기는 현재형 take place + 매 분기 말이라는 <b>시점</b> → at."],
 114: ["<b>해석</b> 일요일에 수리가 끝나지 <b>않으면</b>, 가게는 월요일에 일찍 문을 닫을 것이다.",
       "<b>선지</b> so that ~하도록 / <b>unless ~하지 않으면</b> / in case ~할 경우에 대비해 / as though 마치 ~처럼",
       "<b>네 메모 'if not으로 푼 것 같은데'</b> → 맞아, unless = if not. 그걸 알고 in case를 고른 거야.",
       "<b>in case ≠ if not.</b> in case = <b>혹시 ~할 때를 대비해서</b>: Take an umbrella in case it rains(비 올 경우를 대비해).",
       "넣어 보기: '수리가 끝날 경우를 대비해 일찍 닫는다' → 말이 안 돼. '수리가 안 끝나면 일찍 닫는다' → unless."],
 115: ["<b>해석</b> 오용으로 생긴 것<b>을 제외한</b> 모든 수리 비용은 보증으로 처리된다.",
       "<b>선지</b> otherwise 그렇지 않으면(부사) / <b>except ~을 제외하고(전치사)</b> / unless ~하지 않으면(접속사) / instead 대신에(부사)",
       "<b>핵심</b> 빈칸 뒤 <b>those caused by misuse</b> = 명사구(동사 없음, caused는 분사) → 전치사 → except.",
       "unless는 접속사라 뒤에 주어 + 동사가 와야 해. 선지 품사가 섞이면 → 빈칸 뒤 동사 유무부터."],
 116: ["<b>해석</b> 그 호텔 식당은 여러 나라<b>에서 온</b> 요리를 제공한다.",
       "<b>선지</b> into ~안으로 / <b>from ~에서(출처)</b> / through ~을 통해 / over ~위에",
       "<b>핵심</b> 출처·출신은 from: dishes from many countries, a letter from Ms. Kim, people from Asia.",
       "from에 X를 치고 into를 골랐어. into는 '안으로 들어가는 이동'(walk into the room)이라 요리랑 안 맞아."],
 117: ["<b>해석</b> 보너스는 영업팀 다섯 명<b>에게</b> 똑같이 나뉠 것이다.",
       "<b>선지</b> onto ~위로 / <b>among ~사이에(셋 이상)</b> / about ~에 관해 / beside ~옆에",
       "<b>핵심</b> divide / share / distribute <b>among</b> + 여럿(셋 이상). 둘이면 <b>between</b>.",
       "<b>네 메모 'onto + 숫자 뜻?'</b> → onto는 '~위로 (올라가는 이동)'뿐이야: jump onto the stage. 숫자랑 상관없어."],
 123: ["<b>해석</b> Gomez 씨는 5년 <b>동안</b> 디자인팀을 이끌어 왔다.",
       "<b>선지</b> <b>for + 기간</b> / during + 특정 기간 명사 / lately 최근에(부사) / since + 시점",
       "<b>네 질문 '현재완료 + 기간인데 since는 왜 안 돼?'</b> → since 뒤에는 <b>시점</b>이 와: since 2021, since last year, since she joined.",
       "<b>five years는 기간</b>이야 → for. 현재완료(has led)가 있다고 since가 되는 게 아니라, <b>뒤 명사가 시점이냐 기간이냐</b>로 갈려.",
       "during은 during the meeting / during the summer처럼 '그 기간 중에'라 숫자 기간(five years)이랑은 안 써."],
 131: ["<b>해석</b> 두 제안 중 <b>어느 것도</b> 이사회에서 승인되지 않았다.",
       "<b>선지</b> Nothing 아무것도(of 못 받음) / None 아무것도(셋 이상) / <b>Neither 둘 다 아님</b> / Nobody 아무도(사람)",
       "<b>핵심</b> of the <b>two</b> → Neither / of the three, of all → None. 숫자 two가 단서.",
       "같은 계열: either(둘 중 하나) / both(둘 다) / neither(둘 다 아님)."],
 132: ["<b>해석</b> 고객 설문을 완료하는 <b>사람 누구에게나</b> 기프트 카드가 주어진다.",
       "<b>선지</b> those (who complete) / <b>whoever = anyone who</b> / who / anyone (who 필요)",
       "<b>핵심</b> 전치사 to 뒤 빈칸 + 바로 동사 <b>completes</b>(단수) → 빈칸 혼자 '주어 + 명사' 역할 → whoever.",
       "anyone을 넣으면 'to anyone completes' → who가 없어서 동사를 못 붙여. anyone <b>who</b> completes여야 해.",
       "those는 복수라 complete가 와야 하고 역시 who 필요. 반복 오답 (3회째): <b>to ___ + 동사 = whoever</b>."],
 135: ["<b>해석</b> 새 정책은 우리 영업시간을 바꾸지 않을 것이고, 가격에도 영향을 주지 <b>않을</b> 것이다.",
       "<b>선지</b> also 또한(긍정, 문장 중간) / so 그래서 / <b>either ~도 (부정문 끝)</b> / too ~도 (긍정문 끝)",
       "<b>핵심</b> 문장 끝 '~도 역시': 긍정문 → too / <b>부정문(will not) → either</b>.",
       "I don't like it either. / I like it too."],
 113: ["<b>✓ 맞힘 · 네 질문: throughout vs while 구분?</b>",
       "<b>while + 주어 + 동사</b>(접속사): while I was eating. <b>throughout / during + 명사</b>(전치사): throughout the summer.",
       "빈칸 뒤 the summer는 명사 → throughout. 빈칸 뒤 동사 유무만 보면 돼."],
 122: ["<b>✓ 맞힘 · 네 질문: role + in 규칙 맞아?</b> → 맞아.",
       "role <b>in</b> + 명사/V-ing = ~에서의 역할: his role in organizing the fair.",
       "같은 짝: participate in, interest in, increase in, experience in."],
 126: ["<b>✓ 맞힘 · 네 메모 'C, D 둘 다?'</b>",
       "also, yet, indeed는 <b>부사</b>라서 뒤에 명사(price)를 못 받아. besides만 <b>전치사</b> = ~ 외에도.",
       "해석: 가격 <b>외에도</b> 지역 공급업체를 고르는 데엔 여러 장점이 있다."],
 127: ["<b>✓ 맞힘 · 네 질문: on the contrary 정확한 해석?</b>",
       "<b>on the contrary = 그와는 반대로.</b> 앞 말을 부정할 때: It isn't cheap. On the contrary, it's very expensive.",
       "<b>nevertheless = even so = 그럼에도.</b> 셋 다 접속부사라 명사 앞에 못 와. in spite of(전치사)만 명사 OK.",
       "어제 Test 8-127 오답을 오늘 맞힌 거야 👍"],
 130: ["<b>✓ 맞힘 · those / these에 '?' 친 것</b>",
       "비교 문장에서 앞 명사 되받기: 단수 → <b>that</b>, 복수 → <b>those</b>. these는 이렇게 안 써.",
       "앞이 The prices(복수) → those (at the old location). them은 뒤에 수식어(at~)를 못 붙여."],
 136: ["<b>✓ 맞힘 · 네 질문: whom이면 뒤에 목적어 없어도 되지?</b> → 정확해.",
       "The consultant [whom the manager recommended ___] → recommended 뒤 목적어 자리가 비었으니 목적격 whom.",
       "whose는 뒤에 명사가 붙고(whose experience), which는 사물, what은 앞에 명사가 없을 때."],
}
ORDER = [106, 107, 108, 109, 110, 112, 114, 115, 116, 117, 123, 131, 132, 135, 113, 122, 126, 127, 130, 136]
W = landscape(A4)[0] - 60
rows = []
for n in ORDER:
    stem, ch, a = items[n - 1]
    left = [Paragraph(f"<b>{n}.</b> {stem}", st("S", 10.5, 14.5)), Spacer(1, 3)]
    for k, o in enumerate(ch):
        mark = ""
        if k == a: mark = '  <font color="#1e8449"><b>◀ 정답</b></font>'
        elif MINE[n] and o == MINE[n]: mark = '  <font color="#c0392b"><b>◀ 내 답</b></font>'
        left.append(Paragraph(f"({L[k]}) {o}{mark}", st("K", 10.5, 14.5)))
    if MINE[n] is None: left.append(Paragraph('<font color="#c0392b">(비워 둠)</font>', st("K", 9.5, 13)))
    right = [Paragraph(t, st("K", 9.6, 14.2)) for t in EX[n]]
    rows.append([left, right])
t = Table(rows, colWidths=[W * 0.42, W * 0.58])
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#f6f8fc")), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
s = [Paragraph("약점 메우기 103~137 — 21/35 · 오답 14 + 질문 6 (문제 + 해석 + 해설)", st("K", 15, 21)),
     Paragraph("핵심 2개: ① 전치사 짝 7개 (in writing · on Friday · lecture on · from~until · at the end of · from countries · divide among) → 뜻 말고 덩어리로 ② 정답에 X 친 게 2개(116·132) → 지울 땐 이유 한 단어", st("K", 9.5, 14, "#555555")),
     Spacer(1, 8), t]
SimpleDocTemplate(str(ROOT / "data/workbook/Weak_Side_1126.pdf"), pagesize=landscape(A4), leftMargin=30, rightMargin=30, topMargin=28, bottomMargin=28).build(s)
print("ok")
