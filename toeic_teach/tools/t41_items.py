# TEST 41 — 11/15 정기시험 복원 문항(해커스 카페 공개 복원, 동하가 공유) 정리 + 알고리즘 해설.
# 복원본이라 실제 시험 문장과 다를 수 있음. 정답은 복원 해설과 튜터 풀이 기준.
DIVIDER_NOTE = "11/15 정기시험 복원 문항 (공개 복원 자료 기반, 실제 문장과 다를 수 있음)."
PARTIAL = True
FIRST_PRINTED = 19
NATURAL_KEY = True
P5_GROUPS = [(0, 4), (4, 8), (8, 12), (12, 15)]
P5_GAPS = (14, 14, 22, 22)
PART6 = []

PART5 = [
 ("The company rewarded ------- was involved in the successful marketing campaign with a special bonus.",
  ["who", "whoever", "everyone", "him"],
  "[문법: 대명사·관계사] 빈칸 뒤 was involved = 동사 → 빈칸은 rewarded의 목적어 + was의 주어를 동시에 하는 명사절 → whoever(누구든 ~한 사람). everyone·him은 뒤에 동사를 못 받고, who는 앞에 선행사가 필요. (복원본은 'involved in'만 있으나 해설 문장 기준 was involved)", 1),
 ("Applicants should submit all required documents to the hiring manager ------- attending the interview.",
  ["therefore", "before", "instead", "and"],
  "[전/접/부] 빈칸 뒤 attending(V-ing) → 전치사 + 동명사. 접속부사 therefore·instead 탈락, and는 앞 동사와 병렬이 안 됨(submit ↔ attending 형태 불일치) → before(~하기 전에).", 1),
 ("The new cabinets were delivered early to meet the deadline and ------- in perfectly with the modern kitchen design.",
  ["is fit", "fits", "to fit", "fit"],
  "[문법: 동사 병렬] and 앞 진짜 동사 were delivered(과거) → and 뒤도 과거 동사. fit의 과거형 = fit. fits는 현재·단수(주어 cabinets 복수), to fit은 to meet과 병렬처럼 보이지만 '마감을 맞추고 잘 맞도록'보다 '배달됐고 잘 맞았다'가 자연스러움. 동사 문제 순서: 수일치 → 태 → 시제.", 3),
 ("The finance department obtained ------- from the board before increasing the annual budget.",
  ["approve", "approval", "approved", "will approve"],
  "[문법: 품사] 빈칸 앞 타동사 obtained → 목적어 = 명사 approval. -al로 끝나도 명사(approval, proposal, arrival).", 1),
 ("The local bookstore is closing -------, and many customers are taking advantage of the final discounts.",
  ["prior to", "soon", "regarding", "although"],
  "[전/접/부] 빈칸 뒤가 콤마(아무것도 없음) → 전치사(prior to, regarding)·접속사(although) 탈락 → 부사 soon. 현재진행(is closing) + soon = 가까운 미래.", 1),
 ("The increase in housing prices is ------- to the growing demand for apartments in major cities.",
  ["linked", "explained", "considered", "motivated"],
  "[어휘: 형용사·분사] 빈칸 뒤 to → be linked to(~와 관련이 있다). explained·considered·motivated는 'to + 명사'와 이 뜻으로 안 붙음.", 0),
 ("The local museum ------- several educational workshops over the past few years.",
  ["was hosted", "are hosting", "has hosted", "to host"],
  "[문법: 동사] 수일치(museum 단수 → are 탈락) → 태(목적어 workshops 있음 → 수동 was hosted 탈락) → 시제(over the past few years → 현재완료) → has hosted.", 2),
 ("The employees completed the project on time, ------- they had faced several unexpected challenges.",
  ["whereas", "in spite of", "although", "if"],
  "[전/접/부] 빈칸 뒤 they had faced = 문장 → 접속사. in spite of(전치사) 탈락. 의미: 예상치 못한 어려움에도 제때 끝냄 = 양보 although. whereas는 대조(반면에), if는 조건.", 2),
 ("The marketing director ------- the offer to transfer to the overseas branch due to family responsibilities.",
  ["accepted", "declined", "implemented", "reimbursed"],
  "[어휘: 동사] 목적어 the offer + 이유 due to family responsibilities(가족 사정) → 거절했다 declined. 동사 + 목적어 짝: decline/accept an offer, implement a plan, reimburse 사람 for 비용.", 1),
 ("The employees agreed to extend the operating hours during the holiday season, though -------.",
  ["hesitantly", "previously", "instantly", "permanently"],
  "[어휘: 부사] though + 생략(they agreed) ___ → '마지못해 동의했지만'. though가 양보이므로 동의와 반대 느낌인 hesitantly. previously(이전에)·instantly(즉시)는 though와 안 어울림. previously = 이전에, 앞서 (동하가 뜻을 몰랐던 단어).", 0),
 ("The conference room is available all day ------- when it has been reserved for quarterly meetings.",
  ["because", "along", "due", "except"],
  "[전/접/부] 빈칸 뒤 when + 절 → except when(~할 때를 제외하고). 하루 종일 사용 가능 ↔ 예약된 때는 예외. because는 뒤 when과 연결 안 됨, along·due는 전치사·형용사.", 3),
 ("The supervisor will submit the final report ------- he collects all the necessary information from the team.",
  ["furthermore", "beside", "once", "given"],
  "[전/접/부] 빈칸 뒤 he collects = 문장 → 접속사 once(일단 ~하면, ~하자마자). furthermore는 접속부사, beside·given은 전치사(given that이어야 접속사). 시간절은 미래를 현재(collects)로.", 2),
 ("The company plans to expand the <u>range</u> of its service to include online consultations.<br/>The word \"range\" is closest in meaning to",
  ["price", "scope", "scale", "capacity"],
  "[동의어] range = 범위 → scope. 문장에 넣어 확인: expand the scope of its service. scale(규모)·capacity(수용력)는 '서비스 항목의 폭'이 아님.", 1),
 ("The manager <u>framed</u> the company's success through a message of teamwork.<br/>The word \"framed\" is closest in meaning to",
  ["determined", "presented", "adjusted", "made"],
  "[동의어] frame A as/through B = A를 B로 제시하다(설명하다) → presented. '틀을 만들다'로 직역하면 made에 끌림.", 1),
 ("The company <u>finalized</u> the purchase of new office equipment after reviewing several proposals.<br/>The word \"finalized\" is closest in meaning to",
  ["cancelled", "complete", "avoided", "terminated"],
  "[동의어] finalize = 마무리 짓다(= conclude, complete). finalize a contract = 계약을 체결하다. terminated(끝내다)는 '해지하다' 뉘앙스라 구매를 확정한 것과 반대.", 1),
]

PART7 = [
 {"intro": "survey", "start": 147,
  "passages": [{"kind": "notice_box", "title": "Westwood Art Gallery — Visitor Satisfaction Survey",
    "body": ["We appreciate your feedback. Please select one answer for each question.",
             "<b>Q1.</b> How many different exhibitions have you attended at our gallery over the past year?<br/>[ ] One &nbsp; [X] Two &nbsp; [ ] Three &nbsp; [ ] Four",
             "<b>Q2.</b> Which of the following proposed additions would you most like us to introduce next year?<br/>[X] Art classes for beginners &nbsp; [ ] Expanded exhibition space<br/>[ ] Extended evening hours &nbsp; [ ] Digital audio guides",
             "<b>Q3.</b> How did you gain admission to the gallery today?<br/>[X] A complimentary pass issued through an affiliated local arts association<br/>[ ] An annual membership pass &nbsp; [ ] A regularly priced ticket &nbsp; [ ] A guest invitation"]}],
  "qs": [
   ("What is suggested about Westwood Art Gallery?",
    ["It offers art classes for beginners.", "It has hosted at least four exhibitions.",
     "It recently expanded its exhibition space.", "It provides free admission to local residents."],
    "[불명확 → 선지 진위판단] A ✗: art classes는 next year에 도입할 '제안(proposed additions)' = 아직 없음 / C ✗: expanded space도 제안 항목 / D ✗: 무료 입장은 '제휴 지역 예술 협회(affiliated association)'를 통한 것이지 '지역 주민' 전체가 아님(명사의 범위 바꿔치기) / B ✓: 지난 1년 관람 전시 수 보기가 Four까지 있음 → 최소 4개 전시를 열었다. ※ 복원 자료 기준 튜터 판단, 실제 정답과 다를 수 있음.", 1),
  ]},
]
