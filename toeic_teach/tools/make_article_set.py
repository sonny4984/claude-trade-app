"""11/27 지문 유형 3: 기사(article) 5세트 (기출 구조를 본떠 새로 씀) → data/workbook/Article5_1127.pdf, Article5_1127_key.pdf"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
ROOT = Path(__file__).resolve().parent.parent
L = "/usr/share/fonts/truetype/liberation/"
for n, f in [("S", "LiberationSans-Regular"), ("SB", "LiberationSans-Bold"), ("R", "LiberationSerif-Regular"), ("RB", "LiberationSerif-Bold")]:
    pdfmetrics.registerFont(TTFont(n, L + f + ".ttf"))
pdfmetrics.registerFont(TTFont("K", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))
registerFontFamily("S", normal="S", bold="SB", italic="S", boldItalic="SB"); registerFontFamily("R", normal="R", bold="RB", italic="R", boldItalic="RB")
registerFontFamily("K", normal="K", bold="K", italic="K", boldItalic="K")
st = lambda f, s, l, c="#000000", **k: ParagraphStyle("x", fontName=f, fontSize=s, leading=l, textColor=colors.HexColor(c), **k)
W = A4[0] - 72
Q, O = st("S", 10.2, 13.8), st("S", 10, 13.4, leftIndent=16)
INS = ["[1]", "[2]", "[3]", "[4]"]
def ins(sent): return f"In which of the positions marked [1], [2], [3], and [4] does the following sentence best belong?<br/>\"{sent}\""

# qs: (stem, opts, correct_index, why) — 출력 위치는 TG로 섞음
SETS = [
 dict(start=147, title="Corvin Bakery to Move", paras=[
  "HARBORVIEW (May 3)—Corvin Bakery, a family-owned shop that has operated on Pier Street for 35 years, will move to a larger space on Market Avenue next month. The new location will include a seating area for 40 customers, something the original shop never had. \"Our regulars have been asking for a place to sit and enjoy their coffee for years,\" said owner Lucia Corvin.",
  "The Pier Street shop will close on May 28, and the Market Avenue location is scheduled to open on June 5. During the week in between, orders for birthday cakes can still be picked up at the company's production kitchen on Fourth Street."],
  qs=[("What is the article mainly about?", ["A business that is relocating", "A bakery that has a new owner", "The opening of a production kitchen", "A bakery's anniversary celebration"], 0, "will move to a larger space = relocating. 35년은 영업 기간일 뿐 (D 함정)"),
      ("What is indicated about the shop on Pier Street?", ["It does not have space for customers to sit.", "It sells only birthday cakes.", "It is located on Fourth Street.", "It will remain open until June 5."], 0, "seating area ... something the original shop never had (바꿔 말하기). C는 주방 위치, D는 새 매장 개장일")]),
 dict(start=151, title="Grantley Library Launches Tool Lending Program", paras=[
  "GRANTLEY (October 12)—Residents of Grantley can now borrow more than books from their public library. Starting this month, the main branch on Hill Road offers a collection of over 200 household tools, including drills, ladders, and garden equipment. Anyone with a valid library card may check out up to three tools at a time for one week.",
  "The program was funded by a grant from the Grantley Home Improvement Association. \"Many residents need a tool for only one small project,\" said library director Owen Pratt. \"Buying it doesn't make sense, and storing it takes up space.\"",
  "Mr. Pratt added that the library plans to extend the program to its two smaller branches next spring if demand remains strong. Volunteers are also needed to inspect and clean returned tools; interested individuals can sign up at the information desk."],
  qs=[("What is the purpose of the article?", ["To announce a new library service", "To report on a home improvement contest", "To advertise a hardware store", "To introduce a new library director"], 0, "borrow more than books = 새 서비스. D: Pratt은 원래 관장(new 아님)"),
      ("The word \"extend\" in paragraph 3, line 1, is closest in meaning to", ["lengthen", "expand", "postpone", "repair"], 1, "extend the program to its two smaller branches = 다른 지점으로 넓히다 → expand. lengthen(길이·기간 연장)은 함정"),
      ("According to the article, how can people help with the program?", ["By cleaning items that have been returned", "By donating their used tools", "By contributing money to an association", "By teaching a workshop"], 0, "Volunteers ... inspect and clean returned tools. C: 협회는 돈을 '준' 쪽")]),
 dict(start=155, title="Coastal Air Adds Direct Route to Montreal", paras=[
  "HALIFAX (February 8)—Coastal Air announced on Tuesday that it will begin offering direct flights between Halifax and Montreal on April 1. —[1]—. Currently, travelers between the two cities must change planes in Quebec City, which adds about two hours to the trip.",
  "The new route will operate twice daily, with morning and evening departures. —[2]—. Introductory one-way fares will start at $129 for tickets purchased before March 15.",
  "\"Business travelers have told us that time is their biggest concern,\" said Coastal Air spokesperson Hannah Doyle. —[3]—. The airline expects the route to be especially popular with employees of companies that have offices in both cities.",
  "Coastal Air, which currently serves twelve destinations in eastern Canada, plans to announce additional routes later this year. —[4]—."],
  qs=[("What is the main purpose of the article?", ["To report on a new flight service", "To describe changes to airport security", "To announce the opening of an office in Montreal", "To explain why ticket prices have increased"], 0, "will begin offering direct flights"),
      ("What is suggested about travel between Halifax and Montreal at present?", ["It requires a stop in another city.", "It is available only in the evening.", "It costs less than $129.", "It is offered by Coastal Air twice a day."], 0, "Currently ... must change planes in Quebec City. D는 새 노선(미래) 얘기"),
      (ins("The new schedule will allow them to attend a full day of meetings and return home the same night."), INS, 2, "them = 바로 앞 인용의 Business travelers. [2] 앞에는 them이 받을 사람이 없음")]),
 dict(start=164, title="Ferro Motors to Expand Plant in Easton", paras=[
  "EASTON (June 20)—Ferro Motors, a manufacturer of electric scooters, will invest $40 million to expand its assembly plant in Easton, company officials announced yesterday. The expansion will add a second production line and a new testing facility, and it is expected to create approximately 300 jobs over the next two years.",
  "The decision follows a year of record sales. Ferro sold more than 85,000 scooters last year, nearly double the figure from the year before. \"Demand has grown faster than we predicted,\" said Ferro's chief operating officer, Raj Mehta. \"Our current line simply cannot keep up.\"",
  "Construction is set to begin in September. Ferro will hold a job fair at the Easton Community Center on August 2 for positions in assembly, quality control, and maintenance. Applicants with experience in electrical systems are particularly encouraged to attend.",
  "Easton mayor Claire Dubois welcomed the news. \"Ferro has been a strong partner since it opened here eight years ago,\" she said. \"This expansion confirms that Easton is a good place to do business.\""],
  qs=[("What is NOT mentioned as part of the expansion?", ["A second production line", "A testing facility", "Approximately 300 new jobs", "A new headquarters building"], 3, "A·B·C는 1문단에 다 있음. 본사(headquarters) 얘기는 없음"),
      ("Why is Ferro Motors expanding the plant?", ["To meet increased demand", "To reduce production costs", "To begin making a new type of vehicle", "To replace outdated equipment"], 0, "Demand has grown faster ... current line cannot keep up"),
      ("Who most likely is Ms. Dubois?", ["A Ferro Motors employee", "A local government official", "A job fair organizer", "A construction manager"], 1, "Easton mayor(시장) = 지방 정부 공무원"),
      ("The word \"set\" in paragraph 3, line 1, is closest in meaning to", ["placed", "scheduled", "adjusted", "hardened"], 1, "is set to begin in September = 9월에 시작할 예정 → scheduled")]),
 dict(start=173, title="Local Firm Turns Coffee Waste into Furniture", paras=[
  "PORTVILLE (March 14)—Every day, Portville's cafés throw away hundreds of kilograms of used coffee grounds. Since last year, Greenmark Designs has been collecting some of that waste and turning it into tables, chairs, and shelves. —[1]—.",
  "The company was founded by Ana Silva, a former architect, and her business partner, Leo Grant, who previously managed a recycling plant. Greenmark mixes dried coffee grounds with a plant-based glue and presses the mixture into strong panels. —[2]—. \"The panels are lighter than wood and naturally resist moisture,\" Ms. Silva explained.",
  "At first, Greenmark sold its furniture only through its Web site. —[3]—. This month, however, the company opened a showroom on Bay Street, where customers can see and test the products in person.",
  "Greenmark currently works with eighteen cafés, but Mr. Grant hopes to double that number by the end of the year. \"Each café that joins means less waste going to the landfill,\" he said. —[4]—."],
  qs=[("What is the article mainly about?", ["A company that makes products from waste material", "A new café opening on Bay Street", "A city program to reduce landfill waste", "A competition for furniture designers"], 0, "coffee grounds → tables, chairs, shelves. B: Bay Street은 쇼룸"),
      ("What is indicated about Mr. Grant?", ["He has experience in the recycling industry.", "He used to work as an architect.", "He owns several cafés.", "He designed the company's Web site."], 0, "previously managed a recycling plant. B는 Silva 경력 (사람 바꿔치기)"),
      ("According to Ms. Silva, what is an advantage of the panels?", ["They are inexpensive to produce.", "They are heavier than wood.", "They come in many colors.", "They are not easily damaged by water."], 3, "naturally resist moisture = 물에 잘 안 상함. B는 lighter의 반대"),
      (ins("Some customers, however, wanted to touch the furniture before buying it."), INS, 2, "온라인으로만 팔았다 → [그런데 만져 보고 사고 싶어 하는 손님도] → 그래서 쇼룸 오픈")]),
]
TG = {147: 3, 148: 1, 151: 2, 152: 1, 153: 0, 155: 1, 156: 3, 157: 2, 164: 3, 165: 0, 166: 2, 167: 1, 173: 2, 174: 0, 175: 3, 176: 2}

def art_box(title, paras):
    rows = [Paragraph(f"<b>{title}</b>", st("RB", 12, 16, spaceAfter=8, alignment=1))] + [Paragraph(p, st("R", 10.6, 15.4, spaceAfter=7, firstLineIndent=14)) for p in paras]
    t = Table([[rows]], colWidths=[W * 0.86])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.black), ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14), ("TOPPADDING", (0, 0), (-1, -1), 10)]))
    o = Table([[t]], colWidths=[W]); o.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")])); return o

s = [Paragraph("지문 유형 3: 기사(article) 5세트 (11/27)", st("K", 15, 21)),
     Paragraph("기출 구조(주제·NOT·동의어·문장 삽입·사람 정체·바꿔 말하기)는 그대로, 내용은 새로 썼어. 정답은 Article5_1127_key.pdf.", st("K", 9.2, 13.5, "#555555")), Spacer(1, 10)]
key = []
for i, S in enumerate(SETS):
    if i: s.append(PageBreak())
    a = S["start"]; b = a + len(S["qs"]) - 1
    s += [Paragraph(f"<b>Questions {a}-{b}</b> refer to the following article.", st("S", 10.3, 14, spaceAfter=8)), art_box(S["title"], S["paras"]), Spacer(1, 12)]
    cells = []
    for qi, (q, opts, ci, why) in enumerate(S["qs"]):
        n = a + qi; opts = list(opts)
        if opts != INS:
            right = opts.pop(ci); opts.insert(TG[n], right)
        else:
            right = opts[ci]
        assert opts.index(right) == TG[n], n
        cells.append([Paragraph(f"<b>{n}.</b> {q}", Q)] + [Paragraph(f"({l}) {o}", O) for l, o in zip("ABCD", opts)] + [Spacer(1, 9)])
        key.append((n, "ABCD"[TG[n]], right, why))
    half = (len(cells) + 1) // 2
    g = Table([[[x for c in cells[:half] for x in c], [x for c in cells[half:] for x in c]]], colWidths=[W / 2, W / 2])
    g.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 10)]))
    s.append(g)
SimpleDocTemplate(str(ROOT / "data/workbook/Article5_1127.pdf"), pagesize=A4, leftMargin=36, rightMargin=36, topMargin=34, bottomMargin=34, title="기사 5세트").build(s)

METHOD = ["<b>추천 대응법 (기사)</b>",
          "① 제목 + 첫 문단 두 문장 = 주제. 여백에 한국어 한 줄 (예: 빵집 이전)",
          "② 문단마다 옆에 한 단어 라벨: 배경 / 숫자 / 인용 / 앞으로",
          "③ 사람 이름 = 직함과 같이 동그라미 (Grant-재활용 / Silva-건축가). 사람 바꿔치기 함정 대비",
          "④ 문장 삽입: 넣을 문장의 신호어(them·however·also·this) 먼저 → 그걸 받아 줄 앞 문장 찾기",
          "⑤ 동의어: 사전 뜻 말고 그 문장에 넣어서 해석 (extend → expand / set → scheduled)"]
k = [Paragraph("기사 5세트 정답 · 근거", st("K", 15, 21)), Spacer(1, 6)] + [Paragraph(x, st("K", 9.6, 14.5)) for x in METHOD] + [Spacer(1, 10)]
for n, a, o, w in key:
    k += [Paragraph(f"<b>{n}. ({a}) {o}</b>", st("K", 10, 14)), Paragraph(w, st("K", 9.2, 13.5, "#444444")), Spacer(1, 5)]
SimpleDocTemplate(str(ROOT / "data/workbook/Article5_1127_key.pdf"), pagesize=A4, leftMargin=36, rightMargin=36, topMargin=34, bottomMargin=34).build(k)
print("ok", " ".join(f"{n}{a}" for n, a, o, w in key))
