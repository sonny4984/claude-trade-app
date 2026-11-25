"""11/25 약점 메우기 오답 17문항: 왼쪽 문제, 오른쪽 자세한 해설(동하 메모 질문에 답) -> data/workbook/Weak_Side_1125.pdf"""
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

MINE = {2: "careful", 3: "change", 5: "benefited", 6: "caution", 13: "efficient", 14: "benefited", 15: "regulate", 16: "shortly",
        17: "largest", 23: "respond", 26: "strength", 30: "considerable", 31: "entire", 36: "conveniently", 43: "interesting",
        47: "to contain", 51: "expecting"}
EX = {
 2: ["<b>형 메모 'When (S V) p.p.' → 정확해.</b>",
     "When과 followed 사이에 <b>they are</b>가 생략된 구조야: When (they are) ___ followed.",
     "복원하면 <b>be ___ p.p.</b> → p.p.(followed)를 꾸미는 건 <b>부사</b> → carefully.",
     "같은 모양: If properly installed / Once fully charged / When correctly used."],
 3: ["<b>형 메모 거의 맞는데 하나만 고치자: 여기 make는 5형식이 아니야.</b>",
     "make <b>바로 뒤</b>가 빈칸 → 빈칸이 <b>목적어</b> → 명사. (make changes = 변경하다, 3형식)",
     "change는 셀 수 있는 명사라 단수면 <b>a change</b>여야 해. a가 없으니 복수 <b>changes</b>. 형이 쓴 그대로야.",
     "5형식은 <b>make + 목적어 + 형용사</b>처럼 목적어가 먼저 있고 그 뒤에 빈칸이 올 때만: make <u>the process</u> simple."],
 5: ["<b>형 메모 정확해.</b> be(are) 뒤 보어 → 형용사 자리.",
     "선지에 진짜 형용사(beneficial, -al)와 분사(benefited)가 같이 있으면 <b>진짜 형용사가 거의 정답</b>.",
     "뜻으로도 확인: benefited = '혜택을 받은'. 프로그램이 혜택을 받는 게 아니라 회사에 <b>유익한</b> 것 → beneficial."],
 6: ["<b>형 메모 정확해.</b> proceed = 진행하다, <b>목적어 없는 자동사</b>. 대상은 with로 붙여: proceed with the plan.",
     "동사(proceed)와 전치사(with) <b>사이</b>에 끼어든 빈칸 → 동사를 꾸미는 <b>부사</b> → cautiously.",
     "같은 모양: respond quickly to / work closely with / comply fully with."],
 13: ["<b>형 질문: more ~ than도 as~as처럼 형용사·부사 둘 다 올 수 있어? → 응, 둘 다 가능해.</b>",
      "세트라서 부사인 게 아니라, <b>more·than을 지우고 남은 자리</b>로 정해. as~as랑 똑같은 방법이야.",
      "지우면: Harmon Logistics handles client shipments ___. → 주어+동사+목적어로 <b>문장 완전</b> → 동사를 꾸미는 <b>부사</b> efficiently.",
      "형용사가 오는 경우: Our service is more <b>efficient</b> than theirs. → be 뒤 보어니까 형용사."],
 14: ["<b>빈칸 뒤 include가 동사야.</b> (at Orion Systems는 전치사구라 괄호로 지워.)",
      "Staff ___ [at Orion Systems] <b>include</b> ... → 동사 앞은 <b>주어 = 명사</b> 자리.",
      "staff도 명사지만 '직원들이 무료 주차를 포함한다'는 말이 안 돼 → <b>staff benefits</b>(직원 복리후생)라는 <b>복합명사</b>.",
      "include가 복수 동사(s 없음)니까 복수 명사 <b>benefits</b>. benefited는 동사·분사라 주어가 못 돼."],
 15: ["<b>-ory는 형용사 꼬리야.</b> regulatory(규제의), mandatory(의무의), satisfactory(만족스러운), advisory, introductory.",
      "the ___ <b>environment</b> → 명사 앞 → 형용사 → regulatory.",
      "regulate는 동사, regulator는 사람(규제 기관)이라 명사 앞 수식이 안 돼."],
 16: ["<b>keep은 5형식 동사야.</b> keep + 목적어 + 형용사: keep the room <u>clean</u> / keep costs <u>low</u>.",
      "<b>possible은 형용사 맞아.</b> 그런데 as ___ as possible에서 possible은 빈칸 품사에 영향을 안 줘. '가능한 한 ___하게'라는 세트일 뿐이야.",
      "그래서 <b>as ~ as possible을 통째로 지우고</b> 봐: keep waiting times ___ → 목적어(waiting times) 상태 → 형용사 <b>short</b>.",
      "비교: Please respond as <b>quickly</b> as possible. → 지우면 respond ___ → 동사 꾸밈 → 부사."],
 17: ["<b>even + 비교급 = 훨씬 더</b>. even 뒤에는 무조건 비교급(-er / more ~).",
      "비교급을 강조하는 말: even, much, far, still, a lot, considerably.",
      "또 하나 단서: <b>an</b> even ___ number. 최상급은 <b>the</b> largest라 an이랑 못 써 → larger."],
 23: ["<b>맞아, highly(부사) + 형용사</b> 구조야. highly qualified / highly responsive / highly effective.",
      "being highly ___ to → be 뒤 보어 자리 → 형용사 <b>responsive</b>(-ive = 형용사 꼬리).",
      "respond는 동사라 be 뒤에 못 와. responsive to = ~에 잘 반응하는."],
 26: ["<b>-en이 붙으면 동사가 돼:</b> strong → strengthen, short → shorten, wide → widen, long → lengthen, broad → broaden.",
      "to ___ the company's position → <b>to 뒤 동사원형</b> + 목적어 → strengthen(강화하다).",
      "strength는 명사라 뒤에 목적어(the position)를 못 받아."],
 30: ["천천히 보자. have become ___ <b>shorter</b>.",
      "shorter는 형용사(비교급)고 become 뒤 보어야. 빈칸은 그 <b>shorter를 꾸미는</b> 자리야.",
      "<b>형용사를 꾸미는 건 부사</b> → considerably(상당히). '상당히 더 짧아졌다'.",
      "17번이랑 짝이야: 비교급 앞 강조 = even / much / far / considerably / significantly."],
 31: ["<b>made를 5형식으로 본 게 함정이야.</b> 여기는 <b>be made of = ~로 만들어지다</b>(수동태)야.",
      "빈칸 뒤 of recycled materials는 <b>전치사구</b>야. 목적어나 보어가 아니야.",
      "is made ___ of → 동사(made)와 전치사(of) 사이 → <b>부사</b> entirely(전부, 완전히). 6번 proceed ___ with랑 같은 모양.",
      "5형식 수동이면 형용사가 남아: The file is made <u>available</u> online. 이번엔 빈칸 바로 뒤에 of가 와서 아니야."],
 36: ["<b>find는 5형식 동사야.</b> find + 목적어 + 형용사 = ~가 …하다고 느끼다.",
      "found <u>our new online booking system</u> ___ → 목적어(시스템)의 상태 → 형용사 <b>convenient</b>.",
      "5형식 동사 6개만 외워: <b>make, keep, find, leave, consider, deem</b> + 목적어 + 형용사."],
 43: ["<b>감정 분사 규칙:</b> 사람이 느끼면 <b>-ed</b>, 감정을 주는 사물이면 <b>-ing</b>.",
      "the audience(사람)가 관심을 느낌 → <b>interested</b>. 'The speech was interesting'처럼 연설(사물)이면 -ing.",
      "같은 짝: interested/interesting, satisfied/satisfying, excited/exciting, delighted/delightful.",
      "remain + 형용사는 형이 맞게 봤어. -ed/-ing만 고르면 돼."],
 47: ["<b>designed to contain이 자연스러워 보이는 게 바로 함정이야.</b> 동사 개수를 세 봐.",
      "The survey <u>(that) the marketing team designed</u> ___ twenty questions.",
      "<b>명사(survey) + 명사(team) + 동사(designed)</b> = that 생략 신호. designed는 괄호 안 동사야.",
      "괄호를 지우면 The survey ___ twenty questions → 문장에 진짜 동사가 없어 → 빈칸이 동사 → <b>contained</b>.",
      "to contain을 넣으면 문장 전체에 본동사가 0개라 문장이 안 돼. (같은 함정 3회째)"],
 51: ["the way = '~하는 방식'. 뒤에 <b>주어 + 동사</b>가 붙어.",
      "the way <u>the designers</u> ___ <u>(that) it would (look)</u> → 주어 the designers 뒤에 <b>동사</b>가 필요 → <b>expected</b>.",
      "해석: 새 로비는 <b>디자이너들이 예상했던</b> 모습대로 보이지 않았다.",
      "expecting은 -ing라 혼자서 동사가 못 돼. 47번처럼 '주어 뒤에 동사 있나?'부터 확인."],
}
W = landscape(A4)[0] - 60
rows = []
for n in [2, 3, 5, 6, 13, 14, 15, 16, 17, 23, 26, 30, 31, 36, 43, 47, 51]:
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
s = [Paragraph("약점 메우기 오답 17문항 — 문제 + 해설 (형 메모 질문에 답)", st("K", 15, 21)),
     Paragraph("핵심 2개: ① 빈칸이 명사를 꾸미거나 be·remain·keep O·find O 뒤면 형용사, 나머지는 부사 ② 시제 있는 동사부터 세기", st("K", 9.5, 14, "#555555")),
     Spacer(1, 8), t]
SimpleDocTemplate(str(ROOT / "data/workbook/Weak_Side_1125.pdf"), pagesize=landscape(A4), leftMargin=30, rightMargin=30, topMargin=28, bottomMargin=28).build(s)
print("ok")
