"""11/27 화면 녹화용 세트: P5 10 + P7 이중 1 + 삼중 1 → data/workbook/Rec_Set_1127.pdf (문제), Rec_Set_1127_key.pdf (정답·근거)"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
ROOT = Path(__file__).resolve().parent.parent
LIB = "/usr/share/fonts/truetype/liberation/"
for n, f in [("S", "LiberationSans-Regular"), ("SB", "LiberationSans-Bold"), ("R", "LiberationSerif-Regular"), ("RB", "LiberationSerif-Bold"), ("RI", "LiberationSerif-Italic")]:
    pdfmetrics.registerFont(TTFont(n, LIB + f + ".ttf"))
pdfmetrics.registerFont(TTFont("K", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))
registerFontFamily("S", normal="S", bold="SB", italic="S", boldItalic="SB")
registerFontFamily("R", normal="R", bold="RB", italic="RI", boldItalic="RB")
registerFontFamily("K", normal="K", bold="K", italic="K", boldItalic="K")
st = lambda f, s, l, c="#000000", **k: ParagraphStyle("x", fontName=f, fontSize=s, leading=l, textColor=colors.HexColor(c), **k)
W = A4[0] - 72
Q, O, PS = st("S", 10.3, 14), st("S", 10.1, 13.6, leftIndent=16), st("R", 10.3, 14.6, spaceAfter=5)

P5 = [
 (101, "The marketing team ------- the results of the customer survey before the board meeting next week.", ["reviewing", "will review", "to review", "reviewer"], "B", "동사 자리(문장에 동사 없음) + next week → 미래"),
 (102, "Ms. Tanaka asked that all expense reports be submitted ------- to the accounting department.", ["prompt", "promptly", "promptness", "prompted"], "B", "be submitted(수동태 완성) 뒤 → 동사 꾸미는 부사"),
 (103, "------- the new software is easy to use, many employees still prefer the old system.", ["Despite", "Although", "However", "Even so"], "B", "뒤가 절(주어 + is) + 양보 → 접속사 Although"),
 (104, "The hotel offers a complimentary shuttle to ------- needs transportation to the airport.", ["whoever", "anyone", "those", "who"], "A", "전치사 to 뒤 + 바로 동사 needs → whoever"),
 (105, "Of the two applicants, one has a degree in finance, and ------- has extensive sales experience.", ["another", "others", "the other", "other"], "C", "둘 중 one ↔ 나머지 하나 the other"),
 (106, "Customers who keep their receipts will find the return process ------- simple.", ["surprise", "surprisingly", "surprising", "surprised"], "B", "find O + 형용사(simple)는 이미 있음 → 형용사 simple을 꾸미는 부사"),
 (107, "The director was pleased with the proposal and approved ------- without any changes.", ["it", "its", "itself", "them"], "A", "approved의 목적어 = the proposal(단수, 주어와 다름) → it"),
 (108, "Applicants for the position must be ------- with standard spreadsheet software.", ["familiar", "aware", "capable", "known"], "A", "짝: familiar with (aware of / capable of)"),
 (109, "The annual sales conference will be held ------- the first week of March.", ["during", "while", "until", "since"], "A", "뒤 명사(기간) → 전치사 during (while은 절)"),
 (110, "Thanks to good weather, the renovation project was completed two weeks ahead of -------.", ["schedule", "scheduled", "scheduling", "schedules"], "A", "짝: ahead of schedule (예정보다 일찍)"),
]

def opts(lst):
    return [Paragraph(f"({L}) {o}", O) for L, o in zip("ABCD", lst)]

def box(flow, pad=11):
    t = Table([[flow]], colWidths=[W - 2])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, colors.black), ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
                           ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return t

def grid(rows, widths, head=True):
    t = Table([[Paragraph(c, st("R", 9.8, 13)) for c in r] for r in rows], colWidths=widths)
    s = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#777777")), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if head: s.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")))
    t.setStyle(TableStyle(s)); return t

def qpair(qs):
    cells = [[Paragraph(f"<b>{n}.</b> {stem}", Q)] + opts(o) + [Spacer(1, 8)] for n, stem, o, *_ in qs]
    half = (len(cells) + 1) // 2  # 실제 토익처럼 왼쪽 열 위→아래 먼저, 그다음 오른쪽 열
    left = [x for c in cells[:half] for x in c]; right = [x for c in cells[half:] for x in c]
    t = Table([[left, right]], colWidths=[W / 2, W / 2])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 10)]))
    return t

D = [
 (176, "What is indicated about the workshops?", ["They are taught by local business owners.", "They each last for the same number of weeks.", "They are held in the same room.", "They include all necessary materials."], "B",
  "공지 첫 줄 All workshops run for six weeks = 모두 같은 주 수. D는 수채화만 materials included (지문 단어 함정)"),
 (177, "In the notice, the word \"run\" in paragraph 1, line 1, is closest in meaning to", ["last", "manage", "hurry", "compete"], "A", "run for six weeks = 6주 동안 계속되다 = last"),
 (178, "Why did Mr. Okafor write the e-mail?", ["To ask for a full refund", "To request credit toward a future workshop", "To change to a different weekday class", "To complain about an instructor"], "B",
  "이메일 apply the amount to a workshop this summer = 다음 워크숍에 쓸 크레딧. A는 refund 단어 함정(본인이 환불 못 받는 거 안다고 씀)"),
 (179, "Which workshop did Mr. Okafor register for?", ["Basic Photography", "Introduction to Watercolor", "Small Business Bookkeeping", "Conversational Spanish"], "C",
  "연계: 이메일 Thursday evening + catering business(사업) → 표 Thursdays = Small Business Bookkeeping"),
 (180, "How much should Mr. Okafor most likely have paid for the workshop?", ["$76.50", "$63.75", "$90.00", "$59.50"], "A",
  "연계: 이메일 center member since February + regular price 청구 → 공지 회원 15% 할인 → $90 × 0.85 = $76.50"),
]
T = [
 (186, "What does the advertisement indicate about Brightline Office Furniture?", ["It sells furniture only online.", "It charges a fee for assembly.", "It offers free delivery to all customers.", "It is opening a new showroom."], "B",
  "광고 Assembly service is available for $30 per item. C는 Portland 지역 $500 이상만, D는 renovations(새 매장 아님)"),
 (187, "Why was Ms. Park charged for delivery?", ["Her order totaled less than $500.", "She does not live in the Portland area.", "She requested express shipping.", "She ordered a final sale item."], "B",
  "연계 1-2: 광고 무료 배송은 Portland 지역만 + 주문서 주소 Salem. 상품 합계 $600이라 A 아님 (계산 함정)"),
 (188, "What is suggested about the standing desk?", ["It was assembled by Brightline staff.", "It was delivered later than expected.", "It can be exchanged for a different model.", "It was purchased at the regular price."], "A",
  "주문서 Assembly (standing desk) $30 → 조립 서비스 받음. B는 이메일 arrived on schedule과 반대. C는 final sale이라 불가. D는 광고 5/1~15 책상 20% 할인 + 주문일 5/9 → 할인가"),
 (189, "Why is Ms. Park unable to return the desk?", ["It was damaged during delivery.", "It was a final sale item.", "She ordered it after the sale ended.", "She lost her receipt."], "B",
  "연계 2-1: 주문서 Harbor Standing Desk (final sale) + 광고 final sale items cannot be returned. A는 이메일 scratch 단어 함정(반품 불가 이유 아님)"),
 (190, "When most likely did Ms. Park try to visit the showroom?", ["May 5", "May 9", "May 14", "May 16"], "B",
  "연계 1-2-3: 이메일 showroom was closed the day I visited + 광고 closed May 8-10 + 주문일 May 9(방문 후 주문) → May 9"),
]
assert all(len(x[2]) == 4 for x in D + T)
TARGET = {101: "B", 102: "D", 103: "C", 104: "A", 105: "C", 106: "D", 107: "B", 108: "A", 109: "D", 110: "C",
          176: "B", 177: "D", 178: "C", 179: "A", 180: "D", 186: "C", 187: "A", 188: "D", 189: "D", 190: "B"}
def place(item):
    n, stem, o, a, why = item
    if n == 190: return item
    o = list(o); right = o.pop("ABCD".index(a)); o.insert("ABCD".index(TARGET[n]), right)
    return (n, stem, o, TARGET[n], why)
P5 = [place(x) for x in P5]; D = [place(x) for x in D]; T = [place(x) for x in T]

s = [Paragraph("화면 녹화용 세트 (11/27)", st("K", 16, 22)),
     Paragraph("① P5 101-110 (목표 4분) · ② 이중지문 176-180 (목표 6분) · ③ 삼중지문 186-190 (목표 8분). 클립 3개로 따로 녹화. "
               "실전처럼 풀고, 헷갈린 문제 옆엔 한두 단어 메모(왜 골랐는지). 시작·끝 시각을 맨 위에 적기. 정답은 Rec_Set_1127_key.pdf.", st("K", 9.3, 14, "#555555")),
     Spacer(1, 10), Paragraph("<b>PART 5</b>", st("SB", 12, 16, spaceAfter=6))]
s.append(qpair([(n, q, o) for n, q, o, a, w in P5]))

s += [PageBreak(), Paragraph("<b>Questions 176-180</b> refer to the following notice and e-mail.", st("S", 10.3, 14, spaceAfter=8)),
      box([Paragraph("<b>Riverside Community Center — Spring Workshop Series</b>", st("RB", 11.5, 16, spaceAfter=6)),
           Paragraph("All workshops run for six weeks, beginning the week of April 6. Registration closes on March 30. Center members receive a 15 percent discount on all workshop fees.", PS),
           grid([["Workshop", "Day and Time", "Room", "Instructor", "Fee"],
                 ["Basic Photography", "Mondays, 6:00–8:00 P.M.", "2", "Alan Pierce", "$60"],
                 ["Introduction to Watercolor", "Wednesdays, 7:00–9:00 P.M.", "5", "Grace Lin", "$75 (materials included)"],
                 ["Small Business Bookkeeping", "Thursdays, 6:30–8:30 P.M.", "3", "Omar Haddad", "$90"],
                 ["Conversational Spanish", "Saturdays, 10:00 A.M.–Noon", "2", "Lucia Moreno", "$70"]],
                [W * 0.27, W * 0.27, W * 0.08, W * 0.17, W * 0.18]),
           Spacer(1, 6),
           Paragraph("Participants who cancel at least five days before the first session will receive a full refund. Later cancellations will receive credit toward a future workshop. To register, visit www.riversidecc.org/workshops.", PS)]),
      Spacer(1, 10),
      box([Paragraph("To: registration@riversidecc.org<br/>From: Daniel Okafor &lt;dokafor@okaforcatering.com&gt;<br/>Date: April 15<br/>Subject: My registration", st("R", 10.4, 14.5, spaceAfter=8)),
           Paragraph("Hello,", PS),
           Paragraph("Last month, I signed up for one of your Thursday evening workshops and paid the fee online. I opened a small catering business in January, so the topic is exactly what I need. "
                     "Unfortunately, my company has just won a contract to provide lunches for a local school, and I will be busy preparing food on Thursday evenings for the rest of the spring.", PS),
           Paragraph("I understand that the workshop has already started and that I cannot get my money back at this point. Would it be possible to apply the amount I paid to a workshop this summer instead? "
                     "Also, I noticed that I was charged the regular price, even though I became a center member in February. Could you please look into this?", PS),
           Paragraph("Thank you,<br/>Daniel Okafor", PS)]),
      Spacer(1, 10), qpair([(n, q, o) for n, q, o, a, w in D])]

s += [PageBreak(), Paragraph("<b>Questions 186-190</b> refer to the following advertisement, order confirmation, and e-mail.", st("S", 10.3, 14, spaceAfter=8)),
      box([Paragraph("<b>Brightline Office Furniture — Spring Clearance</b>", st("RB", 11.5, 16, spaceAfter=6)),
           Paragraph("From May 1 to May 15, save 20 percent on all desks and chairs in our showroom and online. Delivery is free on orders over $500 within the Portland area; "
                     "delivery to other locations is available for a flat fee of $45. Our professional assembly service is available for $30 per item.", PS),
           Paragraph("Please note that clearance items marked \"final sale\" cannot be returned. Our Oak Valley showroom will be closed for renovations from May 8 to May 10. Online orders will be processed as usual during this time.", PS)]),
      Spacer(1, 9),
      box([Paragraph("<b>Brightline Office Furniture — Order Confirmation</b>", st("RB", 11, 15, spaceAfter=5)),
           Paragraph("Order number: 58213 &nbsp;&nbsp;&nbsp; Order date: May 9<br/>Customer: Hye-jin Park, Park Design Studio, 412 Alder Street, Salem", st("R", 10.4, 14.5, spaceAfter=6)),
           grid([["Item", "Qty", "Price"],
                 ["Ergo-Plus Office Chair", "2", "$240.00"],
                 ["Harbor Standing Desk (final sale)", "1", "$360.00"],
                 ["Assembly service (standing desk)", "1", "$30.00"],
                 ["Delivery", "", "$45.00"],
                 ["<b>Total</b>", "", "<b>$675.00</b>"]], [W * 0.6, W * 0.12, W * 0.22]),
           Spacer(1, 4), Paragraph("Estimated delivery date: May 14", st("R", 10.4, 14.5))]),
      Spacer(1, 9),
      box([Paragraph("To: support@brightlinefurniture.com<br/>From: Hye-jin Park &lt;hpark@parkdesignstudio.com&gt;<br/>Date: May 16<br/>Subject: Order 58213", st("R", 10.4, 14.5, spaceAfter=8)),
           Paragraph("To whom it may concern,", PS),
           Paragraph("My order arrived on schedule, and the delivery team was courteous. The chairs are comfortable, and two of my designers are already using them. "
                     "However, the standing desk arrived with a long scratch across the top. I know that I cannot send it back, but I would appreciate a partial refund or a replacement desktop.", PS),
           Paragraph("I should also mention that I had hoped to look at the desk in person before placing my order, but your showroom was closed on the day I stopped by. Despite these issues, I would be happy to shop with you again.", PS),
           Paragraph("Hye-jin Park", PS)]),
      PageBreak(), Paragraph("<b>Questions 186-190</b>", st("S", 10.3, 14, spaceAfter=8)), qpair([(n, q, o) for n, q, o, a, w in T])]
SimpleDocTemplate(str(ROOT / "data/workbook/Rec_Set_1127.pdf"), pagesize=A4, leftMargin=36, rightMargin=36, topMargin=34, bottomMargin=34, title="녹화용 세트").build(s)

k = [Paragraph("녹화용 세트 정답 · 근거", st("K", 15, 21)), Spacer(1, 6)]
for n, stem, o, a, why in P5 + D + T:
    k += [Paragraph(f"<b>{n}. ({a}) {o['ABCD'.index(a)]}</b>", st("K", 10, 14)), Paragraph(why, st("K", 9.2, 13.5, "#444444")), Spacer(1, 5)]
SimpleDocTemplate(str(ROOT / "data/workbook/Rec_Set_1127_key.pdf"), pagesize=A4, leftMargin=36, rightMargin=36, topMargin=34, bottomMargin=34).build(k)
print("ok", " ".join(f"{n}{a}" for n, _, _, a, _ in P5 + D + T))
