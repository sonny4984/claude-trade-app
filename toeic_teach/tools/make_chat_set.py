"""11/27 지문 유형 2: 문자·채팅 5세트 (기출 구조를 본떠 새로 씀) → data/workbook/Chat5_1127.pdf, Chat5_1127_key.pdf"""
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

SETS = [
 dict(rng=(147, 148), kind="text-message chain", lines=[
  ("Mina Cho", "9:12 A.M.", "Hi, Paul. Are you still at the Fenwick warehouse?"),
  ("Paul Ortiz", "9:13 A.M.", "Just leaving. Why?"),
  ("Mina Cho", "9:14 A.M.", "The client called. They want 40 folding tables for Saturday instead of 30."),
  ("Paul Ortiz", "9:16 A.M.", "We only loaded 30 onto the truck. Let me go back in and check the shelves."),
  ("Mina Cho", "9:17 A.M.", "Thanks. If there aren't enough, I'll ask the Dalton branch."),
  ("Paul Ortiz", "9:22 A.M.", "Good news—there are plenty here."),
  ("Mina Cho", "9:23 A.M.", "Perfect. I'll update the order form.")],
  qs=[("What is suggested about the client?", ["It needs more tables than it originally requested.", "It has postponed an event.", "It wants a delivery to the Dalton branch.", "It has canceled part of an order."], "30 → 40개로 늘림 (instead of 30)"),
      ("At 9:22 A.M., what does Mr. Ortiz most likely mean when he writes, \"there are plenty here\"?", ["The warehouse has enough tables for the new order.", "The truck is too full to carry more items.", "He does not need Ms. Cho to call him again.", "The Dalton branch has extra tables."], "바로 앞: 선반 확인 + 모자라면 Dalton에 물어볼게 → 여기 충분해 = 창고에 10개 더 있음. D는 Dalton 단어 함정")]),
 dict(rng=(151, 152), kind="text-message chain", lines=[
  ("Grace Lim", "2:05 P.M.", "Daniel, my train from Brookfield is running about 40 minutes late."),
  ("Daniel Kerr", "2:06 P.M.", "Oh no. The client presentation starts at 3:00."),
  ("Grace Lim", "2:07 P.M.", "I know. The slides are already on the shared drive. Could you open the meeting for me?"),
  ("Daniel Kerr", "2:08 P.M.", "Sure. I can cover the sales figures, but I'm not familiar with the new pricing section."),
  ("Grace Lim", "2:09 P.M.", "That part comes last."),
  ("Daniel Kerr", "2:10 P.M.", "OK. I'll let the clients know you're on your way.")],
  qs=[("Why did Ms. Lim send the first message?", ["To report a delay", "To change a meeting location", "To request a copy of some slides", "To ask about a client's budget"], "train ... running 40 minutes late"),
      ("At 2:09 P.M., what does Ms. Lim imply when she writes, \"That part comes last\"?", ["She will arrive in time to present the pricing section herself.", "The pricing section needs to be revised.", "Mr. Kerr should skip the sales figures.", "The presentation will end earlier than planned."], "Kerr: 가격 부분은 잘 몰라 → 그건 맨 마지막 = 그때쯤 내가 도착해서 직접 함")]),
 dict(rng=(160, 163), kind="online chat discussion", lines=[
  ("Rosa Mendes", "10:02 A.M.", "Hi all. The Lisbon office is sending two engineers for the training next Tuesday. Where should we put them?"),
  ("Tom Hale", "10:03 A.M.", "Room 4B is free all day. It has space for six people."),
  ("Rosa Mendes", "10:04 A.M.", "Great. Our own team will be four people, so that works."),
  ("Anita Brooks", "10:06 A.M.", "Wait—Ken from the Denver office asked to join as well. He'll be connecting by video."),
  ("Tom Hale", "10:07 A.M.", "Then 4B won't work. It doesn't have a camera or a large screen."),
  ("Anita Brooks", "10:08 A.M.", "What about the main conference room?"),
  ("Tom Hale", "10:09 A.M.", "It's booked until noon. The training could start at 1:00 instead."),
  ("Rosa Mendes", "10:10 A.M.", "That's fine with me. Anita, can you let the engineers know about the new time?"),
  ("Anita Brooks", "10:11 A.M.", "Will do. I'll also send Ken the video link.")],
  qs=[("What is the discussion mainly about?", ["Arranging a space for a training session", "Hiring new engineers", "Repairing equipment in a meeting room", "Planning a trip to Lisbon"], "Where should we put them? → 방 정하기"),
      ("How many people will most likely attend the training in person?", ["Four", "Five", "Six", "Seven"], "우리 팀 4 + 리스본 엔지니어 2 = 6. Ken은 video라 제외 (7은 함정)"),
      ("At 10:07 A.M., what does Mr. Hale mean when he writes, \"Then 4B won't work\"?", ["The room is too small for the group.", "The room has been reserved by another team.", "The room is being renovated.", "The room lacks equipment needed for a remote participant."], "바로 뒤: camera·large screen 없음 + 바로 앞: Ken video 접속. A는 6명 수용이라 아님"),
      ("What will Ms. Brooks most likely do next?", ["Contact the engineers about a schedule change", "Book Room 4B", "Install a camera", "Travel to Denver"], "Rosa: Anita, 엔지니어들한테 새 시간 알려줄래? → Will do")]),
 dict(rng=(168, 171), kind="online chat discussion", lines=[
  ("Leah Novak", "9:40 A.M.", "Good morning, everyone. The customer survey results are in. Overall satisfaction went up, but many shoppers said our checkout lines are too long on weekends."),
  ("Sam Whitfield", "9:42 A.M.", "That matches what I see at the Elm Street store. Saturdays after 11 are the worst."),
  ("Leah Novak", "9:43 A.M.", "Sam, how many registers are open then?"),
  ("Sam Whitfield", "9:44 A.M.", "Usually three out of five. We don't have enough cashiers."),
  ("Priya Rao", "9:46 A.M.", "I can move two part-time workers from their Thursday shifts to Saturday. Thursdays are quiet."),
  ("Leah Novak", "9:47 A.M.", "Let's try that for a month and see if the comments change."),
  ("Priya Rao", "9:48 A.M.", "I'll update the schedule today and post it in the break room.")],
  qs=[("Who most likely is Mr. Whitfield?", ["A worker at a store location", "An employee of a survey company", "A customer who completed a survey", "A delivery driver"], "what I see at the Elm Street store + 계산대 수 앎 → 매장 직원. C는 '내가 본다' 함정"),
      ("What problem is being discussed?", ["Shoppers are unhappy with product quality.", "Some registers are broken.", "Shoppers wait a long time to pay on weekends.", "A store closes early on Saturdays."], "checkout lines are too long on weekends. B: 5개 중 3개만 여는 이유는 직원 부족이지 고장 아님"),
      ("At 9:46 A.M., what does Ms. Rao mean when she writes, \"Thursdays are quiet\"?", ["She prefers to work on Thursdays.", "The store will close on Thursdays.", "The survey received few responses on Thursdays.", "Fewer staff are needed on Thursdays."], "목요일 근무자 2명을 토요일로 옮길 수 있다 → 왜? 목요일은 한가해서 = 인원 덜 필요"),
      ("What will Ms. Rao most likely do today?", ["Conduct another survey", "Revise a work schedule", "Hire new cashiers", "Visit the Elm Street store"], "I'll update the schedule today = revise. C는 새로 뽑는 게 아니라 옮기는 것")]),
 dict(rng=(172, 175), kind="online chat discussion", lines=[
  ("Carlos Vega", "11:20 A.M.", "The caterer just told me they can't deliver lunch for Friday's workshop until 12:45."),
  ("Dana Lee", "11:21 A.M.", "Our lunch break is scheduled for 12:15."),
  ("Carlos Vega", "11:22 A.M.", "Right. Should we look for another caterer?"),
  ("Mei Tanaka", "11:24 A.M.", "It's too late for that. Why don't we just switch the afternoon session with the lunch break?"),
  ("Dana Lee", "11:25 A.M.", "You mean have Mr. Ahn give his talk from 12:15 to 12:45?"),
  ("Mei Tanaka", "11:26 A.M.", "Exactly. His talk is only 30 minutes long."),
  ("Carlos Vega", "11:27 A.M.", "I'll check with him. He's flying in Thursday night, so he should be available."),
  ("Dana Lee", "11:30 A.M.", "And I'll reprint the programs with the new times.")],
  qs=[("What problem does Mr. Vega mention?", ["A speaker has canceled.", "A caterer has raised its prices.", "A flight has been delayed.", "Food will arrive later than planned."], "can't deliver lunch until 12:45 (점심은 12:15). C는 flying 단어 함정"),
      ("At 11:24 A.M., what does Ms. Tanaka mean when she writes, \"It's too late for that\"?", ["The workshop has already started.", "There is not enough time to hire a different caterer.", "Mr. Ahn cannot change his flight.", "The programs have already been printed."], "that = 바로 앞 '다른 케이터링 찾을까?' → 그러기엔 늦었다"),
      ("What is suggested about Mr. Ahn?", ["He works for the caterer.", "He organized the workshop.", "He will give a short presentation.", "He will arrive on Friday morning."], "His talk is only 30 minutes = short presentation. D: Thursday night 도착 (요일 바꿔치기)"),
      ("What will Ms. Lee most likely do?", ["Update some printed materials", "Call the caterer", "Contact Mr. Ahn", "Book a flight"], "I'll reprint the programs. C는 Vega가 할 일 (사람 바꿔치기)")]),
]

def chat_box(lines, kind):
    rows = []
    for name, t, msg in lines:
        if kind.startswith("text"):
            rows.append(Paragraph(f"<b>{name} ({t})</b><br/>{msg}", st("R", 10.6, 14.6, spaceAfter=7)))
        else:
            rows.append(Paragraph(f"<b>{name} [{t}]</b> &nbsp;{msg}", st("R", 10.6, 14.6, spaceAfter=7)))
    w = W * (0.62 if kind.startswith("text") else 0.98)
    t = Table([[rows]], colWidths=[w])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.4, colors.black), ("ROUNDEDCORNERS", [8, 8, 8, 8]),
                           ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7f7f7")), ("LEFTPADDING", (0, 0), (-1, -1), 12),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 10)]))
    outer = Table([[t]], colWidths=[W]); outer.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    return outer

s = [Paragraph("지문 유형 2: 문자·채팅 5세트 (11/27)", st("K", 15, 21)),
     Paragraph("기출 구조(의도 파악·다음 할 일·사람 정체·숫자 세기)를 그대로 두고 내용은 새로 썼어. 정답은 Chat5_1127_key.pdf.", st("K", 9.2, 13.5, "#555555")), Spacer(1, 10)]
CI = {147: 0, 148: 0, 151: 0, 152: 0, 160: 0, 161: 2, 162: 3, 163: 0, 168: 0, 169: 2, 170: 3, 171: 1, 172: 3, 173: 1, 174: 2, 175: 0}
TG = {147: 2, 148: 1, 151: 3, 152: 0, 160: 1, 161: 2, 162: 3, 163: 0, 168: 2, 169: 0, 170: 3, 171: 1, 172: 3, 173: 1, 174: 2, 175: 0}
key = []
for i, S in enumerate(SETS):
    if i: s.append(PageBreak())
    a, b = S["rng"]
    s += [Paragraph(f"<b>Questions {a}-{b}</b> refer to the following {S['kind']}.", st("S", 10.3, 14, spaceAfter=8)), chat_box(S["lines"], S["kind"]), Spacer(1, 12)]
    cells = []
    for qi, (q, opts, why) in enumerate(S["qs"]):
        n = a + qi
        opts = list(opts); right = opts.pop(CI[n]); opts.insert(TG[n], right)
        cells.append([Paragraph(f"<b>{n}.</b> {q}", Q)] + [Paragraph(f"({l}) {o}", O) for l, o in zip("ABCD", opts)] + [Spacer(1, 9)])
        key.append((n, "ABCD"[TG[n]], right, why))
    half = (len(cells) + 1) // 2
    g = Table([[[x for c in cells[:half] for x in c], [x for c in cells[half:] for x in c]]], colWidths=[W / 2, W / 2])
    g.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 10)]))
    s.append(g)

SimpleDocTemplate(str(ROOT / "data/workbook/Chat5_1127.pdf"), pagesize=A4, leftMargin=36, rightMargin=36, topMargin=34, bottomMargin=34, title="문자·채팅 5세트").build(s)
METHOD = ["<b>추천 대응법 (문자·채팅)</b>",
          "① 읽기 전: 이름만 훑어서 몇 명인지 → 첫 등장 옆에 역할 한 단어 (Rosa-팀장? / Tom-시설 / Anita-연락)",
          "② 의도 문제(At 10:07, what does ~ mean): 그 줄에 표시 → <b>바로 앞 사람 말</b>에 화살표. 답은 대부분 '앞 말에 대한 반응'",
          "③ 계획이 바뀌면(Wait— / Actually / instead) 바뀌기 전 → 후를 여백에 화살표로",
          "④ 마지막 2~3줄 = 누가 뭘 하기로 했나 (I'll ~ / Will do / can you ~?) → 사람별로 이니셜 + 할 일",
          "⑤ 함정: 다른 사람이 할 일(사람 바꿔치기), 지문 단어(Dalton·flying·camera) 재사용, 숫자 세기(video 참석자 빼기)"]
k = [Paragraph("문자·채팅 5세트 정답 · 근거", st("K", 15, 21)), Spacer(1, 6)] + [Paragraph(x, st("K", 9.6, 14.5)) for x in METHOD] + [Spacer(1, 10)]
for n, a, o, w in key:
    k += [Paragraph(f"<b>{n}. ({a}) {o}</b>", st("K", 10, 14)), Paragraph(w, st("K", 9.2, 13.5, "#444444")), Spacer(1, 5)]
SimpleDocTemplate(str(ROOT / "data/workbook/Chat5_1127_key.pdf"), pagesize=A4, leftMargin=36, rightMargin=36, topMargin=34, bottomMargin=34).build(k)
print("ok", " ".join(f"{n}{a}" for n, a, o, w in key))
