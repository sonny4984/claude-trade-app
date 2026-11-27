"""11/25 약점 메우기 오답 17문항: 왼쪽 문제, 오른쪽 자세한 해설(동하 메모 질문에 답) -> data/workbook/Weak_Side_1125b.pdf"""
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

MINE = {52: "using", 53: "resulted", 54: "announcement", 58: "detail", 62: "work", 64: "accessible", 72: "in order to",
        75: "be submitted", 81: "applied", 85: "will provide", 88: "were reviewed", 92: "to", 95: "across", 99: "therefore", 100: "for"}
EX = {
 52: ["<b>시제 있는 동사부터 세자.</b> The printer my coworkers ___ most often <b>is located</b> ... → 진짜 동사 is located가 이미 있어.",
      "그런데 <b>명사(printer) + 명사(coworkers) + 빈칸</b> 모양이 보이지? 이건 <b>that 생략</b> 신호야.",
      "The printer <u>(that) my coworkers ___ most often</u> is located → 괄호 안에도 주어(coworkers)가 있으니 <b>동사</b>가 필요해.",
      "coworkers는 복수 → <b>use</b>. using은 동사가 아니라서 괄호 안 문장이 안 돼. (같은 함정 4번째)"],
 53: ["<b>형 메모 '분사구문'까지는 맞았어.</b>",
      "콤마 앞에 동사 <b>reorganized</b>가 이미 있고, 콤마 뒤에 접속사가 없어 → 동사를 또 쓸 수 없어 → <b>-ing 꼬리</b>.",
      "resulted는 과거 동사로 읽히면 동사 2개가 되고, p.p.로 읽어도 result는 <b>자동사</b>라 수동 꼬리(-ed)가 안 돼.",
      "덩어리: <b>, resulting in</b> + 결과 = 그 결과 ~하게 되다."],
 54: ["진짜 동사는 <b>issued</b>야. 빈칸은 꼬리 자리.",
      "빈칸 뒤에 <b>its plans</b>라는 <b>목적어</b>가 있어 → 목적어를 받을 수 있는 건 동사 성질이 있는 <b>-ing</b> → announcing.",
      "명사 announcement는 뒤에 목적어를 바로 못 받아 (announcement <u>of</u> its plans처럼 of가 필요해).",
      "같은 모양: a letter <b>confirming</b> the order / an e-mail <b>announcing</b> the change."],
 58: ["<b>형 메모 '자세한 = detail 없나?' → 없어.</b> detail은 명사(세부 사항)·동사(자세히 설명하다)야.",
      "형용사 '자세한'은 <b>detailed</b>야. the ___ <b>instructions</b> → 명사 앞 → 형용사 → detailed.",
      "detailing은 '자세히 설명하는'이라 설명서가 스스로 설명하는 말이 돼서 어색해. 같은 짝: detailed information, a detailed report."],
 62: ["<b>be accustomed to + V-ing</b> = ~하는 데 익숙하다. 여기 to는 <b>전치사</b>라 뒤에 동명사가 와.",
      "to를 보자마자 동사원형을 고르면 걸리는 함정이야.",
      "to가 전치사인 덩어리 외우기: <b>look forward to</b> V-ing, <b>be committed to</b> V-ing, <b>be used to</b> V-ing, <b>be dedicated to</b> V-ing."],
 64: ["주어가 <b>사람</b>(staff)이고 뒤에 <b>to enter</b>가 와 → <b>be permitted to V</b> = ~하는 것이 허락되다.",
      "accessible은 <b>장소·물건</b>이 접근 가능하다는 말이야: The server room is accessible only to staff.",
      "possible·probable도 사람 주어 + to V로 못 써 (It is possible for staff to enter 처럼 It을 써야 해)."],
 72: ["빈칸 뒤 <b>hands-on training</b>은 <b>명사</b>야.",
      "in order to는 뒤에 <b>동사원형</b>이 와야 해 (in order to <u>improve</u>). 명사 앞엔 못 와.",
      "명사 ___ 명사 → <b>A as well as B</b> (A뿐 아니라 B도). classroom instruction <b>as well as</b> hands-on training.",
      "now that은 접속사(뒤에 문장), above all은 부사라 둘 다 명사를 못 이어."],
 75: ["주어 Small businesses 뒤 <b>동사 자리</b>야. 그리고 빈칸 뒤에 <b>목적어</b>(up to two grant applications)가 있어.",
      "목적어가 있으면 <b>능동</b> → may submit. be submitted는 수동이라 목적어를 못 받고, 조동사 없이 be 원형만으로는 동사가 안 돼.",
      "submits는 단수라 businesses(복수)랑 안 맞아. 순서: <b>수일치 → 태 → 시제</b>."],
 81: ["<b>형 메모 'A, D 헷갈림'.</b> 승진은 회사가 <b>시켜 주는</b> 것 → 사람이 주어면 <b>수동</b>: <b>be promoted to</b> + 직책.",
      "promoted(능동)를 쓰려면 뒤에 승진시킨 대상이 와야 해: The company promoted <u>Mr. Okoro</u> to manager.",
      "applied to regional manager는 '지역 매니저에게 지원했다'가 돼서 뜻이 안 맞아 (apply <b>for</b> a position이 맞는 짝)."],
 85: ["주어 a full report는 <b>제공되는</b> 쪽이야. 그리고 빈칸 뒤에 목적어 없이 바로 to the building owner가 와.",
      "목적어 없음 + 받는 쪽 → <b>수동</b> → is provided.",
      "will provide를 쓰면 '보고서가 (무언가를) 제공한다'가 되는데 뒤에 목적어가 없어서 문장이 안 돼."],
 88: ["<b>Each of + 복수명사 → 단수 동사.</b> 진짜 주어는 each(각각)야.",
      "applications가 복수라서 were에 끌리는 게 함정이야. 같은 규칙: <b>One of</b> the ~s <b>is</b> / <b>Each of</b> the ~s <b>was</b>.",
      "지원서는 <b>검토되는</b> 쪽 + 뒤에 목적어 없음 → 수동 → <b>was reviewed</b>."],
 92: ["<b>형 메모 'A, C 헷갈림'.</b> 주제를 말할 때 쓰는 전치사는 <b>on</b>이야.",
      "workshop / seminar / class / lecture / presentation / decision <b>on</b> + 주제.",
      "Workshops <b>on</b> using the new software = 새 소프트웨어 사용<b>에 관한</b> 워크숍. to는 방향, by는 수단·기한."],
 95: ["<b>형 메모 'C, D?'</b> 둘 다 '맞은편'처럼 보이지만 모양이 달라.",
      "<b>opposite</b> + 장소 = ~의 맞은편 (바로 명사를 받음).",
      "<b>across from</b> + 장소 = ~의 맞은편 (from이 꼭 있어야 함). across만 있으면 '~을 가로질러'라는 뜻이야.",
      "빈칸 바로 뒤가 the public library(명사)니까 opposite."],
 99: ["<b>형 메모 '해석으로는 B 같은데 B는 전치사 아님?' → 아니야, in case는 접속사야.</b>",
      "<b>in case</b> + 문장(주어+동사) = ~할 경우에 대비해. 빈칸 뒤 the system crashes는 문장이니까 딱 맞아.",
      "<b>in case of</b> + 명사처럼 of가 붙어야 전치사야: in case of an emergency.",
      "therefore는 접속부사라 두 문장을 이어 주지 못해. regarding, due to는 전치사라 뒤에 문장을 못 받아. (in case 3회째)"],
 100: ["<b>in recognition of</b> = ~을 인정하여, ~에 대한 공로로. 통째로 외우는 덩어리야.",
       "for도 '~에 대해'로 해석돼서 끌리지만, recognition 앞에는 in만 와.",
       "비슷한 덩어리: in honor of(~을 기념하여), in appreciation of(~에 감사하여), in response to(~에 응하여)."],
}
W = landscape(A4)[0] - 60
rows = []
for n in sorted(MINE):
    stem, ch, a = items[n - 1]
    left = [Paragraph(f"<b>{n}.</b> {stem}", st("S", 10.5, 14.5)), Spacer(1, 3)]
    for k, o in enumerate(ch):
        mark = ""
        if k == a: mark = '  <font color="#1e8449"><b>◀ 정답</b></font>'
        elif o == MINE[n]: mark = '  <font color="#c0392b"><b>◀ 내 답</b></font>'
        left.append(Paragraph(f"({L[k]}) {o}{mark}", st("K", 10.5, 14.5)))
    right = [Paragraph(t, st("K", 9.6, 14.2)) for t in EX[n]]
    rows.append([left, right])
t = Table(rows, colWidths=[W * 0.42, W * 0.58])
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#f6f8fc")), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
s = [Paragraph("약점 메우기 52~102 오답 15문항 — 문제 + 해설 (형 메모 질문에 답)", st("K", 15, 21)),
     Paragraph("핵심: ① 시제 있는 동사부터 세기 (명사+명사+빈칸 = that 생략) ② 목적어 있나 → 능동/수동 ③ 전치사는 덩어리로", st("K", 9.5, 14, "#555555")),
     Spacer(1, 8), t]
SimpleDocTemplate(str(ROOT / "data/workbook/Weak_Side_1125b.pdf"), pagesize=landscape(A4), leftMargin=30, rightMargin=30, topMargin=28, bottomMargin=28).build(s)
print("ok")
