# TEST 26 — full RC mock: Part 5 from 동하's own "TOEIC Part 5 Practice Test 01" (answers re-placed),
# Part 6 + Part 7 176-200 from TEST 25 (blueprint level), Part 7 147-175 from TEST 12 (unsolved).
import t12_items, t25_items
DIVIDER_NOTE = "실전 모의고사: P5 Practice Test 01 + P6·P7 다중지문(TEST 25) + P7 단일지문(TEST 12). 개인 학습용."
PART5 = [
 ("The marketing director asked all team members to submit their reports ------- the end of the day.", ["by", "during", "since", "among"], "전치사 (기한): by + 시점 = ~까지. during은 기간, since는 과거 기점."),
 ("Ms. Park's ------- presentation impressed the clients and helped the firm win the contract.", ["persuasive", "persuade", "persuasion", "persuasively"], "명사 presentation 앞 형용사 자리."),
 ("Employees who wish to take vacation days must obtain approval from ------- supervisors in advance.", ["their", "they", "them", "theirs"], "명사 앞 소유격 대명사."),
 ("The new software will allow users to ------- large amounts of data quickly and securely.", ["process", "processing", "processed", "processes"], "allow + 목적어 + to + 동사원형."),
 ("Because of the heavy snow, the outdoor concert has been ------- until next Saturday.", ["postponed", "resigned", "declined", "repaired"], "어휘: 연기되다. resign·decline·repair는 문맥 불일치."),
 ("------- the budget was approved last month, construction of the new library has not yet begun.", ["Although", "Despite", "However", "Instead"], "뒤가 절 → 접속사 Although. Despite는 전치사, However·Instead는 부사."),
 ("The shipping department is ------- for ensuring that all orders are delivered on time.", ["responsible", "responsibly", "responsibility", "responsibilities"], "be responsible for ~ (보어 자리 형용사)."),
 ("Mr. Dawson ------- the sales report to the board every Monday morning.", ["presents", "present", "presenting", "to present"], "3인칭 단수 + 현재 습관(every Monday) → presents."),
 ("Hartley Electronics offers a full refund on any product returned ------- thirty days of purchase.", ["within", "between", "toward", "against"], "within + 기간: ~ 이내에."),
 ("The company's profits increased ------- last quarter, exceeding all expectations.", ["significantly", "significant", "significance", "signify"], "동사 increased를 꾸미는 부사."),
 ("All visitors must sign in at the front desk ------- entering the research laboratory.", ["before", "so that", "either", "whereas"], "before + 동명사: ~하기 전에."),
 ("The interviewer was impressed by the candidate's ------- of the local market.", ["knowledge", "know", "knowing", "knowledgeable"], "소유격 뒤 명사 자리 (knowledge of ~)."),
 ("Of the three proposals submitted, only ------- met all of the requirements set by the committee.", ["one", "other", "another", "each other"], "only one: 세 개 중 단 하나만."),
 ("The conference room is ------- for use by staff members from 9 A.M. to 5 P.M. daily.", ["available", "valuable", "capable", "reliable"], "be available for ~: 이용 가능한."),
 ("Please ------- that all electronic devices are turned off before the meeting begins.", ["ensure", "enroll", "entrust", "enclose"], "ensure that ~. 나머지는 that절을 받지 못함."),
 ("Mr. Kim ------- the report by the time the meeting started.", ["had finished", "finishes", "will finish", "finishing"], "by the time + 과거 → 과거완료."),
 ("The newly hired accountant is ------- than anyone else in the finance department.", ["more efficient", "efficient", "most efficient", "efficiently"], "than → 비교급."),
 ("------- interested in the open position should send a résumé to the personnel office.", ["Anyone", "Who", "Whoever", "Which"], "Anyone (who is) interested ~."),
 ("The airline apologized to passengers for the ------- caused by the delayed flight.", ["inconvenience", "inconvenient", "inconveniently", "inconvenienced"], "the 뒤 명사, caused는 후치 수식."),
 ("Residents are advised to conserve water ------- the dry season.", ["during", "while", "because", "so"], "명사구 앞 → 전치사 during."),
 ("The tour guide spoke so ------- that the visitors in the back could not hear her.", ["quietly", "quiet", "quieter", "quietness"], "동사 spoke를 꾸미는 부사 (so ~ that)."),
 ("Ms. Alvarez was ------- to the position of regional manager after only two years with the firm.", ["promoted", "promoting", "promotion", "promotes"], "be promoted to ~."),
 ("Due to a ------- of qualified applicants, the hiring process has been extended by two weeks.", ["shortage", "shorten", "shortly", "shortest"], "a + 명사 + of: a shortage of."),
 ("The proposed merger will ------- affect the way the two companies operate.", ["dramatically", "dramatic", "drama", "dramatize"], "조동사와 동사 사이 부사."),
 ("Neither the manager ------- the assistants were aware of the schedule change.", ["nor", "and", "but", "or"], "neither A nor B."),
 ("Customers who are ------- with their purchases may return them at any time.", ["dissatisfied", "satisfying", "satisfaction", "satisfactorily"], "be dissatisfied with ~ (반품과 문맥 일치)."),
 ("The board will make a final decision ------- the merger at next week's meeting.", ["on", "to", "at", "for"], "decision on ~."),
 ("Participants in the workshop were asked to ------- their questions to the moderator in writing.", ["submit", "submits", "submitted", "submission"], "be asked to + 동사원형."),
 ("The restaurant's popularity is ------- to its reasonable prices and friendly service.", ["due", "because", "despite", "regarding"], "be due to ~: ~ 때문이다."),
 ("The committee members could not agree on ------- of the two candidates should be hired.", ["which", "what", "whose", "whom"], "which of the two ~ (의문사절의 주어)."),
]
PART6 = t25_items.PART6
_singles = [dict(s) for s in t12_items.PART7[:10]]
for s in _singles:
    s.pop("start", None); s.pop("pages", None)
_multis = [dict(s) for s in t25_items.PART7]
_multis[0].pop("start", None)
PART7 = _singles + _multis
P5_GAPS = (12, 12, 15, 15, 24, 24)
