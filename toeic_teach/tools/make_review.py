"""Build the review pack PDF (plan + rule cards + 20-question retrieval quiz + answers). Korean, black & white.
Usage: python3 tools/make_review.py -> data/workbook/Review_1023.pdf"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

root = Path(__file__).resolve().parent.parent
pdfmetrics.registerFont(TTFont("NG", str(root / "tools/fonts/NanumGothic-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NG-B", str(root / "tools/fonts/NanumGothic-Bold.ttf")))
W = A4[0] - 28 * mm
st = lambda **k: ParagraphStyle("x", **k)
H1 = st(fontName="NG-B", fontSize=16, leading=22, spaceAfter=6)
H2 = st(fontName="NG-B", fontSize=12, leading=17, spaceBefore=8, spaceAfter=4)
B = st(fontName="NG", fontSize=10, leading=15)
S = st(fontName="NG", fontSize=9.2, leading=13.5)
SB = st(fontName="NG-B", fontSize=9.6, leading=14)
Q = st(fontName="NG", fontSize=10.2, leading=15, leftIndent=16, firstLineIndent=-16, spaceAfter=7)

PLAN = [
 ("1", "10분", "이 노트의 규칙 카드 14장: 왼쪽 칸만 보고 오른쪽을 말해본 뒤 확인"),
 ("2", "10분", "복습 퀴즈 20문항 (2지선다). 채점은 마지막 장"),
 ("3", "75분", "RC Practice Test 2 실전 풀이. 타이머, Part별 끝난 시각을 답안지에 적기"),
 ("4", "15분", "채점 → 틀린 번호와 '?' 번호, Part별 시각을 튜터에게 보내기"),
 ("5", "10분", "단어 시험지 vocab_s1, vocab_s2 (영어 보고 한국어 쓰기)"),
 ("+", "여유", "RC Practice Test 1 나머지 (101–130, 135–200)"),
]

CARDS = [
 ("빈칸 뒤가 절(주어+동사)인가, 명사인가?", "절 → while / once / although (접속사)<br/>명사 → during / despite (전치사)",
  "closed <b>while</b> it is being repaved / closed <b>during</b> the repairs"),
 ("when · while · as soon as · once · after · until 바로 뒤의 절", "미래 일이어도 <b>현재형</b>. will 금지",
  "show your card when you <b>exit</b> (will exit는 X)"),
 ("그 접속사 <b>앞</b>(주절)의 will은?", "써도 된다. 위치를 먼저 확인!",
  "I <b>will call</b> you as soon as I <b>get</b> home."),
 ("장소 명사, ____ + 주어 + 동사", "<b>where</b> = 거기서 (when은 시간 명사 뒤)",
  "the front desk, <b>where</b> a staff member will give you a receipt"),
 ("be accustomed to / look forward to / be dedicated to + ?", "<b>V-ing</b> (to가 전치사)",
  "accustomed to <b>working</b> long hours"),
 ("to 판별법", "to 뒤에 명사를 넣어 말이 되면 전치사 to → V-ing<br/>안 되면 부정사 to → 동사원형",
  "accustomed to long hours (O) / permitted to devices (X) → permitted <b>to use</b>"),
 ("in order to V", "~하기 <b>위해서</b> (목적). 원인(~때문에)은 because (of)",
  "<b>In order to</b> reduce costs, the company moved."),
 ("tangible / intangible", "실체가 있는, 눈에 보이는 / 무형의, 만질 수 없는",
  "<b>tangible results</b> = 숫자로 확인되는 성과"),
 ("until 4 P.M. / by 4 P.M.", "until = 4시까지 <b>계속</b> / by = <b>늦어도</b> 4시까지 (마감)",
  "stay open <b>until</b> 9 / submit <b>by</b> Friday"),
 ("go ___ effect", "<b>go into effect</b> = 시행되다 (take effect도 같은 뜻)", "The rule will go into effect on May 1."),
 ("for instance / instead / however / consequently / moreover", "예시 / 대신 / 대조 / 결과 / 첨가",
  "풀기 전에 앞뒤 관계를 한국어로 한 줄 요약"),
 ("substantial / sustained", "양이 많은(크기) / 오래 이어지는(기간)", "a <b>substantial</b> amount / <b>sustained</b> growth"),
 ("satisfied / satisfactory", "사람이 만족한 / 결과가 만족스러운", "satisfied customers / satisfactory results"),
 ("be necessary to V", "가능하다! (necessary to become ~)", "Skills are <b>necessary to</b> become an accountant."),
]

QUIZ = [
 ("The museum will be closed ------- the floors are being replaced.", "while", "during", "A", "뒤가 절 → 접속사."),
 ("Please wait in the lobby ------- the inspection.", "while", "during", "B", "뒤가 명사구 → 전치사."),
 ("We will send the invoice after the work ------- finished.", "is", "will be", "A", "after 뒤 절 → 현재형."),
 ("The manager ------- the results as soon as she receives them.", "will announce", "announces", "A", "as soon as 앞(주절) → will 가능."),
 ("Please return the books to the library, ------- a volunteer will check them in.", "when", "where", "B", "장소(the library) 뒤 → where."),
 ("The new hires are not accustomed to ------- such long hours.", "work", "working", "B", "to = 전치사 → V-ing."),
 ("Visitors are not allowed ------- the stage.", "to enter", "entering", "A", "be allowed to + 동사원형."),
 ("------- attract more customers, the store extended its hours.", "In order to", "Because of", "A", "뒤가 동사원형 + 목적."),
 ("------- the heavy traffic, the bus arrived late.", "In order to", "Because of", "B", "뒤가 명사 + 원인."),
 ("The new software has produced ------- results: a 30 percent drop in errors.", "intangible", "tangible", "B", "숫자로 확인되는 성과."),
 ("Please submit your report ------- noon on Friday.", "by", "until", "A", "제출 = 한 번 하는 일 → 마감 by."),
 ("The library is open ------- 9 P.M. on weekdays.", "by", "until", "B", "열려 있는 상태가 계속 → until."),
 ("The new dress code will go ------- effect next month.", "onto", "into", "B", "go into effect."),
 ("Sales fell in March; -------, profits rose because costs were cut.", "however", "for instance", "A", "하락 vs 상승 = 대조."),
 ("The hotel offers many services; -------, guests can borrow bicycles for free.", "instead", "for instance", "B", "서비스의 예시."),
 ("The flight was canceled; -------, we took the train.", "instead", "moreover", "A", "비행기 대신 기차."),
 ("The storm damaged several roads; -------, many schools closed.", "for instance", "consequently", "B", "피해(원인) → 휴교(결과)."),
 ("The company has seen ------- growth for ten straight years.", "sustained", "satisfied", "A", "10년 연속 = 기간."),
 ("The inspector found the safety measures -------.", "satisfied", "satisfactory", "B", "사물(조치)이 만족스러움."),
 ("Good communication skills are ------- to succeed in sales.", "available", "necessary", "B", "성공하는 데 필요 = necessary to V."),
]

doc = SimpleDocTemplate(str(root / "data/workbook/Review_1023.pdf"), pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm,
                        topMargin=14 * mm, bottomMargin=16 * mm, title="Review 10/23")
grid = [("BOX", (0, 0), (-1, -1), 0.8, colors.black), ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")), ("VALIGN", (0, 0), (-1, -1), "TOP")]
story = [Paragraph("10/24 RC 복습 노트", H1),
         Paragraph("10/23에 틀리거나 헷갈린 것만 모았어. 읽기만 하지 말고 <b>왼쪽만 보고 오른쪽을 먼저 떠올린 다음</b> 확인해.", B),
         Paragraph("내일 순서", H2)]
t = Table([[Paragraph(x, SB) for x in ("#", "시간", "할 일")]] + [[Paragraph(a, S), Paragraph(b, S), Paragraph(c, S)] for a, b, c in PLAN],
          colWidths=[10 * mm, 18 * mm, W - 28 * mm])
t.setStyle(TableStyle(grid)); story += [t, Paragraph("규칙 카드 14장", H2)]
rows = [[Paragraph(x, SB) for x in ("단서 (이것만 보고 떠올리기)", "규칙", "예문")]]
rows += [[Paragraph(a, S), Paragraph(b, S), Paragraph(c, S)] for a, b, c in CARDS]
t = Table(rows, colWidths=[W * 0.33, W * 0.33, W * 0.34], repeatRows=1)
t.setStyle(TableStyle(grid)); story += [t, PageBreak(), Paragraph("복습 퀴즈 20문항", H1),
                                        Paragraph("2지선다. 답 옆에 이유를 한 단어로 적어봐 (예: '뒤 절', '마감', '대조'). 정답은 다음 장.", B), Spacer(1, 6)]
for i, (q, a, b, ans, why) in enumerate(QUIZ, 1):
    story.append(Paragraph(f"<b>{i}.</b> {q}<br/>(A) {a} &nbsp;&nbsp;&nbsp; (B) {b} &nbsp;&nbsp;&nbsp; 이유: ______________", Q))
story += [PageBreak(), Paragraph("퀴즈 정답", H1)]
rows = [[Paragraph(x, SB) for x in ("No.", "정답", "이유")]]
rows += [[Paragraph(str(i), S), Paragraph(f"({ans}) {a if ans == 'A' else b}", S), Paragraph(why, S)] for i, (q, a, b, ans, why) in enumerate(QUIZ, 1)]
t = Table(rows, colWidths=[12 * mm, 40 * mm, W - 52 * mm]); t.setStyle(TableStyle(grid)); story.append(t)
doc.build(story)
print("ok")
