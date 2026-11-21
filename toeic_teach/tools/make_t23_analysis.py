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
("103","TEST 23","center","stage",
 "The hotel's conference <b>-------</b> can accommodate up to 300 guests.",
 "[The hotel's conference <b>빈칸</b>] / [can accommodate] / [up to 300 guests]<br/>→ 빈칸은 주어(명사). 동사 <b>accommodate(수용하다)</b>의 주체가 되는 것",
 "동사 <b>accommodate up to 300 guests</b> (300명을 수용)",
 "300명을 '수용하는' 건 공간 전체 → conference <b>center</b>(회의장). 명사 4개가 다 문법상 들어가서 <b>뜻</b>으로만 골라야 하는 의미 어휘 문제.",
 "stage: 무대는 공연하는 곳이지 손님 300명을 수용하는 곳이 아님 / label: 라벨 / ticket: 표",
 "conference를 보고 '회의 + 무대'를 떠올렸어. 빈칸 바로 뒤가 아니라 <b>동사(accommodate)와 목적어(300 guests)</b>까지 읽어야 풀려.",
 "명사 어휘는 <b>뒤 동사와 짝</b>으로: accommodate guests → center / hall / venue"),
("110","TEST 23","protective","protection",
 "Staff members must wear <b>-------</b> footwear in the warehouse at all times.",
 "[Staff members] / [must wear] / <b>빈칸</b> + [footwear] / [in the warehouse]<br/>→ 동사 wear의 목적어 footwear 앞 = <b>명사를 꾸미는 자리</b>",
 "빈칸 바로 뒤 <b>명사 footwear</b>",
 "명사 앞은 형용사가 기본 → <b>protective footwear</b>(보호용 신발). protective equipment / clothing / gloves 같이 굳어진 표현.",
 "protection: 명사. '명사+명사'가 가능한 경우도 있지만 <b>형용사 protective가 선지에 있으면 형용사가 우선</b> / protected: '보호받는' 신발이라 뜻이 반대 / protectively: 부사",
 "메모에 '형/N 가능'이라고 적었어. 복합명사(명사+명사)는 <b>굳어진 표현일 때만</b>(safety equipment, customer service) 정답이 돼. 형용사형이 있으면 형용사부터 넣어봐.",
 "명사 앞 → <b>형용사 먼저</b>. 복합명사는 굳어진 짝만"),
("115","TEST 23","were presented","presented",
 "The quarterly sales figures <b>-------</b> to the board of directors yesterday.",
 "[The quarterly sales figures] / <b>빈칸</b> / [to the board of directors] / [yesterday]<br/>→ 문장에 동사가 없음 → 빈칸이 <b>본동사</b>. 빈칸 뒤에 <b>목적어가 없음</b>",
 "주어가 <b>사물(figures)</b> + 뒤에 목적어 없음 + <b>yesterday</b>",
 "수치는 '제출되는' 것 + 목적어 없음 → 수동 + 과거 → <b>were presented</b>.",
 "presented: 능동 과거. 수치가 스스로 무언가를 제출하는 꼴이고 목적어도 없음 / have presented: 능동 + yesterday와 현재완료 충돌 / are presenting: 진행 + yesterday 충돌",
 "presented가 '제출된'처럼 읽혀서 골랐어. 하지만 그건 <b>명사를 꾸미는 분사</b>일 때 얘기고, 이 문장엔 본동사가 없어서 빈칸이 본동사여야 해. <b>사물 주어 + 목적어 없음 = be + p.p.</b>",
 "동사 자리 3단계: <b>수 일치 → 태(목적어 유무) → 시제(yesterday)</b>"),
("121","TEST 23","throughout","while",
 "The library will remain open late <b>-------</b> final exam week.",
 "[The library] / [will remain open late] / <b>빈칸</b> + <b>[final exam week]</b><br/>→ 빈칸 뒤가 <b>명사구</b>(주어+동사 없음) → 전치사 자리",
 "빈칸 뒤 <b>final exam week</b> (명사구, 기간)",
 "명사구 앞 → 전치사. 기간 '내내' → <b>throughout</b>.",
 "while: 접속사라 뒤에 주어+동사 필요 / whenever: 접속사 / since: 과거 시점 + 현재완료(has remained)일 때만, will과 안 맞음",
 "while을 '~하는 동안'으로 해석해서 골랐어. 뜻은 비슷하지만 <b>while은 절, during·throughout은 명사</b> 앞이야. 해석보다 <b>빈칸 뒤에 동사가 있는지</b> 먼저 봐.",
 "뒤가 명사 → during / throughout / for · 뒤가 절 → while / when"),
("122","TEST 23","remarkable","remarked",
 "Ridgeway Motors has achieved <b>-------</b> growth in its overseas markets this year.",
 "[Ridgeway Motors] / [has achieved] / <b>빈칸</b> + [growth] / [in its overseas markets]<br/>→ achieved의 목적어 growth 앞 = <b>형용사 자리</b>",
 "빈칸 바로 뒤 <b>명사 growth</b>",
 "명사 앞 형용사 → <b>remarkable</b>(놀라운, 두드러진). remarkable growth / success / progress.",
 "remarkably: 부사 / remark: 명사·동사 / remarked: remark(언급하다)의 과거분사. '언급된 성장'이라는 뜻이 되고, 이런 표현은 쓰지 않음",
 "remarkable에 밑줄까지 쳐놓고 remarked를 골랐어. 분사(-ed)도 형용사처럼 쓰이지만 <b>-able형 형용사가 따로 있으면 그게 정답</b>인 경우가 대부분이야.",
 "명사 앞 → <b>-able / -ive / -ful 형용사가 있으면 먼저</b>, 분사는 그다음"),
]
def card(it):
    n,src,ans,mine,sent,parse,clue,why,wrong,pull,rule=it
    rows=[[P("문장",cb),P(sent,en)],[P("문장 해체",cb),P(parse)],[P("단서",cb),P(clue)],[P("정답 근거",cb),P(why)],
          [P("오답 탈락",cb),P(wrong)],[P("왜 끌렸나",cb),P(pull)],[P("규칙",cb),P("<b>"+rule+"</b>")]]
    t=Table(rows,colWidths=[22*mm,W-22*mm])
    t.setStyle(TableStyle([("BOX",(0,0),(-1,-1),.8,colors.black),("INNERGRID",(0,0),(-1,-1),.3,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(0,-1),colors.HexColor("#efefef")),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    head=P(f"<b>{n}번</b> [{src}]  정답 <b>{ans}</b>  ←  네 답: {mine}",h2)
    return KeepTogether([head,t,Spacer(1,5)])
V=[("103-1","Our banquet ------- can seat up to 250 guests for weddings and conferences.","(A) menu (B) hall (C) staff (D) schedule","B"),
("103-2","The university's new parking ------- has space for more than 400 vehicles.","(A) permit (B) fee (C) garage (D) sign","C"),
("110-1","All lab technicians must wear ------- gloves when handling chemicals.","(A) protection (B) protect (C) protectively (D) protective","D"),
("110-2","The hotel received ------- reviews from guests who stayed during the festival.","(A) favorable (B) favor (C) favorably (D) favorableness","A"),
("115-1","The new safety guidelines ------- to all employees last Monday.","(A) distributed (B) were distributed (C) have distributed (D) are distributing","B"),
("115-2","The winners of the design contest ------- at the awards dinner next Friday.","(A) announced (B) will announce (C) will be announced (D) have been announcing","C"),
("121-1","The museum will be closed ------- the renovation period.","(A) while (B) whereas (C) unless (D) during","D"),
("121-2","Customer service representatives are available ------- the day to answer questions.","(A) throughout (B) while (C) although (D) once","A"),
("122-1","The new manager has made ------- progress in reducing shipping delays.","(A) noticeably (B) noticed (C) noticeable (D) notice","C"),
("122-2","The firm reported ------- profits for the third consecutive quarter.","(A) impressed (B) impressive (C) impressively (D) impression","B")]
s=[P("TEST 23 P5 오답 해체 분석 (5문제)",h1),
 P("<b>P5 25/30.</b> TEST 21(21) → TEST 22(24) → TEST 23(25), 실전 비율로 만든 세트에서 계속 오르고 있어.",b),
 P("<b>틀린 이유 요약:</b> 1) 명사 앞 형용사 자리에서 다른 형태를 고름(110 protection, 122 remarked). 2) 빈칸 뒤가 명사인지 절인지 확인 안 함(121 while). 3) 동사 자리에서 태 확인을 건너뜀(115). 4) 의미 어휘를 빈칸 옆 단어만 보고 고름(103).",b),
 P("A. 오답 5개",h2)]
for it in ITEMS: s.append(card(it))
s.append(PageBreak());s.append(P("B. 변형 문제 10개 (오답 1개당 2개, 답은 맨 아래)",h1))
for n,q,ch,a in V: s+= [P(f"<b>{n}번 규칙</b>",c),P(q,en),P(ch,en),Spacer(1,8)]
s.append(Spacer(1,24));s.append(P("정답: "+"   ".join(f"<b>{n}</b> {a}" for n,q,ch,a in V),b))
SimpleDocTemplate("data/workbook/Test23_P5_해체분석.pdf",pagesize=A4,leftMargin=14*mm,rightMargin=14*mm,topMargin=13*mm,bottomMargin=13*mm).build(s)
