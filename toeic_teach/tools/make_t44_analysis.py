"""TEST 44 설계 근거: 기출 실측 + 동하 오답 데이터 요약 (2쪽) -> data/workbook/RC_Test44_Analysis.pdf"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

ROOT = Path(__file__).resolve().parent.parent
F = str(ROOT / "tools/fonts") + "/"
pdfmetrics.registerFont(TTFont("N", F + "NanumGothic-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NB", F + "NanumGothic-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DJ", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
registerFontFamily("N", normal="N", bold="NB", italic="N", boldItalic="NB")
BLUE = colors.HexColor("#1a56b8"); GREY = colors.HexColor("#555555"); PALE = colors.HexColor("#eef2f8")
def st(f="N", s=9.2, l=None, c=colors.black, **k): return ParagraphStyle("x", fontName=f, fontSize=s, leading=l or s * 1.45, textColor=c, **k)
T, H, K, S = st("NB", 16, 22), st("NB", 11.5, 16, BLUE, spaceBefore=8, spaceAfter=3), st(), st(s=8.2, c=GREY)
import re as _re
def P(t, style):
    t = t.replace("→", '<font name="DJ">→</font>').replace("①", "(1)").replace("②", "(2)").replace("③", "(3)")
    return Paragraph(t, style)
W = A4[0] - 76

def table(rows, widths, head=True):
    t = Table([[P(str(c), st("NB" if (head and i == 0) else "N", 8.6)) for c in r] for i, r in enumerate(rows)],
              colWidths=[W * x for x in widths], repeatRows=1 if head else 0)
    sty = [("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b8b8b8")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if head: sty.append(("BACKGROUND", (0, 0), (-1, 0), PALE))
    t.setStyle(TableStyle(sty)); return t

s = [P("실전 TEST 44 — 기출 분석 노트", T),
     P("이 세트는 아래 숫자에 맞춰 만들었어. 출처: ① 실제 기출 20회(ETS 기출 5권 10회 + 1000제 Vol.4 10회) 글자 인식 전수 측정, "
       "② 1000제 Vol.4 해설집 삼중지문 30세트 연계 표시 판독, ③ 형 오답 기록(P5 180문항, P7 Test 5·6·TEST 43).", S),

     P("1. Part 5 — 회당 구성은 거의 고정", H),
     table([["유형", "실제(회당)", "TEST 44", "실제 출제 방식"],
            ["어휘", "10~11", "11", "같은 품사의 흔한 단어 4개. 뜻이 아니라 <b>짝(연어)</b>으로 갈림 (conduct a survey, familiar with)"],
            ["품사 자리", "7~8", "8", "선지가 같은 어근 4개. 빈칸 앞뒤 1~2단어로 3초"],
            ["전치사·접속사·부사", "4~7", "6", "선지에 <b>품사를 섞음</b> (during / while / whereas / meanwhile) → 빈칸 뒤 동사 유무"],
            ["동사 형태(수·태·시제·꼬리)", "2~3", "3", "수일치 → 태 → 시제 순서. 동사 개수 함정 1개"],
            ["대명사·한정사", "1~2", "2", "소유격 / anyone who 같은 짝"]], [0.24, 0.12, 0.1, 0.54]),
     P("· 선지가 두 단어 이상인 문항 17% (TEST 44: 17%) · 120번대로 갈수록 문장이 길어짐(13.8 → 15.6단어)", S),

     P("2. Part 6 — 문장 고르기 자리는 세트마다 다름", H),
     table([["항목", "실제", "TEST 44"],
            ["지문 종류", "이메일 31% · 기사 14% · 공지 13% · 광고 9%", "이메일 · 기사 · 공지 · 광고"],
            ["문장 고르기 위치", "1번째 14% · 2번째 22% · <b>3번째 39%</b> · 4번째 22%", "133(3번째) · 136(2번째) · 142(4번째) · 143(1번째)"],
            ["나머지 3문항", "문맥 어휘 · 시제/태 · 연결어 · 대명사", "같은 비율"]], [0.2, 0.47, 0.33]),

     P("3. Part 7 — 질문 틀과 선지 설계", H),
     table([["항목", "실제(회당)", "TEST 44"],
            ["단일 구성", "2-2-2-2-3-3-3-4-4-4 (20회 중 12회)", "같음"],
            ["주제·목적 / 사실확인 / 추론 / 세부", "4.9 / 8.3 / 13.8 / 20.5", "5 / 10 / 13 / 16"],
            ["동의어 / 삽입 / 의도", "2.5 / 2 / 1.6~2", "3 / 2 / 2"],
            ["많이 나오는 질문 틀", "What is indicated about ~ (50) · suggested (38) · 문장 삽입 (26) · concluded (20) · most likely true (17) · Who most likely is (15)", "같은 틀 위주"],
            ["정답 선지가 지문 단어를 쓰는 비율", "45%", "51%"],
            ["<b>오답이 정답보다 지문 단어를 더 많이 쓰는 문항</b>", "<b>58%</b>", "63%"],
            ["정답이 혼자 제일 긴 문항", "12%", "12%"]], [0.38, 0.4, 0.22]),
     P("→ 실제 시험은 <b>지문과 똑같이 생긴 선지가 함정</b>이고 정답은 돌려 말한다. 형이 틀린 175(equipment), 185(conference)가 이 구조.", S),

     P("4. 삼중지문 연계 위치 (해설집 30세트 · 연계 60문항)", H),
     table([["연계 쌍", "나온 세트", "TEST 44"],
            ["<b>2-3</b>", "<b>28/30 (93%)</b>", "190 · 195 · 199 (세 세트 모두)"],
            ["1-2", "19/30 (63%)", "188 · 198"],
            ["1-3", "12/30 (40%)", "194"]], [0.2, 0.3, 0.5]),
     P("→ 세 번째 지문은 30세트 전부 연계에 쓰였다. 3번째 지문을 읽을 때는 '앞에서 본 이름·날짜·숫자·품목'을 찾아 화살표.", S),
     P("· 이중지문은 세트당 연계 1문항(177, 183). 연계는 '두 군데 한 번 잇기'로만 냈다 (TEST 43-193 같은 네 단계 계산 없음).", S),

     PageBreak(),
     P("5. 형 오답 데이터 → TEST 44에 넣은 것", H),
     table([["형 약점 (근거)", "TEST 44 문항"],
            ["P5 어휘 짝 (오답 180 중 약 50)", "103 proof of · 106 packed securely · 108 conduct a survey · 111 familiar with · 113 temporary basis · 118 comply with · 121 strong demand · 124 address concerns"],
            ["P5 품사 자리 (32)", "101 · 107 · 110 · 115 · 119 · 123 · 126 · 128"],
            ["P5 전접부 (32)", "104 during · 109 while · 114 except · 120 Once · 125 whether · 130 so ~ that"],
            ["P5 동사 개수 · anyone who (반복 오답)", "122 spending (동사 will receive 1개) · 117 Anyone who is"],
            ["P6 가리키는 말·모순 (Test 5-139/141)", "133 there · 136 it · 142 · 143"],
            ["P7 지문에 없는 추론 (Test 6-148·193·197·199)", "153 reasonably priced · 199 more expensive"],
            ["P7 역할·단어 바꿔치기 (175, 185)", "148 · 159 · 162 · 167 · 172"],
            ["P7 한정어 (all / always / only)", "156 all members · 186 always · 191-195 free(대상)"],
            ["P7 다의어 (office · rest · foundation · public)", "151 foundation · 149 closed to the public · 169 run for office · 174 rest · 184 address · 197 terms · 127 issue"],
            ["P7 서명·첫 줄 (Test 6-168)", "151 · 172 Who most likely is"],
            ["P7 연계 (2-3 위주)", "177 · 183 · 188 · 190 · 194 · 195 · 198 · 199"]], [0.38, 0.62]),

     P("6. 실제와 비교 (tools/measure_real.py)", H),
     table([["항목", "실제 20회", "TEST 44"],
            ["P5 문장 길이", "13.6단어", "14.2"], ["P6 지문 길이", "99.7단어", "92"],
            ["P7 지문 길이 2 / 3 / 4문항", "112 / 147 / 190", "103 / 128 / 175"],
            ["P7 이중 / 삼중", "285 / 418 (중앙값 372)", "265 / 318"],
            ["P7 문장 길이", "17.4단어", "16.5"]], [0.4, 0.3, 0.3]),
     P("· 삼중 지문이 실제 평균보다 짧고 긴 단어 비율도 조금 낮아. 시간이 남는다고 실제도 그렇다고 생각하면 안 돼.", S),

     P("7. 풀 때", H),
     table([["P5", "P6", "P7 단일", "이중·삼중", "확인 + 마킹"], ["11분", "8분", "26분", "25분", "5분"]], [0.2] * 5),
     P("· 파트 끝날 때마다 마킹 · 확신 없는 문항은 '?' · 고르기 전에 '이거 지문 몇 번째 줄?' → 손가락으로 못 짚으면 버리기", K),
     P("· 다 풀면 틀린 번호 + 고른 답 + '?' 번호 + 끝난 시각 보내기 → P5 오답은 다음 날 백지 재풀이", K),
     ]
SimpleDocTemplate(str(ROOT / "data/workbook/RC_Test44_Analysis.pdf"), pagesize=A4, leftMargin=38, rightMargin=38, topMargin=36,
                  bottomMargin=36, title="TEST 44 기출 분석 노트").build(s)
print("ok")
