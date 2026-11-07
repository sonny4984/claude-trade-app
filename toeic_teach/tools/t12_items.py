# Original practice TEST 12, written after studying ETS 기출 5 Tests 1-5 (patterns only; no item is copied or paraphrased).
# Quality rules applied (see data/analysis/ets5_notes.md):
#  P5  vocabulary items: four words of the same part of speech, decided by collocation/structure, not by spelling.
#      grammar items: preposition vs. conjunction pairs (during/while, despite/although, until/by) so structure decides.
#  P6  every set has a question that needs another sentence of the passage (tense, connector, reference);
#      insertion distractors are on-topic but contradict the passage or break the reference chain.
#  P7  correct answers are paraphrased; distractors reuse passage words (role swaps, date/number traps, "NOT").
# Tuple formats as in t11_items.py.

PART5 = [
 ("Ms. Okafor asked that all expense reports be sent directly to ------- by the end of the quarter.",
  ["her", "she", "hers", "herself"], "대명사 격: 전치사 to 뒤 → 목적격 her. herself는 주어=목적어일 때만."),
 ("Delmont Grocers will extend its opening hours ------- the holiday season.",
  ["during", "while", "when", "as soon as"], "전치사 vs 접속사: 뒤가 명사구(the holiday season) → 전치사 during. while/when/as soon as는 절(주어+동사)이 와야 함."),
 ("The new scheduling software is ------- to learn than the system we used last year.",
  ["easier", "easy", "easily", "easiest"], "비교급: than → easier."),
 ("Please review the attached contract ------- and return a signed copy to our office by Friday.",
  ["carefully", "careful", "care", "carefulness"], "품사: 완전한 문장(review the contract) 뒤 → 동사 수식 부사."),
 ("Applicants for the position must have at least three years of ------- experience in hotel management.",
  ["relevant", "relevance", "relevantly", "relevancy"], "품사: 전치사 of + ___ + 명사(experience) → 형용사."),
 ("Ferris Outdoor Gear will hold a ------- sale next week to make room for its spring inventory.",
  ["clearance", "clearly", "cleared", "clears"], "복합명사: clearance sale(재고 정리 세일). 명사+명사 조합은 통째로 외우기."),
 ("Smoking is ------- prohibited in all areas of the Westbury Hospital grounds.",
  ["strictly", "highly", "deeply", "closely"], "연어: strictly prohibited(엄격히 금지). highly는 recommended/qualified, closely는 monitor/work와 짝."),
 ("Our customer service representatives are trained to respond to complaints ------- and courteously.",
  ["promptly", "prompt", "prompted", "promptness"], "병렬: and courteously(부사)와 같은 형태 → promptly."),
 ("The shipment was delayed ------- a shortage of packaging materials at the warehouse.",
  ["because of", "because", "although", "so that"], "전치사 vs 접속사: 뒤가 명사구(a shortage) → because of."),
 ("Hillcrest Hotel ------- a free shuttle service to and from the airport every thirty minutes.",
  ["provides", "provide", "providing", "to provide"], "동사 자리 + 수일치: 주어 Hillcrest Hotel(단수), 동사가 없음 → provides."),
 ("The marketing team has ------- a detailed plan to increase sales in the northern region.",
  ["developed", "grown", "risen", "arrived"], "자동사/타동사: 목적어(a detailed plan)가 있으니 타동사 develop. rise/arrive는 목적어 불가."),
 ("Ms. Hahn gave an ------- presentation on the company's new safety procedures.",
  ["informative", "informed", "information", "inform"], "품사+의미: 명사(presentation) 앞 형용사. informative=유익한(정보를 주는), informed=정보를 잘 아는(사람)."),
 ("Ms. Rivera will lead the training session ------- Mr. Choi is attending the conference in Denver.",
  ["while", "during", "despite", "unless"], "전치사 vs 접속사: 뒤가 절(Mr. Choi is attending) → 접속사 while. during은 명사만."),
 ("Customers who wish to ------- their subscriptions before the renewal date may do so online.",
  ["cancel", "resign", "retire", "expire"], "타동사: 목적어(their subscriptions) → cancel. resign(사임)/retire(은퇴)/expire(만료)는 구독을 목적어로 못 받음."),
 ("------- the heavy rain, the outdoor concert at Lakeshore Park went ahead as planned.",
  ["Despite", "Although", "However", "Even"], "전치사 vs 접속사: 뒤가 명사구(the heavy rain) → Despite. Although는 절, However는 접속부사."),
 ("Mr. Abara received an award ------- his contributions to the community garden project.",
  ["in recognition of", "on behalf of", "in addition to", "in case of"], "구전치사 의미: 공로를 인정하여 → in recognition of. on behalf of=~을 대표하여."),
 ("The Riverside branch will remain closed ------- the water damage has been fully repaired.",
  ["until", "by", "during", "because of"], "until vs by: remain closed(상태 계속) + 절 → until. by는 전치사라 절 못 받고 '마감'의 뜻."),
 ("Bring a light jacket ------- the weather turns cold during the evening boat tour.",
  ["in case", "so that", "as if", "whereas"], "의미: ~할 경우에 대비해 → in case. so that은 목적(~하도록)."),
 ("Kenmore Bank ------- its online banking platform to make it easier for customers to transfer funds.",
  ["redesigned", "was redesigned", "redesigning", "to redesign"], "태: 목적어(its online banking platform)가 있으니 능동 → redesigned."),
 ("Ms. Lowe is accustomed to ------- with international clients over video calls.",
  ["working", "work", "worked", "works"], "be accustomed to + V-ing (to는 전치사). 동하 확정 오답 유형."),
 ("Because of the ------- of flight delays this weekend, passengers are advised to arrive at the airport early.",
  ["possibility", "permission", "position", "preference"], "어휘: 지연'가능성' 때문에 일찍 오라 → possibility."),
 ("New employees may need a few weeks to ------- to the fast pace of the production floor.",
  ["adjust", "adopt", "attach", "apply"], "어휘+전치사: adjust to(~에 적응하다). adopt는 '채택하다'(타동사, to 없음)."),
 ("The renovation of the main lobby was completed two weeks ------- than originally scheduled.",
  ["earlier", "early", "earliest", "more early"], "비교급: than → earlier."),
 ("To ------- the risk of injury, all warehouse staff must complete a safety course.",
  ["reduce", "decline", "fall", "rise"], "타동사: 목적어(the risk) → reduce. decline/fall/rise는 '줄다/늘다' 자동사."),
 ("The conference room on the third floor, ------- the quarterly meetings are usually held, is being repainted.",
  ["where", "which", "when", "what"], "관계부사: 뒤가 완전한 절(the meetings are held) + 장소 선행사 → where. which는 뒤가 불완전해야 함."),
 ("The new training program has already produced ------- results, including a 15 percent rise in sales.",
  ["tangible", "eventual", "reluctant", "absent"], "연어: tangible results(가시적 성과). 뒤에 구체적 수치가 근거."),
 ("Dr. Ellison's latest book has been ------- praised by critics for its clear explanations of economic theory.",
  ["widely", "deeply", "firmly", "closely"], "연어: widely praised / widely available(널리)."),
 ("The Harmon Street Bridge will reopen to traffic ------- the safety inspection is completed.",
  ["once", "by", "during", "upon"], "접속사: 뒤가 절 → once(~하자마자). upon/by/during은 전치사."),
 ("The survey results will be ------- to all department heads before Monday's meeting.",
  ["distributed", "attended", "participated", "arrived"], "수동태 가능한 타동사: distribute A to B → be distributed to. participate/arrive는 자동사라 수동 불가."),
 ("Visitors are asked to remain behind the yellow line ------- the train has come to a complete stop.",
  ["until", "by", "since", "unless"], "until vs by: remain(계속) ~할 때까지 → until. since는 '~이후로', unless는 '~하지 않으면'."),
]

PART6 = [
 {"intro": "e-mail",
  "hdr": [("To", "All Sales Staff"), ("From", "Grace Lim, Regional Manager"), ("Date", "3 October"),
          ("Subject", "Quarterly sales meeting")],
  "body": ["Dear Team,",
           "Our quarterly sales meeting {131} on Thursday, 12 October, at 9:00 A.M. This time, however, we will meet in the "
           "training room on the fourth floor instead of the main conference room, which is being renovated. {132}",
           "At the meeting, each team leader will present a summary of last quarter's results. {133}, we will review the new "
           "commission structure that takes effect in November.",
           "Lunch will be served afterward. If you have any dietary {134}, please let Kevin Moss know by Monday."],
  "qs": [
   ("", ["will be held", "was held", "has been held", "is holding"],
    "시제(문맥): 메일 날짜 10/3, 회의 10/12 → 미래 + 회의는 '열리는' 것이므로 수동 will be held."),
   ("", ["The room can seat up to forty people, so there will be enough space for everyone.",
         "The renovation of the conference room was completed last week.",
         "Please submit your September sales figures by Friday.",
         "The training room is reserved for new employees only."],
    "삽입: 바로 앞 = 장소 변경(training room). 그 방의 수용 인원 → 연결. B는 'is being renovated'와 모순, D도 모순."),
   ("", ["In addition", "Instead", "Otherwise", "For example"],
    "접속부사: 결과 발표 + 새 수수료 검토 → 추가 In addition. Instead는 앞 내용을 대체할 때."),
   ("", ["restrictions", "limits", "borders", "obstacles"], "연어: dietary restrictions(식이 제한)."),
  ]},
 {"intro": "notice", "title": "Notice to All Residents of Parkview Towers",
  "body": ["Beginning Monday, 6 May, the main entrance of Parkview Towers will be closed for about two weeks while workers "
           "install new automatic doors. During this period, residents should use the side entrance on Elm Street. {135}",
           "Please note that the side entrance is not wheelchair {136}. Residents who need step-free access may use the "
           "parking garage elevator, which {137} directly to the lobby.",
           "We apologize for any inconvenience. If you have questions, please contact the management office at 555-0143. "
           "Thank you for your {138}."],
  "qs": [
   ("", ["Signs will be posted to direct visitors there as well.", "The new doors were installed last year.",
         "Rent payments are due on the first of each month.", "The Elm Street entrance will also be closed at that time."],
    "삽입: 앞 = 옆문(Elm Street) 이용 안내 → 방문객도 거기로(there) 안내. B·D는 지문과 모순, C는 무관."),
   ("", ["accessible", "access", "accessing", "accessibly"], "품사: be동사(is not) + 보어 → 형용사. wheelchair accessible(휠체어 접근 가능)."),
   ("", ["leads", "lead", "leading", "have led"], "동사 자리 + 수일치: which = the elevator(단수) → leads. leading은 동사가 아님."),
   ("", ["patience", "patient", "patiently", "patients"], "품사: 소유격 your + 명사. patients(환자들)는 의미 함정."),
  ]},
 {"intro": "article", "title": "Brightwell Foods to Open Second Plant",
  "body": ["HARTFORD (14 June)—Brightwell Foods, a maker of frozen meals, announced on Tuesday that it will open a second "
           "production plant in nearby Millbrook. The new facility is expected to create about 200 jobs when it opens next spring.",
           "The company's first plant, located in Hartford, {139} at full capacity for the past three years. \"Demand for our "
           "products has grown {140} than we predicted,\" said CEO Laura Benning. \"A second plant will allow us to fill "
           "orders without delays.\"",
           "{141} Brightwell has also said that it will offer training programs for local residents with no manufacturing "
           "experience. Hiring for the new positions is expected to begin {142} the plant's opening."],
  "qs": [
   ("", ["has been operating", "will operate", "was operated", "to operate"],
    "시제: for the past three years(과거부터 지금까지) → 현재완료(진행) has been operating."),
   ("", ["faster", "fast", "fastest", "more fastly"], "비교급: than → faster."),
   ("", ["The company plans to fill most of the positions with people from the Millbrook area.",
         "The Hartford plant will close once the new one opens.",
         "Brightwell's meals are currently sold only in Hartford.",
         "Ms. Benning plans to retire next year."],
    "삽입: 뒤 문장의 also(또한 지역 주민 교육) → 앞에도 지역 채용 얘기가 있어야 함. B는 'second plant'와 모순."),
   ("", ["well before", "as soon as", "so that", "in order that"],
    "전치사 vs 접속사: 뒤가 명사구(the plant's opening) → 전치사 before. 나머지는 모두 절이 필요."),
  ]},
 {"intro": "advertisement", "title": "Fresh Start Cleaning Services",
  "body": ["Moving into a new home or office? Let Fresh Start Cleaning Services take care of the dirty work. Our {143} staff "
           "will clean every room from top to bottom, including the inside of cabinets, appliances, and windows.",
           "{144} we use only environmentally safe products, our services are suitable for homes with young children and pets. "
           "All of our cleaners are fully insured, and we guarantee your satisfaction. If you are not happy with the results, "
           "we will return within 48 hours and clean the area again {145} charge.",
           "{146} To schedule a free estimate, call 555-0198 or visit www.freshstartclean.com."],
  "qs": [
   ("", ["experienced", "experiencing", "experience", "experiences"],
    "분사: 직원이 '경험을 쌓은' 상태 → experienced staff. experiencing은 '겪고 있는'."),
   ("", ["Because", "Despite", "Although", "Therefore"],
    "접속사 의미: 친환경 제품을 쓰니까 → 아이·반려동물 집에 적합(원인-결과). Despite는 명사, Therefore는 접속부사."),
   ("", ["at no", "for no", "in no", "by no"], "숙어: at no charge(무료로) = free of charge."),
   ("", ["New customers receive 15 percent off their first cleaning.", "Our office will be closed for renovations next month.",
         "We are currently hiring experienced cleaners.", "Please return the completed form to the front desk."],
    "삽입: 광고 마지막 + 다음 문장이 '무료 견적 예약' → 고객 혜택 안내가 자연스러움. C는 구인(대상이 다름)."),
  ]},
]

PART7 = [
 # 147-148
 {"intro": "notice",
  "passages": [{"kind": "notice_box", "title": "Westbrook Community Pool: Summer Schedule Change",
    "body": ["Starting July 1, the Westbrook Community Pool will open at 6:00 A.M. on weekdays, one hour earlier than before, to "
             "accommodate residents who prefer to swim before work. Weekend hours (8:00 A.M. to 8:00 P.M.) will remain unchanged.",
             "Please note that the pool will be closed on Monday, July 15, for its annual water-quality inspection. Swimming lessons "
             "for children will continue to be held on Saturday mornings. Registration forms are available at the front desk."]}],
  "qs": [
   ("What is the purpose of the notice?",
    ["To announce an extended opening time", "To introduce a new swimming instructor",
     "To explain why the pool will close for the summer", "To request feedback on weekend hours"],
    "평일 개장을 한 시간 앞당김(open one hour earlier) → 운영 시간 연장."),
   ("What will happen on July 15?",
    ["The facility will be checked.", "Swimming lessons will begin.", "Weekend hours will change.",
     "Registration forms will be distributed."], "annual water-quality inspection → 시설 점검(checked). 패러프레이즈."),
  ]},
 # 149-151
 {"intro": "article",
  "passages": [{"kind": "article_narrow", "title": "Bakery Expands Delivery Area",
    "body": ["GLENDALE (March 4)—Sunrise Bakery, known for its sourdough bread and fruit pastries, will begin delivering to the "
             "neighboring towns of Oakridge and Millport next month. Until now, the bakery has delivered only within Glendale.",
             "Owner Hana Yoshida said the decision was driven by customer requests. \"Every week, people from Oakridge drive half an "
             "hour to buy our bread,\" she said. \"We wanted to make things easier for them.\" To handle the additional orders, the "
             "bakery has purchased two refrigerated vans and hired three drivers.",
             "Orders can be placed on the bakery's Web site until 8 P.M. for delivery the following morning. Deliveries outside "
             "Glendale will carry a $5 fee."]}],
  "qs": [
   ("What is the article mainly about?",
    ["A business offering a service in more locations", "The opening of a second bakery", "A change in a bakery's ownership",
     "The rising price of bread"], "배달 지역 확대 = 더 많은 곳에서 서비스. 2호점 개점(B)은 아님."),
   ("Why did Ms. Yoshida make the decision?",
    ["Customers asked for it.", "Sales in Glendale had decreased.", "A competitor had closed.", "Delivery costs had gone down."],
    "\"driven by customer requests\"."),
   ("What is indicated about deliveries to Oakridge?",
    ["They require an extra charge.", "They are made in the evening.", "They include only bread.", "They must be ordered by phone."],
    "Glendale 밖 배달은 $5 → 추가 요금. 8 P.M.은 주문 마감(배달은 다음 날 아침) → B 함정."),
  ]},
 # 152-153
 {"intro": "text-message chain",
  "passages": [{"kind": "phone", "msgs": [
    ("Daniel Kwon", "10:12 A.M.", "Hi Mina, the projector in Conference Room B won't turn on, and the client arrives at 11."),
    ("Mina Foster", "10:14 A.M.", "Did you check that it's plugged in? The cleaning crew sometimes unplugs it."),
    ("Daniel Kwon", "10:15 A.M.", "I did. The power light doesn't come on at all."),
    ("Mina Foster", "10:16 A.M.", "Then take the portable one from my office. It's in the cabinet behind my desk."),
    ("Daniel Kwon", "10:17 A.M.", "Thanks! I'll bring it back right after the meeting."),
    ("Mina Foster", "10:18 A.M.", "No rush. I won't need it until Thursday.")]}],
  "qs": [
   ("What problem does Mr. Kwon have?",
    ["Some equipment is not working.", "A client has canceled a meeting.", "A room has been double-booked.", "A cabinet is locked."],
    "프로젝터가 안 켜짐 → equipment not working."),
   ("At 10:18 A.M., what does Ms. Foster most likely mean when she writes, \"No rush\"?",
    ["Mr. Kwon can keep the projector for a while.", "The client will arrive late.",
     "The meeting does not need to start on time.", "She will repair the projector on Thursday."],
    "바로 뒤 '목요일까지 필요 없음' → 급하게 돌려줄 필요 없다."),
  ]},
 # 154-156
 {"intro": "e-mail",
  "passages": [{"kind": "email_gray",
    "hdr": [("To:", "Customer Service <service@ardenoffice.com>"), ("From:", "Paulo Mendes <pmendes@lindqvistdesign.com>"),
            ("Date:", "9 October"), ("Subject:", "Order #58213")],
    "body": ["To Whom It May Concern:",
             "On 2 October, I ordered six ergonomic desk chairs (model EC-40) for our design studio. — [1] —. The chairs arrived "
             "yesterday, and five of them are in excellent condition. — [2] —. However, one chair has a broken armrest, and the box "
             "it came in was badly damaged. — [3] —.",
             "I would prefer a replacement rather than a refund, since we need all six chairs for new staff members who start on "
             "16 October. — [4] —. Please let me know how you would like me to return the damaged chair.",
             "Sincerely,<br/>Paulo Mendes, Studio Manager, Lindqvist Design"]}],
  "qs": [
   ("Why did Mr. Mendes write the e-mail?",
    ["To report a problem with a delivery", "To order additional chairs", "To cancel an order", "To ask for a refund"],
    "의자 1개 파손 신고. 환불이 아니라 교환 원함(D 함정)."),
   ("What is suggested about Lindqvist Design?",
    ["It is hiring new employees.", "It recently moved to a new office.", "It designs office furniture.",
     "It has ordered from Arden Office before."], "new staff members who start on 16 October → 신규 직원 채용 중."),
   ("In which of the positions marked [1], [2], [3], and [4] does the following sentence best belong?<br/><br/>"
    "\"I have attached photographs of both the chair and the packaging.\"",
    ["[1]", "[2]", "[3]", "[4]"], "의자(armrest)와 상자(box) 파손 언급 직후 → [3]. both the chair and the packaging이 두 대상을 받음.", 2),
  ]},
 # 157-158
 {"intro": "advertisement",
  "passages": [{"kind": "ad_box", "title": "Corbin Language Institute",
    "body": ["Preparing for an overseas assignment? Need to communicate better with international clients? Corbin Language "
             "Institute can help. Our certified instructors teach Spanish, Mandarin, Japanese, and German to adults at every level."],
    "list_title": "Course Options",
    "bullets": ["Evening group classes (maximum eight students): Mondays and Wednesdays, 7:00–9:00 P.M.",
                "Private lessons: scheduled at your convenience",
                "Corporate packages: our instructors teach at your workplace"],
    "after": ["All new students take a free placement test to determine their level. Call 555-0172 to arrange your test before "
              "the next term begins on September 9."]}],
  "qs": [
   ("For whom is the advertisement most likely intended?",
    ["Professionals who work with people from other countries", "Students applying to universities",
     "Teachers looking for employment", "Travel agents planning tours"],
    "overseas assignment, international clients → 해외 업무 직장인."),
   ("What is offered free of charge?",
    ["An assessment of language ability", "A private lesson", "Course materials", "A trial group class"],
    "free placement test = 수준 평가(assessment). 패러프레이즈."),
  ]},
 # 159-161
 {"intro": "memo",
  "passages": [{"kind": "memo",
    "hdr": [("From:", "Victor Albrecht, Facilities Director"), ("To:", "All Staff, Kessler Building"), ("Date:", "April 22"),
            ("Subject:", "Parking garage repairs")],
    "body": ["Repairs to the lower level of the parking garage will begin on Monday, May 6, and are expected to take three weeks. "
             "During this period, the lower level will be closed, and about 60 parking spaces will be unavailable.",
             "To reduce congestion, we have arranged for employees to park at the Marlow Street lot, two blocks east of our "
             "building. A shuttle bus will run between the lot and our main entrance every fifteen minutes from 7:00 to 9:30 A.M. "
             "and from 4:30 to 7:00 P.M. Employees who [[regularly]] ride bicycles to work may continue to use the racks on the "
             "upper level, which will not be affected.",
             "If you hold a parking permit for the lower level, please bring it to the facilities office by May 1 to receive a "
             "temporary permit for the Marlow Street lot."]}],
  "qs": [
   ("What is the purpose of the memo?",
    ["To announce temporary changes to parking arrangements", "To introduce a new city bus route",
     "To explain new rules for bicycle storage", "To encourage employees to carpool"],
    "3주간 지하층 폐쇄 + 임시 주차장 안내."),
   ("What are some employees asked to do by May 1?",
    ["Exchange a permit", "Register their bicycles", "Move their cars to the upper level", "Sign up for the shuttle bus"],
    "기존 permit을 가져오면 임시 permit 발급 → 교환(exchange)."),
   ("The word \"regularly\" in paragraph 2, line {LINE:regularly}, is closest in meaning to",
    ["usually", "properly", "evenly", "officially"], "regularly ride = 평소에/습관적으로 타다 → usually."),
  ]},
 # 162-163
 {"intro": "schedule",
  "passages": [{"kind": "table_box", "title": "Harbor City Small Business Fair: Saturday, October 19",
    "intro": ["All sessions take place at the Harbor City Convention Center. Admission is free, but seating for workshops is limited."],
    "rows": [["Time", "Session", "Location"],
             ["9:30 A.M.", "Opening remarks by Mayor Lydia Chen", "Main Hall"],
             ["10:00 A.M.", "Building an Online Store on a Small Budget", "Room 101"],
             ["11:30 A.M.", "Hiring Your First Employee", "Room 103"],
             ["1:00 P.M.", "Networking Lunch (ticket required)", "Atrium"],
             ["2:30 P.M.", "Understanding Small-Business Loans", "Room 101"]],
    "widths": [0.2, 0.56, 0.24],
    "after": ["Exhibitor booths are open from 9:00 A.M. to 4:00 P.M. Lunch tickets ($15) must be purchased by October 12 at "
              "www.harborcitybizfair.org."]}],
  "qs": [
   ("What is indicated about the fair?",
    ["Some sessions have a limited number of seats.", "It takes place over two days.", "All sessions are held in the Main Hall.",
     "Admission must be paid in advance."], "seating for workshops is limited. 입장료는 무료(D 함정)."),
   ("What should attendees do by October 12 if they want to eat lunch at the fair?",
    ["Buy a ticket online", "Visit an exhibitor booth", "Contact the mayor's office", "Arrive before 9:00 A.M."],
    "점심 티켓은 10/12까지 웹사이트에서 구매."),
  ]},
 # 164-167
 {"intro": "press release",
  "passages": [{"kind": "press",
    "body": ["<b>FOR IMMEDIATE RELEASE</b>",
             "<b>Contact:</b> Irene Walsh, iwalsh@alderhome.ca",
             "TORONTO (5 September)—Alder Home Appliances today announced that Keiko Barros will become its vice president of "
             "product design, effective 1 October. — [1] —. Ms. Barros joins Alder from Venn Electronics, where she led the team "
             "that developed the company's best-selling line of energy-efficient refrigerators.",
             "\"Keiko has a rare ability to combine practical engineering with elegant design,\" said Alder president Samuel Ortiz. "
             "\"Her experience will be [[invaluable]] as we prepare to enter the kitchen appliance market.\" — [2] —.",
             "Ms. Barros holds a degree in industrial design from Northfield University and has received several awards for her "
             "work. — [3] —. She will be based at Alder's headquarters in Toronto but will travel regularly to the company's "
             "manufacturing plant in Hamilton.",
             "Alder Home Appliances, founded in 1987, currently produces washing machines, dryers, and air conditioners. — [4] —."]}],
  "qs": [
   ("What is the purpose of the press release?",
    ["To announce the appointment of an executive", "To introduce a new refrigerator", "To report a company merger",
     "To advertise a job opening"], "부사장 임명 발표."),
   ("What is indicated about Alder Home Appliances?",
    ["It plans to sell a new type of product.", "It recently moved its headquarters to Toronto.",
     "It will close its plant in Hamilton.", "It was founded by Mr. Ortiz."],
    "현재 세탁기·건조기·에어컨 + '주방 가전 시장 진출 준비' → 새 종류 제품 판매 계획."),
   ("The word \"invaluable\" in paragraph 2, line {LINE:invaluable}, is closest in meaning to",
    ["extremely useful", "worthless", "difficult to measure", "widely known"],
    "invaluable = 매우 귀중한(값을 매길 수 없을 만큼). in-이 붙었다고 '가치 없는'(worthless)이 아님 → 대표 함정."),
   ("In which of the positions marked [1], [2], [3], and [4] does the following sentence best belong?<br/><br/>"
    "\"Its products are sold in more than 20 countries.\"",
    ["[1]", "[2]", "[3]", "[4]"], "Its = 회사(Alder). 회사 소개(설립 연도·생산품) 바로 뒤 [4].", 3),
  ]},
 # 168-171
 {"intro": "e-mail",
  "passages": [{"kind": "email_title",
    "hdr": [("To:", "Rachel Duarte"), ("From:", "Owen Pritchard"), ("Date:", "14 February"),
            ("Subject:", "Welcome to Fairmont Consulting")],
    "body": ["Dear Ms. Duarte,",
             "Welcome to Fairmont Consulting! We are delighted that you will be joining our research department as a data analyst "
             "on Monday, 3 March.",
             "On your first day, please report to the reception desk on the fifth floor at 8:45 A.M. Lena Okoro from human resources "
             "will meet you there and give you a tour of the office. She will also help you set up your computer account and take "
             "your photo for your employee identification card.",
             "During your first two weeks, you will attend orientation sessions on our software and security procedures. You will "
             "also be paired with a senior analyst, Martin Heller, who can answer any questions about ongoing projects.",
             "Before your start date, please complete the tax and direct-deposit forms attached to this e-mail and return them to me. "
             "If you have any questions, feel free to call me at 555-0119.",
             "Best regards,<br/>Owen Pritchard, Human Resources Manager"]}],
  "qs": [
   ("What is the purpose of the e-mail?",
    ["To provide information to a new employee", "To schedule a job interview", "To announce a promotion",
     "To request feedback on an orientation"], "입사 첫날 안내."),
   ("Who is Ms. Okoro?",
    ["A human resources staff member", "A senior analyst", "A receptionist", "A security officer"],
    "Lena Okoro from human resources. reception desk는 만나는 장소(C 함정), senior analyst는 Heller(B 함정)."),
   ("What is NOT mentioned as something Ms. Duarte will do on her first day?",
    ["Attend a client meeting", "Take a tour of the office", "Have a photograph taken", "Set up a computer account"],
    "투어·사진·계정 설정은 첫날 언급됨. 고객 회의는 없음."),
   ("What is Ms. Duarte asked to do before March 3?",
    ["Return some completed forms", "Call Mr. Heller", "Visit the fifth floor", "Install some software"],
    "Before your start date → 서류 작성 후 회신."),
  ]},
 # 172-175
 {"intro": "online chat discussion",
  "passages": [{"kind": "chat", "msgs": [
    ("Sophie Grant", "9:02 A.M.", "Morning, everyone. Quick update on the Lakeview Hotel brochure: the client approved the layout but wants new photos of the pool area."),
    ("Ravi Desai", "9:03 A.M.", "The pool was being resurfaced when we did the photo shoot in May. Is it open again?"),
    ("Sophie Grant", "9:04 A.M.", "It reopened last week. The client would like the brochure printed by the 28th."),
    ("Tomás Rivera", "9:05 A.M.", "That's tight. Our photographer, Elena, is booked solid until the 20th."),
    ("Ravi Desai", "9:06 A.M.", "What about using the photos the hotel posted on its Web site?"),
    ("Sophie Grant", "9:07 A.M.", "I asked. They're too low in resolution for print."),
    ("Tomás Rivera", "9:09 A.M.", "Let me call Elena's assistant. He sometimes covers small jobs for her."),
    ("Sophie Grant", "9:10 A.M.", "Please do. If he can shoot on Monday, we'll still have a week for editing."),
    ("Tomás Rivera", "9:18 A.M.", "Good news. He's available Monday morning."),
    ("Sophie Grant", "9:19 A.M.", "Perfect. I'll let the client know.")]}],
  "qs": [
   ("What are the writers mainly discussing?",
    ["Updating a promotional publication", "Booking a hotel for a conference", "Hiring a new photographer",
     "Redesigning a Web site"], "호텔 브로슈어(홍보물) 사진 교체."),
   ("What is suggested about the pool at Lakeview Hotel?",
    ["It could not be used in May.", "It will be closed on Monday.", "It will appear on the cover of the brochure.",
     "It was recently enlarged."], "5월 촬영 때 resurfacing 중 → 사용 불가였음."),
   ("Why are the photos on the hotel's Web site unsuitable?",
    ["Their quality is too low for printing.", "They are protected by copyright.", "They show the wrong building.",
     "They are out of date."], "too low in resolution for print. '오래된 사진'(D)은 그럴듯한 함정 — 지문 근거 없음."),
   ("At 9:19 A.M., what does Ms. Grant most likely mean when she writes, \"Perfect\"?",
    ["The deadline can be met.", "She approves the final photos.", "She will meet the assistant on Monday.",
     "The client has paid for the brochure."],
    "월요일 촬영 → 편집 1주 → 28일 인쇄 가능. 일정 맞출 수 있다는 뜻."),
  ], "left": 2},
 # 176-180
 {"intro": "Web page and e-mail",
  "passages": [{"kind": "web_tabs", "url": "https://www.pinecrestlodge.com/meetings",
    "tabs": ["Home", "Rooms", "Meetings", "Contact"], "active": 2, "title": "Meeting and Event Spaces",
    "body": ["Pinecrest Lodge offers three meeting rooms, each with a view of Lake Arden. All rooms include wireless Internet "
             "access, a projector, and a whiteboard at no extra charge.",
             "• Birch Room: seats up to 20; $250 per day",
             "• Cedar Room: seats up to 45; $400 per day",
             "• Summit Hall: seats up to 120; $900 per day; includes a stage and sound system",
             "Groups that reserve ten or more guest rooms receive a 15 percent discount on meeting room fees. Meals are provided "
             "by our on-site restaurant, The Lakeside Grill. Menus are available on request."]},
   {"kind": "email_classic",
    "hdr": [("To:", "events@pinecrestlodge.com"), ("From:", "Nadia Kowalski &lt;nkowalski@brennerlabs.com&gt;"),
            ("Date:", "August 3"), ("Subject:", "Booking inquiry")],
    "body": ["Hello,",
             "I am organizing a two-day training workshop for Brenner Laboratories on September 18 and 19. We expect 35 "
             "participants. About a dozen of them will be traveling from our Chicago office and will need rooms at the lodge for "
             "two nights.",
             "We would also like lunch to be served in the meeting room on both days. Could you send me your menu options and "
             "confirm that a room of the [[appropriate]] size is available on those dates? Some of our trainers will show video "
             "clips, so we will need a projector, but I assume that will not be a problem.",
             "Thank you,<br/>Nadia Kowalski, Training Coordinator"]}],
  "qs": [
   ("What is indicated about the meeting rooms?",
    ["They all overlook a lake.", "They can be combined into one space.", "They were recently renovated.",
     "They must be reserved for at least two days."], "each with a view of Lake Arden → overlook a lake."),
   ("Which room will Ms. Kowalski most likely reserve?",
    ["The Cedar Room", "The Birch Room", "Summit Hall", "The Lakeside Grill"],
    "연계: 참가자 35명 → 45명 수용 Cedar Room. Birch(20)는 부족, Summit Hall(120)은 과함."),
   ("What is suggested about Brenner Laboratories?",
    ["It will qualify for a discount on the meeting room.", "It has an office near Lake Arden.",
     "It has held events at the lodge before.", "It needs a stage for a presentation."],
    "연계: 객실 약 12개(a dozen) 예약 → 10개 이상이면 15% 할인."),
   ("What does Ms. Kowalski ask for?",
    ["Information about food", "A tour of the lodge", "Directions from Chicago", "A list of local trainers"],
    "send me your menu options → 음식 정보."),
   ("In the e-mail, the word \"appropriate\" in paragraph 2, line {LINE:appropriate}, is closest in meaning to",
    ["suitable", "official", "generous", "permitted"], "a room of the appropriate size = 알맞은 크기 → suitable."),
  ]},
 # 181-185
 {"intro": "article and e-mail",
  "passages": [{"kind": "article_two_col", "title": "Greenway Bike Share Program to Expand", "byline": "By Marcus Lee",
    "col1": ["PORTVILLE (April 2)—The city's bike share program, Greenway, will add 15 new stations and 200 bicycles this "
             "summer, bringing its total to 55 stations. The expansion, funded by a state transportation grant, will extend "
             "service to the Eastside and Harbor districts for the first time.",
             "Since its launch three years ago, Greenway has recorded more than 400,000 rides. Most riders use annual "
             "memberships, which cost $80 and allow unlimited rides of up to 45 minutes each."],
    "col2": ["Under a new pricing plan taking effect on June 1, single rides will cost $3 instead of $2.50. Annual memberships "
             "will remain at the current price.",
             "\"We kept the membership price the same to reward our regular riders,\" said program director Alisha Grant. The new "
             "stations are scheduled to open on July 15. A map of the planned locations is available at "
             "www.greenwayportville.org."]},
   {"kind": "email_gray",
    "hdr": [("To:", "info@greenwayportville.org"), ("From:", "Ben Castillo"), ("Date:", "July 30"),
            ("Subject:", "Pier Avenue station")],
    "body": ["Hello,",
             "I live in the Harbor district and was excited to read that Greenway would finally reach my neighborhood. I bought an "
             "annual membership last week, and I have been using the new station on Pier Avenue every day to get to work.",
             "However, the station has been completely empty by 8:00 A.M. on three of the last five mornings. When this happens, I "
             "have to walk twenty minutes to the next station. Are there plans to add more bicycles at Pier Avenue or to restock it "
             "earlier in the day?",
             "Thank you,<br/>Ben Castillo"]}],
  "qs": [
   ("What is the article mainly about?",
    ["The growth of a transportation service", "The opening of a bicycle shop", "A new state law on cycling",
     "The results of a survey of riders"], "정거장·자전거 추가 = 서비스 확장."),
   ("According to the article, what will happen on June 1?",
    ["The price of a single ride will increase.", "New stations will open.", "Annual memberships will become more expensive.",
     "A state grant will be awarded."], "6/1 단건 $2.50 → $3. 새 정거장은 7/15(B 함정), 연간 회원권은 동결(C 함정)."),
   ("How much did Mr. Castillo most likely pay for his membership?",
    ["$2.50", "$3", "$45", "$80"], "연계: 7월 말에 연간 회원권 구매 + 회원권 가격은 그대로 → $80. 45는 분(minute) 숫자 함정.", 3),
   ("What is suggested about the Pier Avenue station?",
    ["It opened in mid-July.", "It is located next to Mr. Castillo's office.", "It has more bicycles than other stations.",
     "It was paid for by local businesses."],
    "연계: Harbor 지구는 이번이 처음 + 새 정거장 개장일 7/15 → 7월 중순 개장."),
   ("What problem does Mr. Castillo describe?",
    ["Bicycles are often unavailable.", "His membership card does not work.", "A station has been moved.",
     "Rides are limited to 45 minutes."], "아침 8시면 정거장이 텅 빔 → 자전거를 못 빌림."),
  ]},
 # 186-190
 {"intro": "Web page, e-mail, and receipt",
  "passages": [{"kind": "web_tabs", "url": "https://www.kestrelculinary.com/classes",
    "tabs": ["Home", "Classes", "Instructors", "Gift Cards"], "active": 1, "title": "Weekend Classes: November",
    "body": ["All classes are held at our Fulton Street kitchen and include ingredients and recipe cards. Participants should "
             "wear closed-toe shoes.",
             "• Saturday, Nov. 2: Fresh Pasta Basics (Chef Amara Diallo), $75",
             "• Saturday, Nov. 9: Thai Street Food (Chef Niran Chai), $85",
             "• Saturday, Nov. 16: Holiday Baking (Chef Amara Diallo), $90",
             "• Saturday, Nov. 23: Knife Skills for Beginners (Chef Paul Lindgren), $60",
             "Members of our Kitchen Club receive 10 percent off all classes. Cancellations made at least 72 hours before a class "
             "receive a full refund; later cancellations receive class credit."]},
   {"kind": "email_classic",
    "hdr": [("To:", "classes@kestrelculinary.com"), ("From:", "Joanna Pike &lt;jpike@morrowdesign.com&gt;"),
            ("Date:", "November 5"), ("Subject:", "Class change")],
    "body": ["Hello,",
             "I am registered for the Thai Street Food class this Saturday. Unfortunately, I have just been asked to attend a "
             "business conference in Seattle that weekend, so I will not be able to come. Would it be possible to switch to Chef "
             "Diallo's class the following week instead? I took her class last Saturday and enjoyed it very much.",
             "I understand there may be a difference in price. Please let me know how much I owe.",
             "Joanna Pike"]},
   {"kind": "table_box", "title": "Kestrel Culinary School: Payment Receipt", "serif": False,
    "rows": [["Item", "Amount"],
             ["Holiday Baking, Nov. 16 (member price)", "$81.00"],
             ["Credit: Thai Street Food, Nov. 9 (member price)", "–$76.50"],
             ["<b>Amount paid</b>", "<b>$4.50</b>"]],
    "widths": [0.75, 0.25],
    "after": ["Customer: Joanna Pike (Kitchen Club member #4471)", "Paid by credit card on November 6. Thank you!"]}],
  "qs": [
   ("What is indicated about the classes?",
    ["Their cost includes ingredients.", "They are all taught by the same chef.", "They are held on weekdays.",
     "They require previous cooking experience."], "include ingredients and recipe cards."),
   ("Why does Ms. Pike want to change her registration?",
    ["She has to travel for work.", "She is unhappy with an instructor.", "The class time has been changed.",
     "She prefers baking to cooking."], "Seattle 출장(business conference) → 업무로 이동."),
   ("What is suggested about Ms. Pike?",
    ["She attended a class on November 2.", "She works for Kestrel Culinary School.", "She lives in Seattle.",
     "She has taken a class with Chef Chai before."],
    "연계: '지난 토요일 Diallo 셰프 수업' + 메일 11/5 → 11/2 Fresh Pasta Basics 수강."),
   ("Which class will Ms. Pike most likely attend?",
    ["Holiday Baking", "Fresh Pasta Basics", "Thai Street Food", "Knife Skills for Beginners"],
    "연계: Diallo 셰프의 '다음 주' 수업 = 11/16 Holiday Baking (영수증에도 확인)."),
   ("What does the receipt indicate about Ms. Pike?",
    ["She received a membership discount.", "She paid in cash.", "Her refund will be mailed to her.",
     "Her class has been canceled."], "member price + Kitchen Club member → 10% 할인 적용(90→81, 85→76.50)."),
  ]},
 # 191-195
 {"intro": "e-mail, schedule, and e-mail",
  "passages": [{"kind": "email_gray",
    "hdr": [("To:", "All Staff"), ("From:", "Priya Natarajan"), ("Date:", "March 3"),
            ("Subject:", "New project management software")],
    "body": ["Dear colleagues,",
             "On April 1, we will replace our current project management tool with TaskBridge, a system that lets teams share files "
             "and track deadlines in one place. To help everyone prepare, the IT department will offer hands-on training sessions "
             "throughout March. The schedule is attached.",
             "Each session lasts 90 minutes and is limited to twelve people so that trainers can give individual attention. Sessions "
             "for managers will also cover how to create reports for clients. Please sign up for one session by March 10 using the "
             "link on the intranet.",
             "Priya Natarajan, IT Manager"]},
   {"kind": "table_box", "title": "TaskBridge Training Schedule (Room 4B)", "serif": False,
    "rows": [["Date", "Time", "Group", "Trainer"],
             ["March 14", "9:00 A.M.", "All staff", "Leo Park"],
             ["March 17", "2:00 P.M.", "Managers", "Leo Park"],
             ["March 20", "10:30 A.M.", "All staff", "Ana Ruiz"],
             ["March 24", "3:00 P.M.", "Managers", "Ana Ruiz"],
             ["March 27", "9:00 A.M.", "All staff*", "Ana Ruiz"]],
    "widths": [0.24, 0.24, 0.26, 0.26],
    "after": ["* The March 27 session will be held in Room 2A."]},
   {"kind": "email_title",
    "hdr": [("To:", "Priya Natarajan"), ("From:", "Gordon Blake"), ("Date:", "March 12"), ("Subject:", "Training session")],
    "body": ["Hi Priya,",
             "I signed up for the managers' session with Leo Park, but I've just learned that I need to meet a client in Boston that "
             "afternoon. Could I move to the other managers' session instead? I'm especially interested in learning to produce "
             "client reports, since my team sends weekly updates to three major accounts.",
             "Also, I apologize for registering late. I was away on vacation last week.",
             "Thanks,<br/>Gordon Blake, Accounts Manager"]}],
  "qs": [
   ("What is the main purpose of the first e-mail?",
    ["To announce training for a new system", "To request feedback on some software", "To introduce a new IT manager",
     "To report a technical problem"], "새 프로그램 도입 + 교육 일정 안내."),
   ("What is indicated about the training sessions?",
    ["They have a limited number of participants.", "They are held online.", "They last a full day.",
     "They are optional for managers."], "limited to twelve people."),
   ("When will Mr. Blake most likely attend training?",
    ["On March 14", "On March 17", "On March 24", "On March 27"],
    "연계: 관리자 세션은 3/17(Park)·3/24(Ruiz). Park 세션을 못 가니 '다른 관리자 세션' = 3/24.", 2),
   ("What is true about the session on March 27?",
    ["It will take place in a different room.", "It is intended for managers.", "It will be led by Mr. Park.",
     "It has been canceled."], "표 각주: Room 2A (나머지는 4B)."),
   ("What does Mr. Blake indicate in his e-mail?",
    ["He missed a registration deadline.", "He has never used project management software.", "He will be in Boston on March 24.",
     "He supervises three employees."],
    "연계: 마감 3/10, 메일 3/12 + 'registering late' → 마감 놓침. three major accounts는 고객사(D 함정)."),
  ]},
 # 196-200
 {"intro": "article, e-mail, and online review",
  "passages": [{"kind": "article_narrow", "title": "Food Truck Festival Returns",
    "body": ["MILFORD (June 3)—The Milford Food Truck Festival will return to Riverside Park on Saturday, June 22, from 11 A.M. to "
             "9 P.M. Now in its fifth year, the festival will feature 40 food trucks, live music, and a children's area with games "
             "and face painting.",
             "Admission is free, but visitors are encouraged to buy food tokens in advance on the festival Web site, where a set of "
             "ten costs $9. Tokens bought on the day of the festival will cost $10 per set. Organizers say the token system has "
             "[[shortened]] lines at the trucks because vendors no longer need to handle cash.",
             "For the first time, this year's festival will also include a competition. Visitors can vote for their favorite truck, "
             "and the winner will receive a free booth at the Milford Autumn Market in October."]},
   {"kind": "email_classic",
    "hdr": [("To:", "Hyun-woo Lee &lt;hlee@seoulstreetkitchen.com&gt;"), ("From:", "Carla Benson &lt;cbenson@milfordfoodfest.org&gt;"),
            ("Date:", "June 24"), ("Subject:", "Congratulations!"), ("Attachment:", "Autumn_Market_Info.pdf")],
    "body": ["Dear Mr. Lee,",
             "Congratulations! Seoul Street Kitchen received the most votes from festival visitors on Saturday, with more than 1,200 "
             "people choosing your truck. Many of them commented on your kimchi tacos and the friendliness of your staff.",
             "As promised, you have earned a free booth at the Milford Autumn Market. Please review the attached information packet, "
             "which includes the market dates and set-up instructions, and confirm your participation by July 15.",
             "Best regards,<br/>Carla Benson, Festival Coordinator"]},
   {"kind": "review", "site": "https://www.milfordlocal.com/reviews", "stars": 4, "title": "Seoul Street Kitchen",
    "body": ["I finally tried Seoul Street Kitchen at the Autumn Market last weekend after hearing that it had won the summer "
             "festival's competition. The kimchi tacos lived up to the hype, and the bulgogi rice bowl was generous. My only "
             "complaint is the wait: it took nearly 30 minutes to reach the front of the line, even though the market was not "
             "especially crowded. I hope the truck becomes a regular at the market.",
             "—Diane Morales, October 14"]}],
  "qs": [
   ("What is NOT mentioned in the article as part of the festival?",
    ["Cooking classes", "A children's area", "Live music", "A competition"], "요리 수업은 언급 없음."),
   ("What is indicated about the food tokens?",
    ["They cost less when bought before the event.", "They can be used at the Autumn Market.", "They are sold only at the park.",
     "They are required for admission."], "사전 구매 $9 < 당일 $10. 입장은 무료(D 함정)."),
   ("In the article, the word \"shortened\" in paragraph 2, line {LINE:shortened}, is closest in meaning to",
    ["reduced", "summarized", "interrupted", "closed"], "줄(lines)을 짧게 했다 → reduced. summarized는 글을 '요약'할 때."),
   ("What is suggested about Mr. Lee?",
    ["He confirmed that he would participate in the Autumn Market.", "He started his business five years ago.",
     "He helped organize the festival.", "He changed his menu after the festival."],
    "연계: 7/15까지 참가 확정 요청 → 10월 리뷰에서 실제로 Autumn Market에 나옴 → 확정했음. five years는 축제 연차(B 함정)."),
   ("What does Ms. Morales say about Seoul Street Kitchen?",
    ["Customers had to wait a long time.", "Its prices were too high.", "Its staff were unfriendly.", "Its portions were small."],
    "30분 대기. 직원 친절(이메일)·양 넉넉(generous)과 반대되는 선지가 함정."),
  ]},
]
P5_GAPS = (12, 12, 15, 15, 24, 24)  # tighter than TEST 11: longer stems
