# TEST 30 — same passages as TEST 29, every option rewritten after 동하 solved two items "in 30 seconds by sight".
# Self-critique of TEST 29: correct options copied the text (overlap 67% vs real 55%), and wrong options were
# unrelated inventions ("order more building materials") that fall away on first read.
# Rule here, taken from real 168-171 ("He asked Ms. Galloway to return a call he had made" = same people, same call,
# reversed direction): every wrong option is a NEAR MISS built from the passage's own people, dates, places and
# conditions with one relation changed (date swapped, person swapped, condition swapped, direction reversed,
# partial → total). Correct options paraphrase moderately; several need two sentences joined.
import copy, t29_items
DIVIDER_NOTE = "Part 7 단일지문 (147-175) — 근접 오답 기준 재작성. 새로 작성한 연습 문제입니다."
PARTIAL = True
NATURAL_KEY = True
PART5 = []
PART6 = []
Q = {
 0: [("What is the purpose of the notice?",
      ["To tell residents to move their bicycles", "To announce that the parking garage will close on April 8",
       "To explain how to get access to a recently built room", "To warn residents that unclaimed bicycles will be donated"],
      "목적: 차고 거치대 철거 + 1층 새 보관실로 이동. (B) 차고 폐쇄가 아니라 '거치대' 철거, (C) 키 카드는 '기존 정문 카드 그대로', (D) 남은 자전거는 관리사무소 보관(기부 아님) → 전부 근접 오답."),
     ("What are residents asked to do?",
      ["Label their bicycles with their unit numbers", "Move their bicycles by April 8",
       "Request a new pass from the building staff", "Leave their bicycles at the management office"],
      "세부: label your bicycle with your unit number. (B) 마감은 4월 7일, 8일은 철거일 → 날짜 바꿔치기. (D) 관리사무소는 '안 옮긴 자전거'가 가는 곳.")],
 1: [("What is suggested about the inspector?",
      ["He will arrive later than expected.", "He wants to check the upper level first.",
       "He called Mr. Ruiz to report a delay.", "He plans to meet Ms. Whitfield after five o'clock."],
      "추론: running about an hour behind. (B) 위층이 아니라 지하 배전반 먼저, (C) 전화 받은 사람은 Whitfield → 사람 바꿔치기, (D) 5시는 Whitfield의 회의 종료 시각."),
     ("At 3:16 P.M., what does Mr. Ruiz most likely mean when he writes, \"I'll take care of it\"?",
      ["He will unlock the basement.", "He will give the inspector a tour of the site.",
       "He will ask the workers to finish early.", "He will tell Ms. Whitfield when the inspector arrives."],
      "의도: 바로 앞 '지하실 열어 둬' → 검사관이 들어갈 수 있게 하겠다.")],
 2: [("What is indicated about the discount?",
      ["It lasts for about two weeks.", "It covers every item in the store.",
       "It requires a purchase of at least $75.", "It is offered every Saturday morning."],
      "사실 확인: April 1 to April 14 = 2주. (B) 도구·가구는 제외, (C) $75는 배송 조건, (D) 토요일 오전은 토양 검사 → 조건 바꿔치기."),
     ("What is mentioned about the workshop?",
      ["Participants must register in advance.", "It includes a free soil test.",
       "It takes place on a Saturday morning.", "It teaches how to grow vegetables outside."],
      "세부: registration required → 사전 예약. (D) 실내 허브 재배(Growing Herbs Indoors) → 대상·장소 바꿔치기.")],
 3: [("What is Mr. Duarte asked to do?",
      ["Return a form to the library", "Bring bottled water to each meeting",
       "Send a list of the club's 40 members", "Confirm the meeting time by phone"],
      "세부: complete the attached form and return it to the front desk. (B) 물은 '허용'일 뿐 요청이 아님, (C) 40은 좌석 수."),
     ("What is suggested about the photography club?",
      ["It can use the room for free.", "It will meet twice a month at the library.",
       "It will be allowed to serve food at meetings.", "It has used the community room before."],
      "추론: nonprofit → at no cost. (B) 매달 둘째 목요일 한 번, (C) 음식 금지, (D) 'Before your first meeting' → 처음 사용.")],
 4: [("What is the article mainly about?",
      ["A bakery's sale to a longtime employee", "The closing of a shop after three decades",
       "A bakery opening a location for gluten-free products", "A celebration of a bakery founder's retirement"],
      "주제: 오랜 직원에게 매각. (B) 31년 영업 후 '매각'이지 폐업 아님, (C) 글루텐 프리는 메뉴 추가."),
     ("What is indicated about Ms. Lam?",
      ["She has held two jobs at the bakery.", "She has led the kitchen since the shop first opened.",
       "She will stop selling some popular products.", "She will close the bakery permanently in July."],
      "두 문장 연결: 고등학생 때 계산원 + 9년간 수석 제빵사 → 여러 직책. (B) 31년은 가게 역사, (C) 대표 메뉴는 유지, (D) 7월엔 1주 휴업."),
     ("The word \"pursue\" in paragraph 4, line {LINE:pursue}, is closest in meaning to",
      ["engage in", "chase", "request", "investigate"],
      "동의어: pursue his interest in woodworking = 몰두하다 → engage in.")],
 5: [("What is NOT mentioned as being offered at the fair?",
      ["Résumé writing help", "Feedback on résumés", "Advice about interviews", "A chance to meet employers"],
      "NOT: 이력서 '검토'는 있지만 '작성 도움'은 없음 → 가까운 오답이 오히려 정답이 되는 NOT 유형. 면접 워크숍, 120개 기업은 언급."),
     ("What will registered attendees receive?",
      ["A list of the employers taking part", "A printed copy of the event program",
       "A résumé review in Room 104", "A reserved seat at the interview workshop"],
      "세부: a list of participating employers. (C) 이력서 검토는 등록과 무관하게 모두에게 제공 → 대상 바꿔치기. (B) 프로그램 인쇄물은 언급 없음."),
     ("What is suggested about the Halvorsen Convention Center?",
      ["It is accessible by public transportation.", "Parking there costs nothing for those who sign up.",
       "It is open from 10 A.M. to 4 P.M. every day.", "It holds job fairs every week."],
      "추론: bus routes 14 and 22 → 차 없이도 감. (B) 주차는 $10, (C) 10~4시는 '행사' 시간이지 건물 운영 시간 아님.")],
 6: [("Why was the memo sent?",
      ["To explain how incoming shipments will be logged", "To describe mistakes made over the past few months",
       "To schedule training sessions for shift supervisors", "To announce that paper checklists will be used for a few more weeks"],
      "목적: 입고 기록을 스캐너로. (B) 오류는 '줄이려는' 이유, (C) 감독관은 이미 교육 완료, (D) 종이 대신 스캐너."),
     ("What is indicated about the shift supervisors?",
      ["They will show team members how to use the scanners.", "They will be trained during the first hour of each shift.",
       "They will handle all technical problems themselves.", "They requested that the scanners be purchased."],
      "추론: will show team members how to use them → 다른 직원 교육. (B) 첫 1시간은 '팀원' 교육 시간, 감독관은 이미 교육받음 → 사람 바꿔치기.")],
 7: [("What is the article mainly about?",
      ["A new space at a library", "A robotics program for local teenagers",
       "A grant awarded to local businesses", "Classes that will begin next month"],
      "주제: 메이커스페이스 개관. (B) 로봇 프로그램은 '아이디어의 계기', (D) 주말 수업은 마지막 문단의 계획."),
     ("How was the makerspace paid for?",
      ["Mostly through a grant", "Only through support from companies",
       "Through fees paid by robotics students", "By selling old periodicals"],
      "세부: funded largely by a grant ... with additional support from local businesses. (B) 기업은 '추가 지원'일 뿐 → 부분을 전체로."),
     ("What is indicated about the makerspace?",
      ["Teenagers suggested it.", "It took the place of a computer lab.",
       "Its supplies cost users nothing.", "It is open only on Tuesday and Thursday evenings."],
      "추론: the idea came from teenagers who attended a robotics program → 젊은 이용자 제안. (C) 재료는 원가, (D) 화·목 저녁은 오리엔테이션.")],
 8: [("What is the purpose of the e-mail?",
      ["To request some documents", "To explain the cause of a recent delay",
       "To request an extension from the tax authority", "To introduce a new staff member"],
      "목적: 2월 10일까지 서류 요청. (B) 환급 지연은 '작년', (C) 연장은 작년에 했던 일, (D) Morales는 '질문 도움' 담당."),
     ("What is NOT among the documents that Ms. Sato is asked to provide?",
      ["Records of employee salaries", "Statements summarizing the year's finances",
       "Receipts for large equipment purchases", "Documentation of payments to contractors"],
      "NOT: 재무제표·$2,500 초과 장비 영수증·외주 지급 기록은 요청. 직원 급여 기록은 없음."),
     ("What is suggested about Ms. Sato's company?",
      ["It worked with Weber &amp; Cole last year.", "It received its refund early last year.",
       "It employs Ms. Morales as an assistant.", "It must file its tax return by February 10."],
      "추론: again this year + Last year ... arrived late. (B) 작년엔 2개월 지연, (C) Morales는 Weber의 조수 → 소속 바꿔치기, (D) 2월 10일은 서류 기한, 신고 기한은 3월 15일.")],
 9: [("What problem are the writers discussing?",
      ["A reserved room is unavailable on March 12.", "The keynote speaker cannot attend on March 12.",
       "A payment has not arrived.", "Interest in the event has been low."],
      "주제: 볼룸 중복 예약. (B) 연사는 '12일만 가능' → 반대, (C) 12월에 보증금 송금, (D) 210명으로 오히려 많음."),
     ("What is suggested about the Lakeview Room?",
      ["It holds fewer people than have registered.", "It is available on March 19.",
       "It is larger than the main space.", "It has already been reserved by another group."],
      "연계: 180명 수용 ↔ 210명 등록. (B) 19일에 비는 건 '볼룸', (D) 중복 예약된 건 볼룸 → 장소 바꿔치기."),
     ("At 11:10 A.M., what does Ms. Park most likely mean when she writes, \"Then we'd lose our biggest draw\"?",
      ["Moving the conference would mean losing the keynote speaker.", "The ballroom is the venue's most popular space.",
       "Watching online would be less popular.", "Another company would book the ballroom on March 19."],
      "의도: 바로 앞 '연사는 12일만 가능' → 날짜를 옮기면 가장 큰 흥행 요소(연사)를 잃는다. (C)는 스트리밍 제안이 '나중에' 나옴."),
     ("What will Ms. Olsen most likely do next?",
      ["Contact the venue", "Contact the keynote speaker", "Reduce the rental fee", "Change the event date"],
      "세부: I'll ask the venue. (C) 대여료 인하는 '요청할' 내용이지 그녀가 하는 일 아님.")],
}
PART7 = []
for i, s in enumerate(t29_items.PART7):
    s = copy.deepcopy(s)
    fixed = [q[3] if len(q) == 4 else None for q in s["qs"]]
    new = list(Q[i])
    k = 0
    qs = []
    for f, old in zip(fixed, s["qs"]):
        if f is not None:
            qs.append(old)            # insertion items keep their fixed answer
        else:
            qs.append(new[k]); k += 1
    s["qs"] = qs
    PART7.append(s)
P5_GAPS = (12, 12, 15, 15, 24, 24)
