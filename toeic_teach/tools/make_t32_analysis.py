from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
pdfmetrics.registerFont(TTFont("NG","tools/fonts/NanumGothic-Regular.ttf"));pdfmetrics.registerFont(TTFont("NG-B","tools/fonts/NanumGothic-Bold.ttf"))
pdfmetrics.registerFontFamily("NG",normal="NG",bold="NG-B")
h1=ParagraphStyle("h1",fontName="NG-B",fontSize=17,leading=23,spaceAfter=4)
h2=ParagraphStyle("h2",fontName="NG-B",fontSize=12.5,leading=17,spaceBefore=6,spaceAfter=4)
b=ParagraphStyle("b",fontName="NG",fontSize=9.4,leading=14)
c=ParagraphStyle("c",fontName="NG",fontSize=8.8,leading=13)
cb=ParagraphStyle("cb",fontName="NG-B",fontSize=8.8,leading=13)
en=ParagraphStyle("en",fontName="Helvetica",fontSize=10,leading=14)
W=182*mm
def P(t,s=c): return Paragraph(t,s)

ITEMS=[
("104","오답","spacious","punctual",
 "The hotel's renovated lobby features a <b>-------</b> seating area overlooking the harbor.",
 "[The hotel's renovated lobby] / [features] / [a <b>빈칸</b> seating area] / [overlooking the harbor]<br/>→ 명사 seating area 앞 형용사. 4개 다 형용사라 <b>의미 + 꾸미는 명사</b>로만 결정",
 "꾸미는 명사 <b>seating area</b>(공간)",
 "공간을 꾸미는 형용사 → <b>spacious</b>(넓은). spacious room / office / lobby.",
 "punctual: 사람·교통수단이 '시간을 지키는'(a punctual employee, punctual arrival) / numerous: 복수명사 앞(numerous seats) / tentative: 일정·계획이 '잠정적인'",
 "spacious를 '넓은?' 하고 확신 못 해서 X 쳤어. <b>형용사 어휘는 그 형용사가 주로 꾸미는 명사 종류</b>로 외워: spacious → 공간, punctual → 사람·시간.",
 "형용사 = <b>꾸미는 명사 종류</b>로 외우기",
 "실제 기출도 같은 방식: 1000제 T7 118 '------- changes to its menu'(extensive/precious/commercial/accurate), T10 124 '------- changes ... greeted enthusiastically'(substantial). 4개 모두 같은 품사, 꾸미는 명사와의 궁합으로 결정."),
("123","오답","tactful","tactically",
 "Mr. Tanaka was commended for <b>his -------</b> handling <b>of</b> a difficult customer complaint.",
 "[Mr. Tanaka] / [was commended for] / [<b>his</b> + 빈칸 + <b>handling</b> + <b>of</b> a complaint]<br/>→ handling 뒤에 <b>of</b>가 있음 = handling은 <b>명사</b>",
 "앞 <b>소유격 his</b> + 뒤 <b>handling of</b>",
 "소유격 + ___ + 명사 → <b>형용사</b> tactful(요령 있는). 칭찬받았으니 긍정 의미.",
 "tactically: 부사는 명사를 못 꾸밈 / tactless: 형용사지만 '요령 없는'이라 칭찬과 반대 / tactic: 명사",
 "메모 'V-ing 앞은 부사'는 반만 맞는 규칙이야. <b>V-ing 바로 뒤</b>를 봐야 해: <b>of</b>가 오면 명사(→ 형용사), <b>목적어</b>가 바로 오면 동명사(→ 부사).",
 "his <b>careful</b> handling <b>of</b> ~ (형) vs by <b>carefully</b> handling ~ (부)",
 "같은 함정이 실제에도 나옴: 기출 빈출 'his/her ------- review of the report', 'the ------- handling of'. 반대로 'by ------- responding to inquiries'(토익응급실 260809 109, 네가 틀렸던 문제)는 부사."),
("110","애매하게 맞힘","prohibited","(?) 표시",
 "Staff are reminded that the use of personal phones is <b>-------</b> during client meetings.",
 "[the use of personal phones] / [is <b>빈칸</b>] / [during client meetings]<br/>→ 주어는 <b>사물(the use)</b>, be + p.p. 수동",
 "주어 <b>the use</b>(사용) + 수동태",
 "사용이 '금지된다' → <b>prohibited</b>. 사물 주어 수동이 자연스러운 동사.",
 "cautioned: caution은 <b>사람</b>을 목적어로(caution staff against ~) → '사용이 주의받다' 불가 / refrained: refrain은 자동사(from)라 수동 불가 / eliminated: '사용이 제거된다'는 의미 어색",
 "네 메모 '주의하다 / from / to'처럼 짝까지 적은 건 아주 좋았어. 마지막엔 <b>주어가 사람인지 사물인지</b>를 보면 cautioned가 바로 빠져.",
 "수동태 어휘: <b>주어(사물)가 그 동작을 당할 수 있는지</b> 확인",
 "실제 기출: 1000제 T7 120 'asked to ------- from asking questions'(refrain/forbid/retreat/hesitate) — refrain은 from과 짝, forbid는 목적어 필요. 같은 짝·구조 판별."),
("126","애매하게 맞힘","clearance","(!) 표시",
 "Employees must obtain security <b>-------</b> before entering the server room.",
 "[Employees] / [must obtain] / [security + <b>빈칸</b>] / [before entering]<br/>→ obtain의 목적어, security와 붙는 <b>복합명사</b>",
 "<b>obtain</b>(얻다) + <b>security</b>",
 "security clearance = <b>보안 출입 허가</b>. 얻을 수 있는 것은 '허가'.",
 "clarity: 명확성(얻는 대상 아님) / clearing: 개간지·청산 / clear: 형용사·동사",
 "clear 계열이 4개라 헷갈렸어. <b>clearance = 허가·승인</b>(security clearance, customs clearance)으로 외워.",
 "obtain / receive / grant + <b>clearance·approval·authorization</b>",
 "실제 기출: 1000제 T10 130 'without prior -------'(authorization) — 허가 명사가 빈출."),
("109","고민한 문제","After","Prior to / Despite 지움",
 "<b>-------</b> the merger was announced, shares of both companies rose sharply.",
 "<b>빈칸</b> + [the merger was announced](절) , [shares rose](주절)",
 "빈칸 뒤 <b>주어 + 동사</b>(the merger was announced)",
 "절 앞 → 접속사 <b>After</b>.",
 "During / Despite / Prior to: 모두 전치사라 절 못 받음",
 "Prior to와 Despite를 지운 판단 정확했어. 이 유형은 <b>뜻보다 빈칸 뒤 동사 유무</b>가 먼저야.",
 "뒤가 절 → 접속사 / 명사 → 전치사",
 "실제 기출: 1000제 T7 115 '------- the cost of travel, the cost of attending is reasonable'(Aside from), T9 124 '------- her starting salary is still being negotiated'(because)."),
("119","맞힘 (복습 포인트)","Anyone","Those 지움",
 "<b>-------</b> who <b>wishes</b> to attend the training session should notify Ms. Park.",
 "[빈칸 + who wishes ...] (주어) / [should notify] (본동사)",
 "who 뒤 <b>단수동사 wishes</b>",
 "단수 동사와 맞는 대명사 → <b>Anyone</b> who wishes.",
 "Those who → 복수동사(wish) / Whoever → who와 중복 / They → 관계절 수식 불가",
 "'단' 메모하고 Those 지운 것 완벽해. TEST 26 118 오답을 이번엔 잡았어.",
 "Anyone who + 단수V / Those who + 복수V",
 "실제 기출: 1000제 T7 123 '------- who arrives at the parking garage after 10 A.M.'(Anyone), T1 123 'Anyone who ------- '(needs)."),
("125","맞힘 (복습 포인트)","to","success to 메모",
 "Analysts attribute the company's recent success <b>-------</b> its expansion into overseas markets.",
 "[attribute] + [A: the company's recent success] + <b>빈칸</b> + [B: its expansion]",
 "동사 <b>attribute</b> (A를 B 덕분으로 돌리다)",
 "attribute A <b>to</b> B.",
 "for / with / by: attribute와 짝이 아님",
 "A가 길어서 to가 멀리 떨어져 있어도 <b>동사의 짝</b>을 끝까지 추적한 게 좋았어.",
 "attribute / owe / credit A <b>to</b> B",
 "실제 기출: 'be attributed to', 'due to'(1000제 T9 'popularity is ------- to' 계열) 빈출."),
("130","맞힘 (고난도)","contingent","consistent·convenient 지움",
 "Funding for the community center is <b>-------</b> upon approval from the city council.",
 "[Funding] / [is <b>빈칸</b> <b>upon</b> approval]",
 "빈칸 뒤 <b>upon</b>",
 "be contingent <b>upon/on</b> = ~에 달려 있다.",
 "consistent with / convenient for / contiguous to: upon과 짝 아님",
 "upon 짝으로 지운 것 정확해. 고난도 어휘는 <b>뒤 전치사</b>가 가장 강한 단서야.",
 "contingent upon · dependent on · subject to",
 "실제 기출 121~130 구간은 이렇게 '짝 전치사로 거르는 고급 형용사'가 매회 1~2개 나옴(commensurate with, conducive to 등)."),
]
def card(it):
    n,src,ans,mine,sent,parse,clue,why,wrong,pull,rule,real=it
    rows=[[P("문장",cb),P(sent,en)],[P("문장 해체",cb),P(parse)],[P("단서",cb),P(clue)],[P("정답 근거",cb),P(why)],
          [P("오답 탈락",cb),P(wrong)],[P("왜 끌렸나",cb),P(pull)],[P("규칙",cb),P("<b>"+rule+"</b>")],[P("실제 기출 대조",cb),P(real)]]
    t=Table(rows,colWidths=[22*mm,W-22*mm])
    t.setStyle(TableStyle([("BOX",(0,0),(-1,-1),.8,colors.black),("INNERGRID",(0,0),(-1,-1),.3,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(0,-1),colors.HexColor("#efefef")),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    head=P(f"<b>{n}번</b> [{src}]  정답 <b>{ans}</b>  ←  네 답: {mine}",h2)
    return KeepTogether([head,t,Spacer(1,5)])

s=[P("TEST 32 P5 헷갈린 문제 해설지 (8문제)",h1),
 P("<b>28/30, 11분.</b> 틀린 2개(104, 123) + 표시하며 고민한 6개(110, 126, 109, 119, 125, 130). 각 문제마다 <b>실제 기출에서 같은 포인트가 어떻게 나오는지</b> 대조했어.",b),
 P("<b>시간:</b> 목표 10분보다 1분 초과. 110·126처럼 확신 안 서는 문제는 15초 안에 짝/주어로 거르고 넘어가기.",b),
 P("A. 틀린 문제",h2)]
for it in ITEMS[:2]: s.append(card(it))
s.append(P("B. 애매하게 맞힌 문제",h2))
for it in ITEMS[2:4]: s.append(card(it))
s.append(P("C. 고민해서 맞힌 문제 (규칙 확인용)",h2))
for it in ITEMS[4:]: s.append(card(it))
s.append(P("한 장 요약",h2))
s.append(P("① 형용사 어휘 = 꾸미는 명사 종류 (spacious → 공간) ② V-ing 뒤 of → 형용사, 목적어 → 부사 ③ 사물 주어 수동태는 '당할 수 있는 동작'인지 ④ clearance = 허가 ⑤ 뒤가 절이면 접속사 ⑥ who + 단수V → Anyone ⑦ attribute A to B ⑧ 고급 형용사는 뒤 전치사 짝",b))
SimpleDocTemplate("data/workbook/Test32_P5_해설.pdf",pagesize=A4,leftMargin=14*mm,rightMargin=14*mm,topMargin=13*mm,bottomMargin=13*mm).build(s)
