# Original practice test written in the page format of a Korean TOEIC past-test book (RC, one test = 28 pages).
# All sentences, passages, and questions are newly written for personal study. Not ETS material.
# Question tuple: (stem, [correct, wrong, wrong, wrong], note) -> builder places the answer.
#                 (stem, [A, B, C, D], note, fixed_index) -> printed order kept.
# Passage text: {131} = Part 6 blank. [[word]] = target word of a synonym question (printed plain).

PART5 = [
 ("The museum's sculpture garden will remain open ------- the renovation of the main gallery.",
  ["during", "among", "between", "onto"], "전치사: the renovation(명사구) 기간 동안 → during."),
 ("Harlow Bakery's ------- lemon tarts have won several regional awards.",
  ["popular", "popularity", "popularize", "popularly"], "품사: 소유격 + ___ + 명사 → 형용사."),
 ("Customers can track the ------- of their orders through the Bexley Home mobile app.",
  ["status", "figure", "rank", "level"], "어휘: track the status of orders = 주문 상태를 추적하다."),
 ("Ms. Navarro asked the interns to submit ------- weekly reports by Thursday afternoon.",
  ["their", "them", "they", "themselves"], "대명사: 명사(reports) 앞 = 소유격."),
 ("To reduce the ------- of errors, all invoices are reviewed by two accountants.",
  ["likelihood", "appearance", "attention", "admission"], "어휘: reduce the likelihood of errors = 오류 가능성을 줄이다."),
 ("The marketing director ------- reviewed every slide before the client presentation.",
  ["thoroughly", "thorough", "thoroughness", "more thorough"], "품사: 주어와 동사 사이 = 부사."),
 ("Please keep your receipt ------- you need to return or exchange the item.",
  ["in case", "so that", "as if", "whereas"], "접속사: ~할 경우에 대비해 = in case."),
 ("The city council approved the ------- of a new bicycle lane on Elm Avenue.",
  ["construction", "construct", "constructive", "constructed"], "품사: the ___ of = 명사."),
 ("Gresham Logistics currently ------- more than 400 trucks across the country.",
  ["operates", "operate", "operating", "to operate"], "수일치·시제: 단수 주어 + currently → 현재형 3인칭 단수."),
 ("Ms. Reyes gave a brief ------- of the new expense policy at the staff meeting.",
  ["explanation", "explain", "explanatory", "explained"], "품사: a + 형용사(brief) + ___ = 명사."),
 ("Ms. Castillo's team completed the audit ------- ahead of schedule.",
  ["well", "very", "so", "more"], "어휘: well ahead of schedule = 예정보다 훨씬 앞서."),
 ("The updated design makes the device ------- lighter than the previous model.",
  ["considerably", "considerable", "consideration", "considerate"], "품사: 비교급(lighter) 강조 = 부사."),
 ("Employees who wish to work remotely must obtain ------- from their department manager.",
  ["permission", "admission", "submission", "commission"], "어휘: obtain permission = 허가를 받다."),
 ("Patrons are ------- reminded that food and drinks are not allowed in the reading room.",
  ["kindly", "gladly", "eagerly", "highly"], "어휘: be kindly reminded = 정중히 알려드립니다."),
 ("The new ventilation system is designed to ------- energy costs by up to 20 percent.",
  ["lower", "decline", "fall", "sink"], "어휘: 목적어(energy costs)가 있음 → 타동사 lower. 나머지는 자동사."),
 ("Kemper Industries hopes to improve the ------- of its customer service representatives.",
  ["efficiency", "efficient", "efficiently", "more efficient"], "품사: the ___ of = 명사."),
 ("Mr. Han received a promotion ------- recognition of his work on the merger.",
  ["in", "at", "by", "on"], "전치사: in recognition of = ~을 인정하여."),
 ("Please arrive fifteen minutes early ------- the session can begin on time.",
  ["so that", "even if", "as though", "until"], "접속사: 목적 '~하도록' = so that."),
 ("The guidebook offers tips on how travelers can ------- to local customs.",
  ["adapt", "adopt", "admit", "adore"], "어휘: adapt to = ~에 적응하다. adopt는 '채택하다'(타동사)."),
 ("Ms. Kim prefers to review the contracts ------- rather than rely on summaries.",
  ["herself", "her", "hers", "she"], "대명사: 직접, 스스로 = 재귀대명사(강조)."),
 ("------- its small size, the new laptop has a remarkably long battery life.",
  ["Despite", "Although", "However", "Whereas"], "전치사: 뒤가 명사구(its small size) + 양보 → despite."),
 ("Customers who wish to ------- a complaint should speak with the store manager.",
  ["file", "filing", "filed", "files"], "to + 동사원형. file a complaint = 불만을 제기하다."),
 ("Ms. Patel's ------- knowledge of tax law makes her a valuable consultant.",
  ["extensive", "exclusive", "expensive", "excessive"], "어휘: extensive knowledge = 폭넓은 지식."),
 ("The museum's new security ------- have been praised by visitors.",
  ["measures", "measure", "measuring", "measured"], "수일치: 동사 have → 복수 주어 measures."),
 ("The new assembly line has ------- increased the plant's output.",
  ["significantly", "mutually", "separately", "tentatively"], "어휘: significantly increased = 크게 늘렸다."),
 ("For your -------, a map of the conference center is included in your welcome packet.",
  ["convenience", "convenient", "conveniently", "convene"], "품사: 소유격(your) 뒤 = 명사. for your convenience."),
 ("The success of the product launch was largely due to the marketing team's careful -------.",
  ["planning", "deadline", "decline", "departure"], "어휘: careful planning = 신중한 계획."),
 ("------- its regular menu, the café offers seasonal specials every month.",
  ["In addition to", "In spite of", "Instead", "Even though"], "어구: 정규 메뉴에 더해 = in addition to + 명사."),
 ("The ------- deadline for submitting proposals is May 31.",
  ["final", "eventual", "completed", "extreme"], "어휘: final deadline = 최종 마감."),
 ("The ------- results of the survey will be shared at Monday's meeting.",
  ["detailed", "detailing", "detail", "details"], "분사: 결과는 '상세하게 정리된' 쪽 = 과거분사 detailed."),
]

PART6 = [
 {"intro": "flyer", "title": "Clearwater Pet Grooming",
  "body": ["Bring your pet to Clearwater Pet Grooming! Our experienced groomers treat every animal with patience and care. "
           "{131} We offer bathing, haircuts, and nail trimming for dogs and cats of all sizes. Our {132} salon on Harbor "
           "Street was recently renovated and now has a separate waiting area for cats. Appointments can {133} be booked "
           "online in just a few minutes. With more than 15 years in business, our team knows how to keep {134} pets looking "
           "and feeling their best."],
  "qs": [
   ("", ["Your pet's comfort is always our first priority.", "Our prices have increased this month.",
         "Dogs must be kept on a leash in the park.", "We are hiring part-time cashiers."],
    "문장 삽입: 앞 문장(인내와 정성으로 돌봄)과 같은 흐름 → 반려동물의 편안함이 최우선."),
   ("", ["spacious", "spacing", "space", "spaciously"], "품사: 소유격 + ___ + 명사(salon) = 형용사."),
   ("", ["easily", "hardly", "rarely", "closely"], "어휘: 몇 분 만에 온라인 예약 → easily."),
   ("", ["your", "its", "their", "our"], "대명사: 광고가 고객에게 말하는 글 → your pets."),
  ]},
 {"intro": "letter",
  "body": ["12 March", "Mr. Daniel Okonkwo<br/>45 Willow Lane<br/>Fenwick, OH 43160", "Dear Mr. Okonkwo,",
           "On behalf of the board of directors of Fenwick Community Theater, I would like to thank you for your generous "
           "donation. {135} Your gift will allow us to replace the stage lighting system, which {136} since the theater "
           "opened in 1998.",
           "As a token of our appreciation, you will receive two season passes for our upcoming productions. They will be "
           "mailed to you {137} the end of this month.",
           "Your support helps us bring {138} performances to our community. Thank you once again.",
           "Sincerely,", "Rosa Delgado, Executive Director<br/>Fenwick Community Theater"],
  "qs": [
   ("", ["We are truly grateful for your continued support.", "Please renew your membership by Friday.",
         "Our next production has been canceled.", "The theater will be closed for the summer."],
    "문장 삽입: 기부 감사 직후 → 감사 표현이 이어짐."),
   ("", ["has been in use", "will be in use", "is using", "uses"], "시제: since + 과거 시점 → 현재완료. 조명은 사용되는 것."),
   ("", ["by", "until", "since", "among"], "전치사: 발송은 한 번에 끝나는 일 → 마감 by. until은 계속."),
   ("", ["memorable", "memorized", "memorizing", "memory"], "어휘·품사: 명사(performances) 앞 형용사, 기억에 남는 공연."),
  ]},
 {"intro": "e-mail",
  "hdr": [("To", "All Staff"), ("From", "Daniel Osei, Facilities Manager"), ("Date", "14 November"),
          ("Subject", "Elevator maintenance")],
  "body": ["Dear Colleagues,",
           "Please note that the east elevator will be out of service on Saturday, 18 November, while technicians {139} its "
           "annual inspection. The west elevator will remain {140} throughout the day. {141} Employees who need assistance "
           "moving heavy equipment should contact the facilities office in advance.",
           "We {142} for any inconvenience this may cause.", "Daniel Osei"],
  "qs": [
   ("", ["conduct", "conducting", "conducted", "will have conducted"], "시제: while(시간절) 안에서는 미래도 현재형."),
   ("", ["available", "availability", "avail", "availably"], "품사: remain + 형용사."),
   ("", ["The inspection is expected to take about six hours.", "The new cafeteria menu will be posted on Monday.",
         "Please submit your timesheets by Friday.", "The parking garage has been repaved."],
    "문장 삽입: 점검 안내 흐름 → 점검 소요 시간."),
   ("", ["apologize", "apology", "apologizing", "apologetic"], "품사: 주어 We 뒤 동사."),
  ]},
 {"intro": "article", "title": "Northgate Library Launches Tool-Lending Program",
  "body": ["NORTHGATE (3 March)—Northgate Public Library has begun lending household tools to residents with a valid "
           "library card. The collection {143} drills, ladders, and garden equipment. Items may be borrowed for up to one "
           "week. {144}, borrowers can renew an item once if no one else has reserved it. {145}",
           "\"Many residents need a tool only once or twice a year,\" said head librarian Marta Silva. \"This program saves "
           "them money and storage space.\" The library plans to {146} the collection based on community feedback."],
  "qs": [
   ("", ["includes", "including", "inclusion", "inclusive"], "문장에 동사가 없음 → 단수 주어 + includes."),
   ("", ["In addition", "Instead", "As a result", "For example"], "접속부사: 대여 규정에 규정을 하나 더 → 첨가."),
   ("", ["Late returns will result in a small daily fee.", "The library was built in 1965.",
         "Ms. Silva will retire next year.", "Several local bookstores have closed."],
    "문장 삽입: 대여 기간·연장 규정 뒤 → 연체료 규정."),
   ("", ["expand", "expansion", "expansive", "expanding"], "plan to + 동사원형."),
  ]},
]

# Part 7. Each set: intro line, list of passages, questions, page layout.
PART7 = [
 {"intro": "notice",
  "passages": [{"kind": "letter_plain",
    "body": ["Dear Maple Grove Condominium Residents,",
             "Crestline Window Services will clean the exterior windows of all units on Tuesday, April 9, and Wednesday, April 10, "
             "between 9 A.M. and 4 P.M. Workers will use a platform lowered from the roof, so please keep your balcony doors and "
             "windows closed during these hours. Balcony furniture should be moved at least one meter away from the railing by "
             "8 A.M. on April 9. If you have plants hanging over the railing, please bring them indoors. Residents who have "
             "questions may contact the management office at 555-0137.",
             "Thank you for your cooperation,<br/>Gregory Lin, Building Manager"]}],
  "qs": [
   ("What is the purpose of the notice?",
    ["To announce a maintenance service", "To introduce a new building manager", "To report damage to some balconies",
     "To announce a change in office hours"], "창문 외부 청소 일정 안내."),
   ("What are residents asked to do?",
    ["Move items away from the railing", "Clean their own windows", "Leave their windows open", "Visit the management office"],
    "\"Balcony furniture should be moved at least one meter away from the railing\""),
  ]},
 {"intro": "text-message chain",
  "passages": [{"kind": "phone", "msgs": [
    ("Priya Raman", "2:05 P.M.", "Hi Luis, are you still at the print shop?"),
    ("Luis Ortega", "2:07 P.M.", "Yes, I'm picking up the banners for Saturday's charity run."),
    ("Priya Raman", "2:08 P.M.", "Great. Could you also ask if they can print 300 maps of the race route? The ones we ordered from the other shop haven't arrived."),
    ("Luis Ortega", "2:12 P.M.", "I just asked. They can have them ready by Friday at noon."),
    ("Priya Raman", "2:13 P.M.", "That works. The volunteers aren't meeting until Friday evening.")]}],
  "qs": [
   ("What most likely is Mr. Ortega doing?",
    ["Collecting materials for an event", "Running in a race", "Designing a map", "Delivering banners to volunteers"],
    "인쇄소에서 자선 달리기용 현수막 수령."),
   ("At 2:13 P.M., what does Ms. Raman mean when she writes, \"That works\"?",
    ["The maps will be ready in time.", "She will meet the volunteers on Friday at noon.",
     "She approves a new race route.", "The other shop has sent the maps."],
    "금요일 정오 완성 < 자원봉사자 모임 금요일 저녁 → 시간 안에 준비됨."),
  ]},
 {"intro": "e-mail",
  "passages": [{"kind": "email_title",
    "hdr": [("To:", "All Branch Staff"), ("From:", "Helen Achebe"), ("Date:", "3 February"), ("Subject:", "Announcements")],
    "body": ["Dear Team,",
             "I am pleased to report that our Riverside branch exceeded its sales target for the fourth quarter. Thank you all for "
             "your hard work.",
             "I would also like to let you know that Tomás Reyes, our assistant manager, has accepted a position at our Northfield "
             "branch and will begin there on 1 March. Please join me in thanking Tomás for his contributions over the past six years.",
             "To help with the transition, Tomás will train his replacement, Grace Mwangi, during the last two weeks of February. "
             "If you have questions about ongoing projects, please direct them to Grace starting 15 February.",
             "Best regards,<br/>Helen Achebe, Branch Manager"]}],
  "qs": [
   ("What is mentioned about Mr. Reyes?",
    ["He will work at a different branch.", "He exceeded his personal sales target.", "He will retire in March.",
     "He was recently hired."], "Northfield 지점으로 이동."),
   ("What are staff asked to do starting February 15?",
    ["Send their questions to Ms. Mwangi", "Attend a training session", "Submit sales reports", "Contact the Northfield branch"],
    "\"direct them to Grace starting 15 February\". 교육은 Tomás가 Grace에게 하는 것(대상 함정)."),
  ]},
 {"intro": "article",
  "passages": [{"kind": "article_narrow", "title": "Historic Mill Reopens as Market Hall",
    "body": ["CARVERTON (May 12)—The old Carverton textile mill, which has stood empty for nearly two decades, will reopen next "
             "month as an indoor market hall. The building was purchased last year by brothers Kenji and Daniel Mori, who also run "
             "the popular Mori Coffee Roasters on Main Street.",
             "\"We grew up walking past this building every day,\" said Kenji Mori. \"We always wanted to see it full of people "
             "again.\" The market hall will house 30 stalls selling local produce, crafts, and prepared food. A grand opening "
             "celebration is planned for June 14. For details, visit www.carvertonmarkethall.com."]}],
  "qs": [
   ("What is the article mainly about?",
    ["The reuse of an old building", "The opening of a coffee shop", "The history of the textile industry",
     "A local farming festival"], "비어 있던 공장 → 실내 시장으로 재개장."),
   ("Who is Daniel Mori?",
    ["Kenji Mori's business partner", "The mayor of Carverton", "A market stall owner", "The author of the article"],
    "형제가 함께 건물을 사고 커피 가게도 함께 운영 → 사업 파트너."),
  ]},
 {"intro": "e-mail",
  "passages": [{"kind": "email_title",
    "hdr": [("To:", "Martin Hughes <mhughes@quickpost.net>"), ("From:", "Ana Ferreira <aferreira@lumenaudio.com>"),
            ("Date:", "9 July"), ("Subject:", "Order LA-20578")],
    "body": ["Dear Mr. Hughes,",
             "Thank you for ordering the Lumen Studio 5 wireless headphones. Unfortunately, the color you selected, forest green, "
             "is temporarily out of stock. — [1] —. We expect a new shipment in about three weeks. If you would prefer not to wait, "
             "the same model is currently available in black and silver. — [2] —. Alternatively, you may choose the Lumen Studio 7, "
             "which offers a longer battery life and comes in forest green. It normally costs $40 more, but we would be happy to "
             "provide it at the price of your original order. — [3] —.",
             "Please reply to this e-mail within 72 hours to let us know your choice. — [4] —. If we do not hear from you, we will "
             "ship your original order once it is back in stock.",
             "Sincerely,<br/>Ana Ferreira<br/>Customer Care, Lumen Audio"]}],
  "qs": [
   ("Why did Ms. Ferreira write the e-mail?",
    ["To offer options for a delayed order", "To request a payment", "To introduce a new product line", "To confirm a shipment"],
    "품절 → 기다리기 / 다른 색 / Studio 7 선택지 제시."),
   ("What is indicated about the Lumen Studio 7?",
    ["It has a longer battery life than the Studio 5.", "It is available only in black.", "It is cheaper than the Studio 5.",
     "It will be released in three weeks."], "\"offers a longer battery life\". 원래는 $40 더 비쌈."),
   ("In which of the positions marked [1], [2], [3], and [4] does the following sentence best belong?<br/><br/>"
    "\"Both colors can be shipped to you immediately.\"",
    ["[1]", "[2]", "[3]", "[4]"], "Both colors = black and silver → 그 문장 바로 뒤 [2].", 1),
  ]},
 {"intro": "e-mail",
  "passages": [{"kind": "email_gray",
    "hdr": [("To:", "Rebecca Stone <rstone@inkmail.com>"), ("From:", "Hugo Lindqvist <guestrelations@hotelbelmar.se>"),
            ("Date:", "28 October"), ("Subject:", "Your reservation")],
    "body": ["Dear Ms. Stone,",
             "Thank you for choosing Hotel Belmar for your stay from 12 to 15 November. As requested, we have changed your room to "
             "one with a view of the harbor. Please note that the rate for this room is €20 higher per night.",
             "Check-in begins at 3 P.M. If you are arriving earlier, our front desk staff will be happy to store your luggage. "
             "Breakfast is served in the Terrace Restaurant from 6:30 to 10:30 A.M. and is included in your rate.",
             "If you need to make further changes, please contact us at least 48 hours before your arrival.",
             "Kind regards,<br/>Hugo Lindqvist, Guest Relations"]}],
  "qs": [
   ("What is one purpose of the e-mail?",
    ["To confirm a change to a booking", "To advertise a new restaurant", "To request an advance payment",
     "To cancel a reservation"], "요청대로 객실 변경 확인."),
   ("What is indicated about Ms. Stone's new room?",
    ["It costs more per night.", "It includes dinner.", "It is available from 6:30 A.M.", "It is on the top floor."],
    "\"€20 higher per night\""),
   ("What can guests who arrive early do?",
    ["Leave their bags at the front desk", "Check in at noon", "Eat breakfast at no extra charge", "Change their room"],
    "\"store your luggage\". 조식 포함은 일찍 오는 것과 무관."),
  ]},
 {"intro": "article",
  "passages": [{"kind": "article_two_col", "title": "Halden Foods Introduces Ready-to-Cook Meal Kits",
    "byline": "By Laura Brennan",
    "col1": ["OSLO (15 September)—Halden Foods, the grocery chain best known for its bakery products, will soon offer "
             "something new: ready-to-cook meal kits. Each kit contains fresh, pre-measured ingredients and a recipe card for a "
             "dinner that can be prepared in about 30 minutes. \"Our customers told us they want healthy home-cooked meals but do "
             "not always have time to [[plan]] them,\" said Halden's product manager, Ingrid Solberg."],
    "col2": ["\"The kits take care of the planning and shopping.\"",
             "Halden will partner with farms in the region to supply vegetables and meat for the kits. \"Sourcing locally means "
             "our ingredients spend less time in transit, so they stay fresh longer,\" Ms. Solberg said. The kits will be sold in "
             "all 42 Halden stores beginning in October, and a vegetarian line will follow in the spring."]}],
  "qs": [
   ("What is one purpose of the article?",
    ["To announce a new product", "To report on a corporate merger", "To review a local restaurant",
     "To introduce a recently hired executive"], "새 밀키트 출시 소개."),
   ("The word \"plan\" in paragraph 1, line {LINE:plan}, is closest in meaning to",
    ["organize", "draw", "intend", "predict"], "plan meals = 식사를 계획·준비하다(organize). draw a plan(설계) 함정."),
   ("What does Ms. Solberg suggest about local sourcing?",
    ["It helps keep food fresh.", "It lowers prices.", "It supports local bakeries.", "It is required by law."],
    "\"spend less time in transit, so they stay fresh longer\""),
  ]},
 {"intro": "advertisement",
  "passages": [{"kind": "ad_box", "title": "Brightway Office Suites",
    "body": ["Are you tired of working from your kitchen table? Do you need a professional space to meet clients? Brightway Office "
             "Suites offers flexible workspaces for freelancers and small businesses in downtown Ashford.",
             "Brightway opened eight years ago with a single floor of shared desks. Today, our building on Carlton Street has four "
             "floors, including private offices, meeting rooms, and a rooftop lounge. Founder and owner Teresa Vance still greets "
             "many of our members personally."],
    "list_title": "Membership includes",
    "bullets": ["High-speed Internet and printing", "Access to the building from 6 A.M. to midnight",
                "Free use of meeting rooms for up to five hours per month", "Coffee and tea at no extra charge"],
    "after": ["Private offices require a minimum six-month agreement.",
              "To arrange a tour, contact our membership coordinator, Paolo Greco, at 555-0168. Members who sign up before "
              "June 30 will receive their first month free."]}],
  "qs": [
   ("According to the advertisement, who most likely is Ms. Vance?",
    ["A business owner", "A freelance designer", "A membership coordinator", "A real estate agent"],
    "Founder and owner. 회원 담당은 Mr. Greco(역할 함정)."),
   ("What is indicated about Brightway Office Suites?",
    ["It has grown since it opened.", "It is open 24 hours a day.", "It was founded by Mr. Greco.",
     "It is located outside the city."], "1개 층 → 4개 층."),
   ("What is included in a membership?",
    ["Some free use of meeting rooms", "Unlimited use of meeting rooms", "A private office", "Free parking"],
    "\"up to five hours per month\" → 일부 무료. 무제한 아님."),
   ("What will happen on June 30?",
    ["A special offer will end.", "The building will close.", "Membership prices will decrease.", "A rooftop lounge will open."],
    "6/30 전 가입 시 첫 달 무료 → 혜택 마감."),
  ]},
 {"intro": "article",
  "passages": [{"kind": "article_narrow",
    "body": ["BRAYFIELD (September 2)—Solano Textiles will move its headquarters from downtown Brayfield to a renovated "
             "warehouse in the city's Riverside district next spring. — [1] —. The company, which designs and manufactures "
             "upholstery fabrics, has outgrown its current offices on Grant Street, where it has been located since 2009.",
             "The new building will bring the company's design studio and its production facility under one roof for the first "
             "time. — [2] —. \"Right now, our designers have to drive 40 minutes to see their samples being made,\" said CEO "
             "Lorena Solano. \"Having everyone together will speed up our work.\"",
             "The renovation will include solar panels and a rooftop garden. — [3] —. Solano Textiles also plans to hire about 60 "
             "additional workers once the move is complete. Applications will be accepted through the company's Web site "
             "beginning in January. — [4] —."]}],
  "qs": [
   ("What is the article mainly about?",
    ["A company's relocation plans", "The launch of a new fabric", "A merger between two companies", "The opening of a store"],
    "본사 이전 계획."),
   ("What is indicated about Solano Textiles' production facility?",
    ["It is currently separate from the design studio.", "It is located on Grant Street.", "It will close next spring.",
     "It was built in 2009."], "처음으로 한 지붕 아래 + 디자이너가 40분 운전 → 지금은 떨어져 있음."),
   ("According to the article, what will happen in January?",
    ["The company will begin accepting job applications.", "The move will be completed.", "Solar panels will be installed.",
     "The CEO will visit the factory."], "\"Applications will be accepted ... beginning in January\""),
   ("In which of the positions marked [1], [2], [3], and [4] does the following sentence best belong?<br/><br/>"
    "\"The building was originally used to store grain.\"",
    ["[1]", "[2]", "[3]", "[4]"], "The building = 바로 앞의 renovated warehouse → [1].", 0),
  ]},
 {"intro": "online chat discussion",
  "passages": [{"kind": "chat", "msgs": [
    ("Hannah Cole", "9:02 A.M.", "Good morning. I'm checking on the brochures for the Kinsley Hotels account. Did the printer send the proofs yet?"),
    ("Marcus Webb", "9:03 A.M.", "They arrived last night. I noticed that the phone number on the back cover is wrong. It shows the old reservation line."),
    ("Hannah Cole", "9:04 A.M.", "That's a problem. The client needs 5,000 copies for the trade show on Thursday."),
    ("Marcus Webb", "9:05 A.M.", "I've added Ji-woo Park to the chat. She handled the client's last update."),
    ("Ji-woo Park", "9:06 A.M.", "Hi, everyone. The client sent us the new number two weeks ago. I'll forward that e-mail to the printer now."),
    ("Hannah Cole", "9:07 A.M.", "Thanks. Will the printer still be able to deliver on time?"),
    ("Ji-woo Park", "9:09 A.M.", "I called them yesterday about another job. They said they could turn around a corrected file within 24 hours."),
    ("Hannah Cole", "9:10 A.M.", "That's a relief.")]}],
  "qs": [
   ("Why did Ms. Cole start the online chat?",
    ["To check on the status of a print job", "To schedule a trade show", "To hire a new printer", "To contact a client"],
    "브로슈어 교정본 도착 여부 확인."),
   ("What problem does Mr. Webb mention?",
    ["Some contact information is incorrect.", "The brochures were damaged.", "The proofs arrived late.",
     "The client canceled an order."], "뒷표지 전화번호가 예전 번호."),
   ("What will Ms. Park do next?",
    ["Send an e-mail to the printer", "Call the client", "Attend a trade show", "Update a Web site"],
    "\"I'll forward that e-mail to the printer now\""),
   ("At 9:10 A.M., what does Ms. Cole most likely mean when she writes, \"That's a relief\"?",
    ["She believes the brochures will be ready on time.", "She is glad the client changed the order.",
     "She is pleased that a trade show was postponed.", "She thinks the error was the client's fault."],
    "24시간 내 수정 가능 → 목요일 전시회에 맞출 수 있음."),
  ], "left": 3},
 {"intro": "article and e-mail",
  "passages": [{"kind": "tips", "title": "Five Tips for Hosting a Successful Workshop",
    "body": ["Whether you are teaching pottery or personal finance, a well-planned workshop keeps participants engaged. Here are "
             "some suggestions.",
             "<b>1. Limit the size.</b> Groups of 12 to 15 allow every participant to ask questions.",
             "<b>2. Send materials in advance.</b> A short reading or checklist e-mailed a few days before the session helps "
             "participants arrive prepared.",
             "<b>3. Plan hands-on activities.</b> Participants remember more when they practice a skill rather than just listen.",
             "<b>4. Leave time for questions.</b> Reserve at least ten minutes at the end of each session.",
             "<b>5. Ask for feedback.</b> A brief survey at the end of the session will help you improve future workshops."]},
   {"kind": "email_gray",
    "hdr": [("To:", "Sofia Marquez <smarquez@budgetwise.com>"), ("From:", "Daniel Kerr <dkerr@ashtonlibrary.org>"),
            ("Date:", "March 3"), ("Subject:", "Budgeting workshop")],
    "body": ["Dear Ms. Marquez,",
             "Thank you for agreeing to lead the personal budgeting workshop at Ashton Public Library on March 20. As we discussed, "
             "registration will be capped at 15 people, and the session will run from 6:00 to 8:00 P.M. in Meeting Room B.",
             "I read the article on workshop planning that you recommended, and I agree that we should give participants something "
             "to review beforehand. If you send me your budgeting worksheet by March 15, I will e-mail it to everyone who has "
             "registered. I will also print the feedback survey you mentioned.",
             "Best regards,<br/>Daniel Kerr, Programs Coordinator"]}],
  "qs": [
   ("According to the article, why should workshop leaders limit group size?",
    ["So that all participants can ask questions", "To reduce the cost of materials", "To fit into small rooms",
     "To finish sessions early"], "Tip 1."),
   ("What does Mr. Kerr ask Ms. Marquez to do?",
    ["Send him a document by a certain date", "Print a feedback survey", "Register the participants", "Reserve a meeting room"],
    "워크시트를 3/15까지 보내기. 설문 인쇄는 Mr. Kerr가 함(역할 함정)."),
   ("Who most likely is Ms. Marquez?",
    ["A personal finance expert", "A librarian", "A pottery teacher", "A survey designer"], "예산 관리 워크숍 강사."),
   ("Which tip from the article is Mr. Kerr referring to when he mentions something to review beforehand?",
    ["Tip 2", "Tip 3", "Tip 4", "Tip 5"], "미리 자료 보내기 = Tip 2 (연계)."),
   ("According to the e-mail, when will the workshop take place?",
    ["On March 20", "On March 3", "On March 15", "On March 30"], "\"on March 20\""),
  ]},
 {"intro": "e-mail and press release",
  "passages": [{"kind": "email_title",
    "hdr": [("To:", "Teresa Wong <twong@harborviewba.org>"), ("From:", "Kofi Asante <kasante@bellmontcollege.edu>"),
            ("Date:", "April 8"), ("Subject:", "Construction notice")],
    "body": ["Dear Ms. Wong:",
             "I am writing to ask the Harborview Business Association to [[share]] some information with its members. As reported "
             "in last week's <i>Coastal Times</i>, Bellmont College will replace the water pipes beneath Front Street, which runs "
             "between our campus and the Harborview shopping district.",
             "The work is scheduled to begin on Monday, May 6, and will last approximately three weeks. During this period, Front "
             "Street will be closed to vehicles between Oak Avenue and Pier Road, although sidewalks will remain open. Crews will "
             "work from 7 A.M. to 4 P.M., Monday through Friday.",
             "We regret any inconvenience to local businesses and their customers. Please direct any questions to me at 555-0149.",
             "Kofi Asante<br/>Community Relations Office, Bellmont College"]},
   {"kind": "press",
    "body": ["<b>FOR IMMEDIATE RELEASE</b>", "<b>Contact:</b> Teresa Wong, twong@harborviewba.org",
             "HARBORVIEW (April 15)—The Harborview Business Association has moved its annual Spring Sidewalk Sale from May 11 to "
             "June 8. Shoppers can expect the same discounts from more than 50 participating stores, and the popular food court "
             "will again be set up in Pier Road Plaza.",
             "As in past years, Front Street will be closed to traffic for the event so that merchants can display goods outdoors. "
             "Live music will be provided by students from the Bellmont College music department."]}],
  "qs": [
   ("What is indicated about the pipe replacement project?",
    ["It will affect traffic on Front Street.", "It was paid for by local businesses.", "It will take place on weekends.",
     "It will close the sidewalks."], "차량 통행 금지, 인도는 개방."),
   ("In the e-mail, the word \"share\" in paragraph 1, line {LINE:share}, is closest in meaning to",
    ["pass along", "divide", "own", "split"], "share information = 정보를 전달하다. divide/split(나누다) 함정."),
   ("What can be concluded about the Harborview shopping district?",
    ["It is located near Bellmont College.", "It holds a music festival every May.", "It includes Pier Road Plaza only.",
     "It is home to the Coastal Times."], "Front Street가 캠퍼스와 상가 사이 → 가까움."),
   ("Why most likely did the Harborview Business Association change the date of its sale?",
    ["To avoid a construction period", "To attract more college students", "To add more participating stores",
     "To prevent a conflict with a concert"], "5/6부터 약 3주 공사 → 5/11은 공사 중 (연계)."),
   ("What is mentioned in the press release about Bellmont College students?",
    ["They will perform at the event.", "They will sell goods at the event.", "They will run the food court.",
     "They will help close the street."], "\"Live music will be provided by students\""),
  ]},
 {"intro": "advertisement, form, and review",
  "passages": [{"kind": "ad_plain", "title": "Greenleaf Lawn &amp; Garden: Serving the Tri-County Area Since 1995",
    "body": ["Greenleaf Lawn &amp; Garden provides landscaping and tree care for homes and businesses in Milford, Easton, and "
             "nearby towns. Our services range from weekly lawn mowing and seasonal planting to tree trimming and irrigation "
             "system repair.",
             "Every project is overseen by a certified arborist who visits the site, explains the work plan, and checks the "
             "results. To schedule a free consultation, visit www.greenleaflawn.com or call our office at 555-0115."]},
   {"kind": "form", "title": "Greenleaf Lawn &amp; Garden Service Request Form",
    "intro": "Tell us about your property, and one of our specialists will contact you promptly. All tree services include a free "
             "follow-up visit within 30 days.",
    "rows": [("Name", "Alan Pierce"), ("Date", "October 3"), ("E-mail", "apierce@mailbox.net"), ("Phone", "555-0172"),
             ("Address", "14 Linden Court<br/>Easton"),
             ("How may we help you?", "A large oak tree in my backyard has several broken branches after last week's storm, and "
              "some of them are hanging over my neighbor's fence. I would like someone to remove the damaged branches and check "
              "whether the tree is still healthy.")]},
   {"kind": "review", "site": "Neighborhood Reviews: Greenleaf Lawn &amp; Garden", "stars": 5,
    "quote": "\"Fast, careful, and friendly\"",
    "body": ["I submitted a request online, and the very next morning a specialist came to look at my oak tree. Two days later, a "
             "crew removed all of the broken branches. Mateo Ruiz, who had inspected the tree, stayed for the entire job and "
             "explained each step. What impressed me most was that the crew used a small crane so that no branches fell into my "
             "neighbor's yard. I will definitely use Greenleaf again.",
             "— Alan Pierce, Easton"]}],
  "qs": [
   ("According to the advertisement, what is one type of work performed by Greenleaf Lawn &amp; Garden?",
    ["Repairing irrigation systems", "Building fences", "Installing swimming pools", "Cleaning gutters"],
    "\"irrigation system repair\""),
   ("What does Mr. Pierce indicate on the form?",
    ["A storm damaged a tree.", "His fence needs to be replaced.", "He would like weekly lawn care.",
     "His neighbor recommended the company."], "지난주 폭풍으로 가지가 부러짐."),
   ("When did Greenleaf Lawn &amp; Garden most likely inspect Mr. Pierce's tree?",
    ["On October 4", "On October 3", "On October 6", "On October 30"], "10/3 신청 → 다음 날 아침 방문 (연계)."),
   ("Who most likely is Mr. Ruiz?",
    ["A certified arborist", "An office receptionist", "Mr. Pierce's neighbor", "A crane manufacturer"],
    "현장을 점검·설명 = 광고의 certified arborist 역할 (연계)."),
   ("According to the review, what impressed Mr. Pierce about the crew?",
    ["The equipment they used", "The price they charged", "The warranty they offered", "The speed of their payment process"],
    "크레인 사용 → 장비."),
  ]},
 {"intro": "Web page and e-mails",
  "passages": [{"kind": "web_table", "url": "https://www.westfieldcc.com/meeting-rooms",
    "title": "Westfield Convention Center — Meeting Rooms",
    "rows": [["Room", "Capacity", "Equipment", "Rate per hour"],
             ["Aster", "20", "TV screen", "$40"],
             ["Birch", "45", "Projector, microphone", "$75"],
             ["Cedar", "60", "Projector", "$90"],
             ["Dahlia", "120", "Projector, stage, microphone", "$150"]],
    "after": ["Catering from our in-house kitchen is available for groups of 25 or more. Rooms may be reserved in blocks of at least "
              "two hours."]},
   {"kind": "email_gray",
    "hdr": [("To:", "events@westfieldcc.com"), ("From:", "Nora Feld <nfeld@ridgewayins.com>"), ("Date:", "August 12"),
            ("Subject:", "Room reservation")],
    "body": ["Hello,",
             "I would like to reserve a meeting room for a training session on September 9 from 9 A.M. to 1 P.M. We expect about "
             "40 participants, and our trainer will need both a projector and a microphone. Could you also tell me whether lunch "
             "can be provided for the group?",
             "Thank you,<br/>Nora Feld, Ridgeway Insurance"]},
   {"kind": "email_gray",
    "hdr": [("To:", "Nora Feld <nfeld@ridgewayins.com>"), ("From:", "Ivan Petrov <events@westfieldcc.com>"), ("Date:", "August 13"),
            ("Subject:", "RE: Room reservation")],
    "body": ["Dear Ms. Feld,",
             "Thank you for your inquiry. Unfortunately, the room that best fits your needs is already booked on September 9. "
             "However, I can offer you our Dahlia Room for the same time at the rate of the room you would have chosen, since it is "
             "not being used that morning. Lunch can be arranged for your group, and I have attached our catering menu.",
             "Please confirm by August 20 so that I can hold the room for you.",
             "Best regards,<br/>Ivan Petrov, Event Services"]}],
  "qs": [
   ("Which room would Ms. Feld most likely have chosen?",
    ["Birch", "Aster", "Cedar", "Dahlia"], "40명 + 프로젝터 + 마이크 → Birch (연계)."),
   ("What does Ms. Feld ask about?",
    ["Meal service", "Parking for participants", "Hotel rooms nearby", "Discounts for nonprofits"], "점심 제공 여부."),
   ("What is indicated about the Dahlia Room?",
    ["It has a stage.", "It holds 60 people.", "It normally costs $75 per hour.", "It is booked on September 9."],
    "표: Projector, stage, microphone."),
   ("How much per hour will Ms. Feld most likely pay?",
    ["$75", "$150", "$90", "$40"], "원래 고를 방(Birch)의 요금 (연계)."),
   ("Why is Ms. Feld's group able to receive catering?",
    ["The group has more than 25 people.", "The booking was made before August 20.", "The session ends at 1 P.M.",
     "The room has a kitchen."], "케이터링은 25명 이상 → 40명 (연계)."),
  ]},
 {"intro": "e-mail, review, and notice",
  "passages": [{"kind": "email_gray",
    "hdr": [("To:", "Kitchen Staff"), ("From:", "Olivia Grant"), ("Date:", "October 2"), ("Subject:", "Autumn menu")],
    "body": ["Dear Team,",
             "Our autumn menu launches on October 15. Thank you to everyone who submitted recipes. The four dishes selected are:",
             "<b>Roasted squash soup</b>, created by Leo Banks<br/><b>Mushroom risotto</b>, created by Aisha Rahman<br/>"
             "<b>Braised short ribs</b>, created by Tom Fischer<br/><b>Apple-ginger tart</b>, created by our pastry chef, Mina Choi",
             "Please attend a tasting on October 10 at 3 P.M. so that the serving staff can learn to describe each dish to guests.",
             "Thanks,<br/>Olivia Grant<br/>General Manager, Bistro Lumière"]},
   {"kind": "review", "site": "https://www.valleyeats.com", "stars": 4, "title": "Bistro Lumière (Westbrook)",
    "body": ["My husband and I visited last Friday to try the new autumn menu. The risotto was the best I have ever had—rich and "
             "perfectly cooked. The soup was a little too salty for my taste. Our server, Daniel, described every dish in detail "
             "and recommended the dessert, which turned out to be wonderful. We will be back soon.",
             "—Carla Diaz, October 20"]},
   {"kind": "notice_box", "title": "Congratulations to Aisha Rahman!",
    "body": ["Bistro Lumière is proud to announce that the dish created by Aisha has been named one of the Top 10 Autumn Dishes by "
             "<i>Valley Dining Magazine</i>. Readers voted throughout October.",
             "Aisha joined our kitchen two years ago after completing her training at the Berwick Culinary Institute. Stop by this "
             "month and receive a free glass of apple cider with any order of her dish!"]}],
  "qs": [
   ("What is the purpose of the e-mail?",
    ["To share information about a menu", "To announce a staff promotion", "To request recipes from the staff",
     "To schedule a job interview"], "가을 메뉴 4가지와 시식회 안내."),
   ("According to the e-mail, what will happen on October 10?",
    ["Staff members will sample some dishes.", "The autumn menu will launch.", "A magazine will publish a review.",
     "A new chef will start work."], "시식회(tasting). 출시는 10/15."),
   ("What can be concluded about Ms. Diaz?",
    ["She visited after the new menu was launched.", "She ordered the braised short ribs.", "She complained to the server.",
     "She works as a chef."], "10/20 리뷰의 '지난 금요일' → 10/15 출시 이후 (연계)."),
   ("What is most likely true about the dish that Ms. Diaz liked best?",
    ["It was recognized by a magazine.", "It was created by the pastry chef.", "It was too salty.", "It is no longer served."],
    "가장 좋았던 risotto = Aisha 작품 = 잡지 Top 10 (삼중 연계)."),
   ("What is indicated about Ms. Rahman in the notice?",
    ["She received formal culinary training.", "She is the restaurant's pastry chef.", "She owns Bistro Lumière.",
     "She joined the restaurant last month."], "Berwick Culinary Institute에서 교육."),
  ]},
]
