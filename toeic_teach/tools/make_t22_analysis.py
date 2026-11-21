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
("105","TEST 22","from","at",
 "The museum is open <b>-------</b> 9 A.M. until 5 P.M. every day.",
 "[The museum] / [is open] / <b>빈칸</b> + [9 A.M.] / <b>[until 5 P.M.]</b> / [every day]<br/>→ 시각 두 개가 <b>시작~끝</b>으로 묶여 있음",
 "뒤의 <b>until 5 P.M.</b> (끝 시점이 이미 나옴)",
 "<b>from A until/to B</b> = A부터 B까지. 끝(until)이 보이면 시작은 from.",
 "at: 시각 하나만 가리킬 때(at 9 A.M.) / since: 과거부터 지금까지(현재완료와 함께) / between: between A <b>and</b> B라서 until과 안 맞음",
 "9 A.M. 바로 앞이라 at을 골랐어. <b>빈칸 바로 뒤 한 단어가 아니라 문장 끝까지</b> 봐야 해. until이 짝을 알려줘.",
 "until / to 가 보이면 → <b>from</b> / and 가 보이면 → between"),
("110","TEST 22","strengthen","strength",
 "The merger is expected to <b>-------</b> the company's position in the Asian market.",
 "[The merger] / [is expected <b>to</b>] / <b>빈칸</b> + [the company's position] / [in the Asian market]<br/>→ to 뒤 + 뒤에 목적어(the company's position) → <b>동사원형</b>",
 "<b>to</b> 바로 뒤 + 빈칸 뒤 목적어",
 "be expected to + <b>동사원형</b>. 목적어가 있으니 타동사 strengthen(강화하다).",
 "strength: 명사 / strong: 형용사 / strongly: 부사. 셋 다 to 뒤 동사 자리에 못 옴",
 "메모에 '여기 to가 중요'라고 쓰고도 명사를 골랐어. strength가 '힘'이라 뜻으로 끌린 거야. <b>to 뒤 = 동사원형</b>이면 -en, -ize, -ify로 끝나는 동사형부터 찾아.",
 "to + ___ + 목적어 → 동사원형 (strengthen, widen, shorten)"),
("119","TEST 22","reduced","dropped",
 "Rising material costs have <b>-------</b> the firm's profits.",
 "[Rising material costs] / [have <b>빈칸</b>] + <b>[the firm's profits]</b><br/>→ have + p.p. 뒤에 <b>목적어</b>가 있음 → 타동사",
 "빈칸 뒤 <b>목적어 the firm's profits</b>",
 "목적어가 있으니 <b>타동사</b> reduce(줄이다): 비용 상승이 이익을 줄였다.",
 "declined / fallen / dropped: '줄어들다'라는 자동사라 목적어를 못 받음 (drop은 '떨어뜨리다' 뜻일 때만 타동사, 이익에는 안 씀)",
 "<b>어제 lower/decline이랑 똑같은 규칙</b>이야. 줄다(자동사)와 줄이다(타동사)를 목적어로 구분하는 거. 이번이 2번째.",
 "목적어 있음 → reduce·lower·cut / 없음 → decline·fall·drop"),
("121","TEST 22","whether","that",
 "The committee has not yet decided <b>-------</b> to hire an outside consultant.",
 "[The committee] / [has not yet decided] / <b>빈칸</b> + <b>[to hire]</b> + [an outside consultant]<br/>→ decided의 목적어 자리에 <b>빈칸 + to V</b>",
 "빈칸 바로 뒤 <b>to hire</b> + 앞의 <b>not yet decided</b>(아직 결정 안 됨)",
 "<b>whether to V</b> = ~할지 말지. 아직 결정 안 했으니 '할지 말지'.",
 "if: 뜻은 같지만 <b>if to V는 불가</b> / that: 뒤에 주어+동사 절이 와야 함, to V 못 받음 / what: 뒤에 목적어가 빠진 구조여야 하는데 consultant가 있음",
 "if와 what을 X 친 것까지는 맞았어. that은 '~라는 것'이라 뒤에 <b>절</b>이 와야 해. <b>to V 앞에 올 수 있는 건 whether, how, what, where</b> 같은 의문사.",
 "decide / ask / wonder + <b>whether to V</b>"),
("128","TEST 22","at","since",
 "The contract will expire <b>-------</b> the end of the year unless it is renewed.",
 "[The contract] / [will expire] / <b>빈칸</b> + [the end of the year] / [unless it is renewed]<br/>→ 미래(will) 한 시점에 만료",
 "<b>the end of</b> + 미래 시제 will",
 "<b>at the end of</b> ~ = ~의 말에. 만료되는 한 시점.",
 "of: 앞 명사와 연결하는 말이라 동사 expire 뒤 불가 / since: 과거부터 지금까지 계속(현재완료와 씀), will과 안 맞음 / between: A and B 필요",
 "since를 '~부터'로 읽고 골랐어. since는 <b>과거 시점 + 현재완료(has been)</b>에서만 써. will 문장에는 안 와.",
 "<b>at the end of / at the beginning of</b> / since + 과거 + 현재완료"),
("130","TEST 22","visit","visiting",
 "The cafeteria my coworkers <b>-------</b> most often is on the second floor.",
 "[The cafeteria] <u>[that] 생략</u> [my coworkers] <b>빈칸</b> [most often] / <b>[is]</b> on the second floor<br/>→ 본동사는 이미 is. 빈칸은 관계절의 동사",
 "<b>명사(cafeteria) + 명사(my coworkers) + 빈칸</b>",
 "my coworkers가 주어, 빈칸은 그 동사. 복수 주어 → <b>visit</b>. (that 생략: cafeteria가 visit의 목적어)",
 "visiting: 동사가 아님, 주어 my coworkers에 동사가 없어짐 / to visit: 동사 아님 / visits: coworkers 복수라 단수 동사 불가",
 "<b>이 유형 3번째 오답이야.</b> (서아 13, TEST 21 130, 오늘 130) 명사 + 명사 뒤 빈칸을 보면 무조건 '-ing로 꾸미는 말'로 읽고 있어. 공식으로 외워.",
 "<b>명사 + 명사 + 빈칸 → 동사 (that 생략)</b>. 주어 수에 맞춰 s 붙이기"),
]
def card(it):
    n,src,ans,mine,sent,parse,clue,why,wrong,pull,rule=it
    rows=[[P("문장",cb),P(sent,en)],[P("문장 해체",cb),P(parse)],[P("단서",cb),P(clue)],[P("정답 근거",cb),P(why)],
          [P("오답 탈락",cb),P(wrong)],[P("왜 끌렸나",cb),P(pull)],[P("규칙",cb),P("<b>"+rule+"</b>")]]
    t=Table(rows,colWidths=[22*mm,W-22*mm])
    t.setStyle(TableStyle([("BOX",(0,0),(-1,-1),.8,colors.black),("INNERGRID",(0,0),(-1,-1),.3,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(0,-1),colors.HexColor("#efefef")),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    head=P(f"<b>{n}번</b> [{src}]  정답 <b>{ans}</b>  ←  네 답: {mine}",h2)
    return KeepTogether([head,t,Spacer(1,5)])
V=[("105","The pharmacy is open ------- 8 A.M. to 9 P.M. on weekdays.","(A) since (B) at (C) from (D) between","C"),
("110","The new policy is designed to ------- customer trust.","(A) strength (B) strengthen (C) strong (D) strongly","B"),
("119","The new software has ------- processing time by half.","(A) fallen (B) declined (C) dropped (D) cut","D"),
("121","Ms. Ito has not decided ------- to accept the job offer.","(A) that (B) whether (C) if (D) what","B"),
("128","The store will close ------- the end of the month.","(A) since (B) of (C) at (D) between","C"),
("130","The printer my teammates ------- every morning needs new ink.","(A) using (B) use (C) uses (D) to use","B")]
s=[P("TEST 22 오답 해체 분석 (6문제)",h1),
 P("<b>24/30.</b> 어제 TEST 21(21/30)보다 3개 올랐어. 틀린 6개 중 2개는 어제랑 같은 규칙이야: <b>119 자동사/타동사</b>, <b>130 that 생략(3번째)</b>.",b),
 P("<b>틀린 이유 요약:</b> 1) 빈칸 뒤만 보고 문장 끝 단서를 놓침(105 until, 128 will). 2) to 뒤 자리 판단(110 to+동사, 121 whether to). 3) 반복 규칙(119, 130).",b),
 P("A. 오답 6개",h2)]
for it in ITEMS: s.append(card(it))
s.append(PageBreak());s.append(P("B. 변형 문제 6개 (답은 맨 아래)",h1))
for n,q,ch,a in V: s+= [P(f"<b>{n}번 규칙</b>",c),P(q,en),P(ch,en),Spacer(1,8)]
s.append(Spacer(1,30));s.append(P("정답: "+"   ".join(f"<b>{n}</b> {a}" for n,q,ch,a in V),b))
SimpleDocTemplate("data/workbook/Test22_해체분석.pdf",pagesize=A4,leftMargin=14*mm,rightMargin=14*mm,topMargin=13*mm,bottomMargin=13*mm).build(s)
