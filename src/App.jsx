import { useState, useEffect, Component } from "react";

const KR = "'Noto Sans KR', sans-serif";
const MO = "'JetBrains Mono', monospace";

try {
  if (typeof document !== "undefined" && !document.getElementById("ct-gf")) {
    const l = document.createElement("link"); l.id = "ct-gf"; l.rel = "stylesheet";
    l.href = "https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=JetBrains+Mono:wght@400;600&display=swap";
    document.head.appendChild(l);
  }
} catch(e) {}

const C = {
  // 토스 검정 다크 팔레트
  coral:"#3182f6", coralDark:"#1b64da",        // 포인트 = 토스 블루
  bg:"#0e0f11", surface:"#17181c", surfaceLight:"#202228",
  ink:"#ffffff", inkMute:"#9ea3ad", inkSubtle:"#5e636e",
  border:"#26282e",
  green:"#f04452", red:"#f04452", amber:"#ffa726", blue:"#3d8bff",  // 상승=빨강, 하락=파랑
};


const TODAY_BRIEF = {
  id:"2026-04-23",
  date:"2026년 4월 23일 (목)",
  sentiment:68,
  sentimentLabel:"신중한 낙관",
  headline:"SK하이닉스 실적과 한국 GDP가 KOSPI 방향 결정",
  oneLiner:"간밤 S&P·나스닥 사상 최고. 시간외 테슬라·IBM·ServiceNow 실망. 오늘 08시 한국 Q1 GDP(+1.7%)와 SK하이닉스 영업익 37.6조 발표가 모든 걸 결정.",
  overnight:[
    {k:"S&P 500",v:"7,137.90",c:"+1.05%",up:true},
    {k:"나스닥",v:"24,657.57",c:"+1.64%",up:true},
    {k:"PHLX 반도체",v:"16일 연속↑",c:"사상 최장",up:true},
    {k:"미 10년물",v:"4.305%",c:"+1bp",up:false},
    {k:"브렌트",v:"$101.81",c:"+3.38%",up:false},
    {k:"비트코인",v:"$78,551",c:"+3.75%",up:true},
    {k:"원/달러",v:"1,476",c:"-7.5원",up:true},
    {k:"공포&탐욕",v:"68",c:"신중한 낙관",up:true},
  ],
  afterHours:[
    {t:"TSLA",c:-2.0,r:"매출 $22.39B 미스, 2026 CapEx $25B 상향, HW3.0 FSD 불가 시인"},
    {t:"IBM",c:-6.8,r:"가이던스 재확인에 그침"},
    {t:"ServiceNow",c:-14,r:"중동 온프레미스 딜 지연"},
    {t:"Lam Research",c:4.0,r:"2026 WFE $140B 상향 → 韓 장비사 호재"},
  ],
  themes:[
    {icon:"💥",title:"SK하이닉스 실적 D-DAY",desc:"영업익 37.6조 컨센, 영업이익률 첫 70%대. 강도에 따라 KOSPI 6,500 돌파 vs 순환매 붕괴"},
    {icon:"🚀",title:"한국 Q1 GDP +1.7% QoQ",desc:"컨센 +0.9% 대폭 상회. 5년 반만 최대. BOK 5월 동결 확정"},
    {icon:"🚗",title:"현대차 Q1 영업익 -26.65%",desc:"매출 45.77조 사상최대에도 관세+화재+유가 3중고"},
    {icon:"⚔️",title:"이란 호르무즈 재긴장",desc:"2차 종전협상 이란 불참. 美 상선 나포 경고. 유가 $100+ 재돌파"},
    {icon:"🏛️",title:"Warsh 인준 + Fed 블랙아웃",desc:"매파 발언 수위에 10Y 반응. 4/28-29 FOMC 동결 98%"},
  ],
  catalysts:[
    {t:"08:00",e:"🇰🇷 Q1 GDP 속보치",imp:"critical"},
    {t:"장전",e:"📢 SK하이닉스 Q1 실적",imp:"critical"},
    {t:"장중",e:"🚗 현대차 Q1 실적",imp:"high"},
    {t:"22:45",e:"🇺🇸 S&P 플래시 PMI",imp:"critical"},
    {t:"새벽",e:"💻 Intel Q1 (AMC)",imp:"high"},
  ],
  conclusion:{
    best:"조선·전력기기·방산 순환매 2차 파동 (HD현대중공업·현대로템·두산에너빌리티)",
    trap:"엔터 2인방(하이브·SM) 데드캣바운스, LG화학 지분가치 매력 함정",
    cash:"현금 비중 20~30% 유지. 종가 레버리지 금물",
    msg:"GDP 서프라이즈 + 하이닉스 빅비트면 KOSPI 6,500p 돌파. 반대로 '40조 미달' 또는 현대차 쇼크면 6,380p 지지 테스트.",
  },
};

const NEWS_TOP10 = [
  {r:1,src:"한국경제",cat:"🔥 최우선",title:"SK하이닉스 1Q 영업익 37.6조 컨센 — 영업이익률 첫 70% 돌파 전망",impact:"서프라이즈 시 KOSPI 6,500p / 미달 시 차익실현"},
  {r:2,src:"매일경제",cat:"🇰🇷 GDP",title:"한국 Q1 GDP +1.7% QoQ — 5년 반만 최대 성장",impact:"KOSPI 갭업 + 원화 강세. 외국인 유입 모멘텀"},
  {r:3,src:"CNBC",cat:"📉 시간외",title:"테슬라 -2%, IBM -6.8%, ServiceNow -14% — 시간외 실망",impact:"미 지수선물 -0.2% 약세 전환"},
  {r:4,src:"Bloomberg",cat:"🏛️ 연준",title:"Warsh 인준 청문회 '체제 전환' 예고 — 10Y +4bp",impact:"달러 재강세·장기물 상방 압력"},
  {r:5,src:"Reuters",cat:"⚔️ 지정학",title:"이란 2차 종전협상 불참 — 호르무즈 美 상선 나포 경고",impact:"유가 $100+ 재돌파. 방산·조선 호재"},
  {r:6,src:"Reuters",cat:"🚢 조선",title:"HD현대중공업 +11.28% — 스웨덴 쇄빙선 + AEG 데이터센터 발전기 수주",impact:"조선+AI 전력 슈퍼 사이클"},
  {r:7,src:"매일경제",cat:"🚗 자동차",title:"현대차 Q1 영업익 2.67조 -26.65% — 관세+화재+유가 3중고",impact:"자동차 밸류체인 전반 압박"},
  {r:8,src:"Bloomberg",cat:"🤖 AI",title:"SK하이닉스 120만원 돌파 — 엔비디아 베라 루빈 SOCAMM2 양산",impact:"한미반도체·이수페타시스 동반 수혜"},
  {r:9,src:"연합인포맥스",cat:"🎤 엔터",title:"하이브 방시혁 의장 1,900억 부정거래 구속영장 신청",impact:"하이브·SM 동반 약세"},
  {r:10,src:"FT",cat:"💱 관세",title:"트럼프 OBBBA 법안 9월 IRA 세액공제 조기 종료 확정",impact:"LG화학 LGES 2026 영업익 -45% 전망"},
];

const SIGNALS = [
  {
    t:"SK하이닉스",code:"000660",cur:1230000,action:"분할 매수",actCol:"green",conf:80,
    timing:"실적 발표(4/23 장전) 후 시초가 30분 관망 → 갭상승 시 추격 X / 갭하락 시 분할 진입",
    entry:[
      {l:"1차 (40%)",p:"1,180,000",r:"20일선 + 직전 저점 지지"},
      {l:"2차 (30%)",p:"1,150,000",r:"60일선 근접 + RSI 35 과매도권"},
      {l:"3차 (30%)",p:"1,100,000",r:"심리적 지지선 + 강한 매수세"},
    ],
    exit:[
      {l:"1차 (30%)",p:"1,400,000",r:"+14%, 메리츠 목표가"},
      {l:"2차 (40%)",p:"1,600,000",r:"+30%, 컨센 평균"},
      {l:"3차 (30%)",p:"1,800,000",r:"+46%, 삼성/씨티 목표"},
    ],
    stop:"1,080,000 (-12%)",hold:"1~3개월",
    bull:"HBM4 엔비디아 독점, 영업이익률 첫 70%, 2026 DRAM +170%·NAND +190% 전망",
    bear:"40조 컨센 미달시 'buy rumor sell news', 6개월 +60% 급등 차익실현, 6-7월 ADR $10B 조달 수급 부담",
  },
  {
    t:"HD현대중공업",code:"329180",cur:500000,action:"매수 검토",actCol:"green",conf:78,
    timing:"4/23 실적 당일 시초가 변동성 클 것. 갭상승 7%+ 시 다음날 눌림목 매수가 안전",
    entry:[
      {l:"1차 (50%)",p:"485,000",r:"5일선 지지 + 거래량 동반 확인"},
      {l:"2차 (50%)",p:"465,000",r:"3/31 EB 발행 저점 지지"},
    ],
    exit:[
      {l:"1차 (40%)",p:"600,000",r:"+20%, 메리츠 목표가"},
      {l:"2차 (40%)",p:"720,000",r:"+44%, 메리츠 목표"},
      {l:"3차 (20%)",p:"850,000",r:"+70%, 한국투자/iM 목표"},
    ],
    stop:"460,000 (-8%)",hold:"1~3개월",
    bull:"22개사 Strong Buy. 스웨덴 쇄빙선 5,150억+AEG 6,271억 동시 수주. AI 전력 테마 겹침",
    bear:"3/31 $2B 교환사채 희석. 추가 블록딜 가능. 호르무즈 완화시 프리미엄 되돌림",
  },
  {
    t:"한미반도체",code:"042700",cur:190000,action:"단기 트레이딩",actCol:"amber",conf:70,
    timing:"SK하이닉스 실적 결과 100% 연동. 하이닉스 서프라이즈 시 즉시 매수, 미스 시 회피",
    entry:[
      {l:"하이닉스 +5%↑",p:"195,000~205,000",r:"실적 서프라이즈 동반 매수"},
      {l:"하이닉스 변동 미미",p:"180,000~185,000",r:"60일선 지지 후 진입"},
    ],
    exit:[
      {l:"1차 (50%)",p:"220,000",r:"+16%, 단기 저항"},
      {l:"2차 (50%)",p:"240,000",r:"+26%, 리딩투자 목표"},
    ],
    stop:"165,000 (-13%)",hold:"1~4주 (하이닉스 연동)",
    bull:"HBM4 TC BONDER 4 양산 완료. 2026말 Wide TC Bonder 출시. 하이닉스 연동 레버리지",
    bear:"하이닉스 조정시 1.5배 동반 급락. 한화세미텍 경쟁. PER 59배 고평가",
  },
  {
    t:"현대로템",code:"064350",cur:260000,action:"중기 매수",actCol:"green",conf:75,
    timing:"방산 차익실현 진정 확인 후 분할. 호르무즈 이벤트 시 단기 급등 가능",
    entry:[
      {l:"1차 (50%)",p:"248,000",r:"20일선 + 4월 박스 하단"},
      {l:"2차 (50%)",p:"235,000",r:"60일선 + 거래량 확인"},
    ],
    exit:[
      {l:"1차 (40%)",p:"290,000",r:"+12%, 삼성증권 목표가"},
      {l:"2차 (60%)",p:"320,000~340,000",r:"+23~31%, 한국투자/키움 목표"},
    ],
    stop:"235,000 (-10%)",hold:"1~3개월",
    bull:"12개사 18명 전원 BUY. 2025 영업익 +120% 사상최대. 폴란드 2차 K2 + 이라크/루마니아",
    bear:"중동전 드론·미사일 공중전 전환 → 지상전력 예산 축소 우려. 폴란드 K2 2차 820대 지연시 동력 약화",
  },
  {
    t:"두산에너빌리티",code:"034020",cur:115800,action:"관망 후 진입",actCol:"amber",conf:68,
    timing:"평균 목표 12만 근접. 4/29 실적 후 조정 시 진입이 안전. 추격매수 비추",
    entry:[
      {l:"보수적 (60%)",p:"108,000~112,000",r:"60일선 + 4월 박스 중간"},
      {l:"공격적 (40%)",p:"99,000~103,000",r:"120일선 강한 지지"},
    ],
    exit:[
      {l:"1차 (50%)",p:"125,000",r:"+8%, 컨센 평균"},
      {l:"2차 (50%)",p:"145,000~155,000",r:"+25~34%, 유진 목표가"},
    ],
    stop:"99,500 (-14%)",hold:"6개월+",
    bull:"19개사 Strong Buy. X-energy SMR 16기 주기기. 빅테크 H급 가스터빈 7기. 2026 수주 14.6조",
    bear:"평균 목표 12만 근접 → 추가 멀티플 제한. 체코 원전 공시 지연시 모멘텀 공백. 배당 0%",
  },
];

const TICKERS = {
  "SK하이닉스":{kr:"000660",cur:1230000,sec:"반도체"},
  "HD현대중공업":{kr:"329180",cur:500000,sec:"조선"},
  "한미반도체":{kr:"042700",cur:190000,sec:"반도체장비"},
  "현대로템":{kr:"064350",cur:260000,sec:"K-방산"},
  "두산에너빌리티":{kr:"034020",cur:115800,sec:"원전"},
  "삼성전자":{kr:"005930",cur:90000,sec:"반도체"},
  "현대차":{kr:"005380",cur:215000,sec:"자동차"},
  "한화에어로":{kr:"012450",cur:1378000,sec:"K-방산"},
};

const FMT = v => v==null||isNaN(+v)?"—":(+v).toLocaleString("ko-KR");

// 💼 내 보유종목 (2026-05-22 새벽 매수, 시드 160만원)
// buyUsd = 5/21 미국 종가(매수단가 추정), krAmount = 투자 원금(원화)
const HOLDINGS = [
  { sym:"VRT",  name:"버티브 홀딩스",      sec:"데이터센터",  krAmount:136567, buyUsd:323.40 },
  { sym:"IONQ", name:"아이온큐",          sec:"양자컴퓨팅",  krAmount:287048, buyUsd:58.89  },
  { sym:"AVAV", name:"에어로바이런먼트",   sec:"드론·방산",   krAmount:710543, buyUsd:163.09 },
  { sym:"AMD",  name:"AMD",              sec:"반도체",      krAmount:340860, buyUsd:449.59 },
  { sym:"ASTS", name:"AST 스페이스모바일", sec:"위성통신",    krAmount:201347, buyUsd:96.23  },
];
const HOLDING_SYMS = HOLDINGS.map(h=>h.sym);
const BUY_FX = 1500; // 매수 시점(5/22 새벽) 환율 추정

// ⭐ 관심 미국주 (추천)
const WATCH_US = [
  { sym:"NVDA", name:"엔비디아",  sec:"AI 반도체" },
  { sym:"PLTR", name:"팔란티어",  sec:"AI 소프트웨어" },
  { sym:"RKLB", name:"로켓랩",    sec:"우주발사체" },
];

/* ════ 스토랩스 시스템 데이터 ════ */
const MACRO = [
  {k:"NASDAQ", v:"24,468", c:"+1.52%", up:true},
  {k:"S&P 500", v:"7,126.06", c:"+1.20%", up:true},
  {k:"USD/KRW", v:"1,466원", c:"-13.1 (-0.89%)", up:false, blue:true},
  {k:"VIX 공포", v:"17.48", c:"-0.46p", up:false, blue:true},
  {k:"DXY 달러", v:"98.23", c:"+0.02%", up:true},
  {k:"금 (GOLD)", v:"$4,880", c:"+1.36%", up:true},
];

const STOCKS = {
  RKLB: {
    name:"로켓랩", flag:"🇺🇸", ticker:"RKLB",
    cur:85.39, prevClose:84.39, change:1.19,
    high52w:99.58, low52w:43.80,
    monthMA5:69.75, ma5Diff:21.2,
    weekVolRatio:1.0, drawdown:-15.1, drawdownPct:84,
    nextEarnings:"2026.05.07", earningsDays:18,
    stoch:{ market:57.5, marketD:58.7, weekly:98.8, weeklyD:81.7, monthly:98.8 },
    levels:{
      target2:88.52, target1:86.66, center:85.13,
      defense1:83.27, defense2:81.74,
      buyTarget2:88.79, buyTarget1:86.92, buyCenter:85.39,
      buyDef1:83.52, buyDef2:81.99,
      sellTarget2:88.25, sellTarget1:86.40, sellCenter:84.87,
      sellDef1:83.02, sellDef2:81.49,
      afterMarket:84.50,
    },
    aiRec:{ buy:"center", sell:"target1" },
    signals:{
      ppRecover:"PP 회복을 시도 중이에요 · PP 안착을 확인한 뒤 R1 목표로 진입해보세요",
      stochSummary:"주봉 %K 93 (GC) · 월봉 %K 75 → 기울기 상승",
      ma5Note:"단기 추세가 살아있어요. 5주선 위를 유지하는 한 매수 우위예요.",
      defenseNote:"장기 방어선이에요 · 이 가격대에서 반등 가능성을 주시하세요",
      volNote:"평소와 비슷한 거래량이에요. 특별한 신호는 없어요.",
      drawdownNote:"신고가 대비 의미 있는 조정이 왔어요. 지지선 확인 후 분할 접근이 유효해요.",
      earningsNote:"한 달 내 실적 발표예요. 서서히 주시하면서 전략을 잡아요.",
    },
  },
};

const SEED_PRESETS = [
  {l:"1,000만", v:10000000},
  {l:"500만", v:5000000},
  {l:"100만", v:1000000},
  {l:"50만", v:500000},
  {l:"10만", v:100000},
];

const KRW_RATE = 1466;
const US2KRW = usd => Math.round(usd * KRW_RATE);

/* 레벨 라벨 */
const LEVEL_LABELS = {
  target2:"2차 목표", target1:"1차 목표", center:"중심선",
  defense1:"1차 방어", defense2:"2차 방어",
};

class ErrBoundary extends Component {
  constructor(p){ super(p); this.state={err:null}; }
  static getDerivedStateFromError(err){ return {err}; }
  render(){
    if(this.state.err) return (
      <div style={{padding:24,fontFamily:KR,background:C.bg,color:C.ink,minHeight:"100vh"}}>
        <div style={{fontSize:32,marginBottom:12}}>⚠</div>
        <h2 style={{color:C.coral,fontSize:18,marginBottom:8}}>오류</h2>
        <div style={{background:C.surface,padding:14,borderRadius:10,fontFamily:MO,fontSize:11,wordBreak:"break-word"}}>{String(this.state.err?.message||this.state.err)}</div>
      </div>
    );
    return this.props.children;
  }
}

function AppInner(){
  const [tab,setTab] = useState("today");
  const [showBrief,setShowBrief] = useState(false);
  const [openSig,setOpenSig] = useState(null);
  const [openNews,setOpenNews] = useState(null);
  const [time,setTime] = useState(new Date("2026-04-23T08:35:00"));

  // 스토랩스 state
  const [slStock,setSlStock] = useState("RKLB");
  const [slSeed,setSlSeed] = useState(20000000); // 2000만원 기본
  const [slSeedInput,setSlSeedInput] = useState("");
  const [slBuyLevel,setSlBuyLevel] = useState("center"); // AI 추천: 중심선
  const [slSellLevel,setSlSellLevel] = useState("target1"); // AI 추천: 1차 목표

  // 🔄 데이터 갱신 시스템 (정직한 수동 갱신)
  const [lastRefresh,setLastRefresh] = useState(()=>{
    try { const v=localStorage.getItem("ct_last_refresh"); return v?parseInt(v):Date.now(); }
    catch { return Date.now(); }
  });
  const [toast,setToast] = useState(null);
  const [showRefreshBanner,setShowRefreshBanner] = useState(false);
  // 사용자가 직접 입력한 현재가 (갱신 시 매수/매도 테이블 전체 재계산)
  const [livePrice,setLivePrice] = useState(()=>{
    try { const v=localStorage.getItem("ct_live_price"); return v?JSON.parse(v):{}; }
    catch { return {}; }
  });
  const [priceInput,setPriceInput] = useState("");

  // 🤖 AI 자동 갱신 (Claude API + Web Search)
  const [aiBrief,setAiBrief] = useState(()=>{
    try { const v=localStorage.getItem("ct_ai_brief"); return v?JSON.parse(v):null; }
    catch { return null; }
  });
  const [aiLoading,setAiLoading] = useState(false);
  const [aiError,setAiError] = useState(null);

  // 디버그: 마지막 응답 원본 저장 (에러 시 동하한테 보여주기)
  const [aiDebug,setAiDebug] = useState(null);
  const [showDebug,setShowDebug] = useState(false);

  // Claude API 호출 — 견고한 파싱 + web_search fallback
  // 🚀 진짜 백엔드 — 시세 + 매크로 + 뉴스 통합 자동 갱신
  const BACKEND_URL = "https://claude-trade-backend.vercel.app";
  const [liveMacro,setLiveMacro] = useState(()=>{
    try { const v=localStorage.getItem("ct_live_macro"); return v?JSON.parse(v):null; }
    catch { return null; }
  });
  const [liveStocks,setLiveStocks] = useState(()=>{
    try { const v=localStorage.getItem("ct_live_stocks"); return v?JSON.parse(v):null; }
    catch { return null; }
  });
  const [liveNews,setLiveNews] = useState(()=>{
    try { const v=localStorage.getItem("ct_live_news"); return v?JSON.parse(v):null; }
    catch { return null; }
  });

  const fetchAiBrief = async () => {
    setAiLoading(true);
    setAiError(null);
    setAiDebug(null);
    const debugLog = [];
    try {
      debugLog.push(`시작: ${new Date().toLocaleTimeString()}`);
      debugLog.push(`서버: ${BACKEND_URL}`);

      // 4개 API 동시 호출 (실패해도 다른 거 받기 위해 Promise.allSettled)
      const [marketR, quoteR, krR, newsR] = await Promise.allSettled([
        fetch(`${BACKEND_URL}/api/market`).then(r=>r.json()),
        fetch(`${BACKEND_URL}/api/quote?symbols=VRT,IONQ,AVAV,AMD,ASTS,NVDA,PLTR,RKLB`).then(r=>r.json()),
        fetch(`${BACKEND_URL}/api/krquote?codes=000660,005930,329180,034020,042700,064350,012450,005380`).then(r=>r.json()),
        fetch(`${BACKEND_URL}/api/news`).then(r=>r.json()).catch(()=>({success:false,error:"news endpoint 없음"})),
      ]);

      debugLog.push(`매크로: ${marketR.status}`);
      debugLog.push(`미국주: ${quoteR.status}`);
      debugLog.push(`한국주: ${krR.status}`);
      debugLog.push(`뉴스: ${newsR.status}`);

      const marketData = marketR.status==="fulfilled" ? marketR.value : null;
      const quoteData = quoteR.status==="fulfilled" ? quoteR.value : null;
      const krData = krR.status==="fulfilled" ? krR.value : null;
      const newsData = newsR.status==="fulfilled" ? newsR.value : null;

      if(marketR.status==="rejected") debugLog.push(`매크로 에러: ${marketR.reason?.message}`);
      if(quoteR.status==="rejected") debugLog.push(`미국주 에러: ${quoteR.reason?.message}`);
      if(krR.status==="rejected") debugLog.push(`한국주 에러: ${krR.reason?.message}`);

      // ✅ 하나라도 success:true면 작동
      const marketOk = marketData?.success;
      const quoteOk = quoteData?.success;
      const krOk = krData?.success;
      const newsOk = newsData?.success;

      if(!marketOk && !quoteOk && !krOk && !newsOk) {
        // 전부 실패한 경우만 에러
        const errors = [
          marketData?.error || (marketR.status==="rejected" ? marketR.reason?.message : ""),
          quoteData?.error || (quoteR.status==="rejected" ? quoteR.reason?.message : ""),
          krData?.error || (krR.status==="rejected" ? krR.reason?.message : ""),
          newsData?.error || "",
        ].filter(Boolean).join(" / ");
        throw new Error(errors || "백엔드 연결 실패");
      }
      debugLog.push(`성공: 매크로${marketOk?"✓":"✗"} 미국${quoteOk?"✓":"✗"} 한국${krOk?"✓":"✗"} 뉴스${newsOk?"✓":"✗"}`);

      const m = marketData?.macro || {};
      const fmt = (v, decimals=2) => v==null ? "—" : Number(v).toLocaleString("ko-KR", {minimumFractionDigits:0, maximumFractionDigits:decimals});
      const fmtChg = (v) => v==null ? "" : (v>=0?"+":"") + Number(v).toFixed(2) + "%";

      const usUp = (m.sp500?.changePct || 0) >= 0;
      const krwDown = (m.usdkrw?.changePct || 0) <= 0;
      const headline = m.sp500?.price
        ? `미국장 S&P ${fmtChg(m.sp500?.changePct)} · 나스닥 ${fmtChg(m.nasdaq?.changePct)} · 원달러 ${fmt(m.usdkrw?.price)}원`
        : "시세 가져오는 중...";

      // 종목 시세 → livePrice + liveStocks 자동 업데이트
      const newLivePrices = {...livePrice};
      const krNameMap = {
        "000660":"SK하이닉스", "005930":"삼성전자", "329180":"HD현대중공업",
        "034020":"두산에너빌리티", "042700":"한미반도체", "064350":"현대로템",
        "012450":"한화에어로", "005380":"현대차",
      };
      const krSecMap = {
        "000660":"반도체","005930":"반도체","329180":"조선","034020":"원전",
        "042700":"반도체장비","064350":"K-방산","012450":"K-방산","005380":"자동차",
      };
      const stocksList = [];
      let topStock = "—";
      let topChange = -999;
      let updateCount = 0;
      // 한국주
      (krData?.quotes || []).forEach(q => {
        const name = krNameMap[q.symbol] || q.name || q.symbol;
        stocksList.push({ key:name, name, code:q.symbol, sec:krSecMap[q.symbol]||"", market:"KR",
          price:q.price, change:q.change, changePct:q.changePct, volume:q.volume, high:q.high, low:q.low });
        if(q.price) { newLivePrices[name] = { price:q.price, at:Date.now() }; updateCount++; }
        if((q.changePct||-999) > topChange) { topChange=q.changePct; topStock=`${name} ${fmtChg(q.changePct)}`; }
      });
      // 미국주 (보유 5 + 관심 3)
      (quoteData?.quotes || []).forEach(q => {
        stocksList.push({ key:q.symbol, name:q.name||q.symbol, code:q.symbol, sec:"", market:"US",
          price:q.price, change:q.change, changePct:q.changePct, volume:q.volume, high52w:q.high52w, low52w:q.low52w });
        if(q.price) { newLivePrices[q.symbol] = { price:q.price, at:Date.now() }; updateCount++; }
        if((q.changePct||-999) > topChange) { topChange=q.changePct; topStock=`${q.name||q.symbol} ${fmtChg(q.changePct)}`; }
      });
      debugLog.push(`종목 ${updateCount}개 업데이트 (한국 ${krData?.quotes?.length||0} + 미국 ${quoteData?.quotes?.length||0})`);

      const brief = {
        kospi: m.kospi?.price ? `${fmt(m.kospi?.price, 2)} ${fmtChg(m.kospi?.changePct)}` : "데이터 없음",
        krw: m.usdkrw?.price ? `${fmt(m.usdkrw?.price)}원 ${fmtChg(m.usdkrw?.changePct)}` : "—",
        nasdaq: m.nasdaq?.price ? `${fmt(m.nasdaq?.price)} ${fmtChg(m.nasdaq?.changePct)}` : "—",
        vix: m.vix?.price ? `VIX ${fmt(m.vix?.price)} (${fmtChg(m.vix?.changePct)})` : "—",
        gold: m.gold?.price ? `금 $${fmt(m.gold?.price)} ${fmtChg(m.gold?.changePct)}` : "—",
        btc: m.btc?.price ? `BTC $${fmt(m.btc?.price, 0)} ${fmtChg(m.btc?.changePct)}` : "—",
        headline,
        summary: m.sp500?.price
          ? `미국장 ${usUp?"상승":"하락"} 흐름 (S&P ${fmtChg(m.sp500?.changePct)}, 나스닥 ${fmtChg(m.nasdaq?.changePct)}). 원달러 ${fmt(m.usdkrw?.price)}원, 금 $${fmt(m.gold?.price)}.`
          : "시세 데이터를 가져오지 못했어. 잠시 후 다시 시도해줘.",
        topStock,
        risk: m.vix?.price ? (m.vix.price > 25 ? `VIX ${fmt(m.vix?.price,1)} 고변동성` : `VIX ${fmt(m.vix?.price,1)} 안정 구간`) : "VIX 데이터 없음 (무료 플랜)",
        method: "twelvedata",
        fetchedAt: Date.now(),
      };

      setAiBrief(brief);
      setLivePrice(newLivePrices);

      // 관심종목 실시간 저장 (오늘 탭 대시보드용)
      if(stocksList.length){
        const stocksObj = { items: stocksList, fetchedAt: Date.now() };
        setLiveStocks(stocksObj);
        try { localStorage.setItem("ct_live_stocks", JSON.stringify(stocksObj)); } catch {}
      }

      // 매크로 raw 저장 (스토랩스 탭 실시간 그리드용)
      if(marketOk && m && Object.keys(m).length){
        const macroObj = { ...m, fetchedAt: Date.now() };
        setLiveMacro(macroObj);
        try { localStorage.setItem("ct_live_macro", JSON.stringify(macroObj)); } catch {}
      }

      // 뉴스 저장
      if(newsData?.success && newsData.news?.length > 0) {
        const newsObj = { items: newsData.news, fetchedAt: Date.now() };
        setLiveNews(newsObj);
        try { localStorage.setItem("ct_live_news", JSON.stringify(newsObj)); } catch {}
        debugLog.push(`뉴스 ${newsData.news.length}건 갱신`);
      }

      try {
        localStorage.setItem("ct_ai_brief", JSON.stringify(brief));
        localStorage.setItem("ct_live_price", JSON.stringify(newLivePrices));
      } catch {}

      setAiDebug({ method:"real_yahoo", raw: debugLog.join("\n") });
      setToast(`✅ ${updateCount}개 종목 + ${newsData?.news?.length||0}건 뉴스 갱신`);
      setTimeout(()=>setToast(null), 3500);
      refreshNow();
    } catch(e) {
      console.error("백엔드 호출 실패:", e);
      debugLog.push(`최종 에러: ${e.message}`);
      setAiError(e.message || "갱신 실패");
      setAiDebug({ method:"backend_error", raw: debugLog.join("\n") + "\n\n" + (e.stack || "") });
      setToast(`⚠ ${e.message?.slice(0,60)}`);
      setTimeout(()=>setToast(null), 4500);
    } finally {
      setAiLoading(false);
    }
  };

  // 🔄 앱 열 때 자동 1회 호출 + 5분마다 자동 갱신
  useEffect(()=>{
    const lastFetch = aiBrief?.fetchedAt || 0;
    const since = Date.now() - lastFetch;
    if(since > 5*60*1000) {
      // 5분 넘었으면 자동 호출
      fetchAiBrief();
    }
    const t = setInterval(()=>{
      fetchAiBrief();
    }, 5*60*1000); // 5분마다
    return () => clearInterval(t);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[]);



  // 5분마다 외부 확인 배너 표시
  useEffect(()=>{
    const checkBanner = () => {
      const since = Date.now() - lastRefresh;
      if(since > 5*60*1000) setShowRefreshBanner(true); // 5분 초과
      else setShowRefreshBanner(false);
    };
    checkBanner();
    const t = setInterval(checkBanner, 30000); // 30초마다 체크
    return () => clearInterval(t);
  },[lastRefresh]);

  // 새로고침 시각 저장
  const refreshNow = () => {
    const now = Date.now();
    setLastRefresh(now);
    try { localStorage.setItem("ct_last_refresh", String(now)); } catch {}
    setShowRefreshBanner(false);
    setToast("🔄 갱신 시각 기록됨. 외부에서 확인한 가격을 입력해줘");
    setTimeout(()=>setToast(null), 3500);
  };

  // 사용자 입력 가격 적용
  const applyLivePrice = (ticker, price) => {
    const updated = {...livePrice, [ticker]:{price:parseFloat(price), at:Date.now()}};
    setLivePrice(updated);
    try { localStorage.setItem("ct_live_price", JSON.stringify(updated)); } catch {}
    setToast(`✅ ${ticker} 현재가 $${price} 반영됨`);
    setTimeout(()=>setToast(null), 3000);
    refreshNow();
  };

  // "N분 전" 포맷
  const timeAgo = ts => {
    const diff = Math.floor((Date.now()-ts)/1000);
    if(diff < 60) return `${diff}초 전`;
    if(diff < 3600) return `${Math.floor(diff/60)}분 전`;
    if(diff < 86400) return `${Math.floor(diff/3600)}시간 전`;
    return `${Math.floor(diff/86400)}일 전`;
  };

  useEffect(()=>{ const t=setInterval(()=>setTime(new Date()),1000); return()=>clearInterval(t); },[]);

  const closeBrief = () => {
    setShowBrief(false);
    try { localStorage.setItem("ct_seen_v2",TODAY_BRIEF.id); } catch {}
  };

  const naverUrl = code => `https://m.stock.naver.com/domestic/stock/${code}/total`;

  const TABS = [
    {id:"today",l:"🌅 오늘"},
    {id:"signals",l:"🎯 매매타이밍"},
    {id:"stoplaps",l:"📊 스토랩스"},
    {id:"news",l:"📰 뉴스 TOP10"},
    {id:"watch",l:"⭐ 종목"},
  ];

  return (
    <div style={{fontFamily:KR,background:C.bg,minHeight:"100vh",color:C.ink}}>
      <style>{`*{box-sizing:border-box}::-webkit-scrollbar{display:none}button:active{opacity:.7}@keyframes slideDown{from{transform:translateY(-100%);opacity:0}to{transform:translateY(0);opacity:1}}@keyframes slideUp{from{transform:translateY(20px);opacity:0}to{transform:translateY(0);opacity:1}}`}</style>

      {/* 🍞 토스트 알림 */}
      {toast && (
        <div style={{position:"fixed",bottom:24,left:"50%",transform:"translateX(-50%)",background:C.coral,color:"#fff",padding:"12px 20px",borderRadius:24,fontSize:13,fontWeight:700,zIndex:10000,boxShadow:"0 8px 24px rgba(0,0,0,0.4)",animation:"slideUp .3s",letterSpacing:"-0.2px",maxWidth:"90vw",textAlign:"center"}}>
          {toast}
        </div>
      )}

      {/* 🔔 5분 초과 갱신 배너 (자동) */}
      {showRefreshBanner && !showBrief && (
        <div style={{background:`${C.amber}25`,borderBottom:`1px solid ${C.amber}60`,padding:"10px 14px",display:"flex",alignItems:"center",gap:10,animation:"slideDown .3s",position:"sticky",top:60,zIndex:150}}>
          <span style={{fontSize:16}}>⏰</span>
          <div style={{flex:1,minWidth:0}}>
            <div style={{fontSize:11.5,fontWeight:700,color:C.amber,letterSpacing:"-0.2px"}}>외부에서 확인할 시간이야</div>
            <div style={{fontSize:10,color:C.inkMute,marginTop:1}}>마지막 갱신 {timeAgo(lastRefresh)} · 네이버에서 실시간 가격 확인하고 와</div>
          </div>
          <button onClick={()=>setShowRefreshBanner(false)} style={{background:"transparent",border:"none",color:C.inkSubtle,fontSize:14,cursor:"pointer",padding:4}}>✕</button>
        </div>
      )}

      {showBrief && (
        <div style={{position:"fixed",inset:0,background:"rgba(0,0,0,.85)",zIndex:9999,display:"flex",alignItems:"flex-end"}} onClick={closeBrief}>
          <div style={{background:C.bg,borderRadius:"20px 20px 0 0",width:"100%",maxHeight:"92vh",overflow:"auto",border:`1px solid ${C.coral}40`}} onClick={e=>e.stopPropagation()}>
            <div style={{padding:"18px 18px 12px",borderBottom:`1px solid ${C.border}`,display:"flex",alignItems:"center",gap:10,position:"sticky",top:0,background:C.bg,zIndex:2}}>
              <span style={{fontSize:24}}>🌅</span>
              <div style={{flex:1}}>
                <div style={{fontSize:11,color:C.coral,fontWeight:700}}>{TODAY_BRIEF.date} · 자동 아침 브리핑</div>
                <div style={{fontSize:15,fontWeight:800,color:C.ink,marginTop:2,letterSpacing:"-0.4px"}}>좋은 아침이야 동하야 ☀</div>
              </div>
              <button onClick={closeBrief} style={{background:C.surface,border:`1px solid ${C.border}`,color:C.inkMute,fontSize:18,width:32,height:32,borderRadius:16,cursor:"pointer"}}>✕</button>
            </div>
            <div style={{padding:"14px 18px"}}>
              <div style={{background:`linear-gradient(135deg,${C.coral}20,${C.surface})`,border:`1px solid ${C.coral}40`,borderRadius:12,padding:"14px 16px",marginBottom:14}}>
                <div style={{fontSize:14,fontWeight:800,color:C.coral,lineHeight:1.4,marginBottom:8,letterSpacing:"-0.3px"}}>{TODAY_BRIEF.headline}</div>
                <div style={{fontSize:12,color:C.ink,lineHeight:1.65,letterSpacing:"-0.2px"}}>{TODAY_BRIEF.oneLiner}</div>
              </div>

              <div style={{background:C.surface,borderRadius:12,padding:"14px 16px",marginBottom:14}}>
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:10}}>
                  <span style={{fontSize:12,color:C.inkMute,fontWeight:600}}>📊 시장 심리</span>
                  <span style={{fontFamily:MO,fontSize:22,fontWeight:800,color:C.green}}>{TODAY_BRIEF.sentiment}<span style={{fontSize:11,color:C.inkSubtle}}>/100</span></span>
                </div>
                <div style={{height:10,background:C.bg,borderRadius:5,overflow:"hidden",position:"relative"}}>
                  <div style={{width:"100%",height:"100%",background:`linear-gradient(90deg,${C.red},${C.amber},${C.green})`,opacity:.3}}/>
                  <div style={{position:"absolute",top:0,left:`${TODAY_BRIEF.sentiment}%`,width:3,height:10,background:"#fff",transform:"translateX(-1.5px)"}}/>
                </div>
                <div style={{textAlign:"center",fontSize:11,color:C.coral,marginTop:8,fontWeight:600}}>"{TODAY_BRIEF.sentimentLabel}"</div>
              </div>

              <div style={{fontSize:12,color:C.inkMute,fontWeight:700,marginBottom:8}}>🌙 간밤 핵심 숫자</div>
              <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:6,marginBottom:14}}>
                {TODAY_BRIEF.overnight.map((o,i)=>(
                  <div key={i} style={{background:C.surface,borderRadius:8,padding:"8px 10px"}}>
                    <div style={{fontSize:9,color:C.inkSubtle}}>{o.k}</div>
                    <div style={{fontFamily:MO,fontSize:12,fontWeight:700,color:C.ink}}>{o.v}</div>
                    <div style={{fontSize:9,color:o.up?C.green:C.red,marginTop:1}}>{o.c}</div>
                  </div>
                ))}
              </div>

              <div style={{fontSize:12,color:C.inkMute,fontWeight:700,marginBottom:8}}>⚠ 시간외 충격</div>
              <div style={{marginBottom:14}}>
                {TODAY_BRIEF.afterHours.map((a,i)=>(
                  <div key={i} style={{display:"flex",gap:8,padding:"8px 10px",background:a.c<0?`${C.red}15`:`${C.green}15`,border:`1px solid ${a.c<0?C.red:C.green}40`,borderRadius:8,marginBottom:5}}>
                    <span style={{minWidth:75,fontSize:11,fontWeight:700,color:C.ink}}>{a.t}</span>
                    <span style={{minWidth:48,fontFamily:MO,fontSize:11,fontWeight:700,color:a.c<0?C.red:C.green}}>{a.c>0?"+":""}{a.c}%</span>
                    <span style={{flex:1,fontSize:10,color:C.inkMute,lineHeight:1.4}}>{a.r}</span>
                  </div>
                ))}
              </div>

              <div style={{fontSize:12,color:C.inkMute,fontWeight:700,marginBottom:8}}>🎯 5대 지배 테마</div>
              <div style={{marginBottom:14}}>
                {TODAY_BRIEF.themes.map((th,i)=>(
                  <div key={i} style={{display:"flex",gap:10,padding:"10px 12px",background:C.surface,borderRadius:8,marginBottom:6,borderLeft:`3px solid ${C.coral}`}}>
                    <span style={{fontSize:20}}>{th.icon}</span>
                    <div style={{flex:1}}>
                      <div style={{fontSize:12,fontWeight:700,color:C.ink,marginBottom:2}}>{th.title}</div>
                      <div style={{fontSize:11,color:C.inkMute,lineHeight:1.5}}>{th.desc}</div>
                    </div>
                  </div>
                ))}
              </div>

              <div style={{fontSize:12,color:C.inkMute,fontWeight:700,marginBottom:8}}>📅 오늘 일정</div>
              <div style={{marginBottom:14}}>
                {TODAY_BRIEF.catalysts.map((c,i)=>{const col=c.imp==="critical"?C.red:c.imp==="high"?C.amber:C.blue;return(
                  <div key={i} style={{display:"flex",gap:10,alignItems:"center",padding:"8px 10px",background:C.surface,borderRadius:8,marginBottom:5,borderLeft:`3px solid ${col}`}}>
                    <span style={{minWidth:48,fontFamily:MO,fontSize:11,fontWeight:700,color:col}}>{c.t}</span>
                    <span style={{flex:1,fontSize:11,color:C.ink}}>{c.e}</span>
                  </div>
                );})}
              </div>

              <div style={{background:`${C.blue}15`,border:`1px solid ${C.blue}40`,borderRadius:12,padding:"14px 16px",marginBottom:14}}>
                <div style={{fontSize:12,color:C.coral,fontWeight:700,marginBottom:10}}>💡 오늘의 결론</div>
                <div style={{fontSize:11,color:C.ink,lineHeight:1.7,marginBottom:6}}><b style={{color:C.green}}>✅ 베스트:</b> {TODAY_BRIEF.conclusion.best}</div>
                <div style={{fontSize:11,color:C.ink,lineHeight:1.7,marginBottom:6}}><b style={{color:C.red}}>⚠ 함정:</b> {TODAY_BRIEF.conclusion.trap}</div>
                <div style={{fontSize:11,color:C.ink,lineHeight:1.7,marginBottom:8}}><b style={{color:C.coral}}>💰 현금:</b> {TODAY_BRIEF.conclusion.cash}</div>
                <div style={{fontSize:11,color:C.ink,lineHeight:1.7,padding:10,background:C.bg,borderRadius:8,marginTop:8}}>{TODAY_BRIEF.conclusion.msg}</div>
              </div>

              <div style={{textAlign:"center",fontSize:10,color:C.inkSubtle,padding:"6px 0",marginBottom:8,lineHeight:1.5}}>⚠ 컨센서스·뉴스 사실 기반 정보. 매매 추천 아니야.</div>
              <button onClick={closeBrief} style={{width:"100%",background:C.coral,border:"none",color:"#fff",fontFamily:KR,fontSize:14,fontWeight:700,padding:14,borderRadius:10,cursor:"pointer"}}>📊 앱 시작하기 →</button>
            </div>
          </div>
        </div>
      )}

      <div style={{background:C.surface,borderBottom:`1px solid ${C.border}`,padding:"12px 16px",display:"flex",alignItems:"center",justifyContent:"space-between",position:"sticky",top:0,zIndex:200,gap:8}}>
        <div style={{display:"flex",alignItems:"center",gap:10,minWidth:0,flex:1}}>
          <div style={{width:32,height:32,borderRadius:8,background:`linear-gradient(135deg,${C.coral},${C.coralDark})`,display:"flex",alignItems:"center",justifyContent:"center",fontSize:16}}>✦</div>
          <div style={{minWidth:0}}>
            <div style={{fontSize:15,fontWeight:800,letterSpacing:"-0.5px"}}>Claude Trade <span style={{color:C.coral}}>MAX</span></div>
            <div style={{fontSize:10.5,color:C.inkSubtle,marginTop:1}}>{time.toLocaleTimeString("ko-KR",{hour12:false})} · {time.toLocaleDateString("ko-KR",{month:"long",day:"numeric",weekday:"short"})}</div>
          </div>
        </div>
        <div style={{display:"flex",gap:6,alignItems:"center"}}>
          <button onClick={refreshNow} style={{background:C.surface,border:`1px solid ${C.border}`,color:C.inkMute,fontSize:11,padding:"6px 9px",borderRadius:14,cursor:"pointer",fontWeight:700,fontFamily:KR,display:"flex",alignItems:"center",gap:4}}>
            <span style={{fontSize:12}}>🔄</span>
            <span style={{fontSize:9.5,color:C.inkSubtle}}>{timeAgo(lastRefresh)}</span>
          </button>
        </div>
      </div>

      <div style={{background:C.surface,borderBottom:`1px solid ${C.border}`,display:"flex",overflowX:"auto",padding:"0 8px"}}>
        {TABS.map(t=>(
          <button key={t.id} onClick={()=>setTab(t.id)} style={{background:"none",border:"none",fontFamily:KR,fontSize:13,fontWeight:tab===t.id?700:500,color:tab===t.id?C.coral:C.inkMute,padding:"12px 14px",cursor:"pointer",borderBottom:`2px solid ${tab===t.id?C.coral:"transparent"}`,whiteSpace:"nowrap",letterSpacing:"-0.3px"}}>{t.l}</button>
        ))}
      </div>

      <div style={{padding:"14px 14px 60px"}}>
        {tab==="today" && (
          <>
            {/* 🤖 AI 실시간 브리핑 (Claude API + 웹검색) */}
            <div style={{background:aiBrief?`linear-gradient(135deg,${C.green}25,${C.surface})`:C.surface,border:`2px solid ${aiBrief?C.green+"60":C.border}`,borderRadius:14,padding:"14px 16px",marginBottom:12}}>
              <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:10}}>
                <span style={{fontSize:18}}>🤖</span>
                <div style={{flex:1,minWidth:0}}>
                  <div style={{fontSize:13,fontWeight:800,letterSpacing:"-0.3px"}}>AI 실시간 시장 브리핑</div>
                  <div style={{fontSize:10,color:C.inkSubtle,marginTop:1}}>{aiBrief?`✅ 마지막 갱신 ${timeAgo(aiBrief.fetchedAt)}`:"한 번도 갱신 안 됨"}</div>
                </div>
                <button onClick={fetchAiBrief} disabled={aiLoading} style={{background:aiLoading?C.surfaceLight:C.green,border:"none",color:"#fff",fontFamily:KR,fontSize:11,fontWeight:700,padding:"8px 14px",borderRadius:10,cursor:aiLoading?"wait":"pointer",letterSpacing:"-0.2px",opacity:aiLoading?0.6:1}}>
                  {aiLoading?"🔄 검색 중...":"🔄 갱신"}
                </button>
              </div>

              {aiError && (
                <div style={{background:`${C.red}15`,border:`1px solid ${C.red}40`,borderRadius:8,padding:"10px 12px",fontSize:11,color:C.red,marginBottom:8}}>
                  ⚠ {aiError}<br/>
                  <span style={{fontSize:10,color:C.inkMute}}>네트워크 또는 API 한도 문제일 수 있어. 잠시 후 다시 시도해줘.</span>
                  {aiDebug && (
                    <>
                      <button onClick={()=>setShowDebug(!showDebug)} style={{display:"block",marginTop:8,background:"transparent",border:`1px solid ${C.red}40`,color:C.red,fontSize:10,padding:"4px 8px",borderRadius:6,cursor:"pointer",fontFamily:KR}}>{showDebug?"▲ 디버그 닫기":"▼ 디버그 보기 (응답 원본)"}</button>
                      {showDebug && (
                        <pre style={{marginTop:8,padding:10,background:C.bg,borderRadius:6,fontSize:9,fontFamily:MO,color:C.inkMute,whiteSpace:"pre-wrap",wordBreak:"break-all",maxHeight:240,overflow:"auto"}}>{aiDebug.method ? `[방법: ${aiDebug.method}]\n\n` : ""}{aiDebug.raw}</pre>
                      )}
                    </>
                  )}
                </div>
              )}

              {aiBrief ? (
                <div>
                  <div style={{background:C.bg,borderRadius:10,padding:"12px 14px",marginBottom:8}}>
                    <div style={{fontSize:13.5,fontWeight:800,color:C.green,lineHeight:1.5,marginBottom:8,letterSpacing:"-0.3px"}}>{aiBrief.headline}</div>
                    <div style={{fontSize:11.5,color:C.ink,lineHeight:1.65}}>{aiBrief.summary}</div>
                  </div>
                  <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:6,marginBottom:8}}>
                    <div style={{background:C.bg,borderRadius:8,padding:"8px 10px"}}>
                      <div style={{fontSize:9,color:C.inkSubtle,marginBottom:2}}>나스닥(QQQ)</div>
                      <div style={{fontSize:12,fontWeight:700,letterSpacing:"-0.2px"}}>{aiBrief.nasdaq}</div>
                    </div>
                    <div style={{background:C.bg,borderRadius:8,padding:"8px 10px"}}>
                      <div style={{fontSize:9,color:C.inkSubtle,marginBottom:2}}>원/달러</div>
                      <div style={{fontSize:12,fontWeight:700,letterSpacing:"-0.2px"}}>{aiBrief.krw}</div>
                    </div>
                  </div>
                  <div style={{background:`${C.coral}10`,borderLeft:`3px solid ${C.coral}`,borderRadius:6,padding:"10px 12px",fontSize:11,lineHeight:1.5,marginBottom:6}}>
                    <span style={{color:C.coral,fontWeight:700}}>📌 주목 종목: </span>{aiBrief.topStock}
                  </div>
                  <div style={{background:`${C.red}10`,borderLeft:`3px solid ${C.red}`,borderRadius:6,padding:"10px 12px",fontSize:11,lineHeight:1.5}}>
                    <span style={{color:C.red,fontWeight:700}}>⚠ 리스크: </span>{aiBrief.risk}
                  </div>
                </div>
              ) : (
                <div style={{textAlign:"center",padding:"16px 12px",fontSize:12,color:C.inkMute,lineHeight:1.6}}>
                  🔄 갱신 버튼을 누르면 Claude AI가<br/>웹 검색으로 진짜 최신 시장 정보를 가져와.
                </div>
              )}
                  <div style={{textAlign:"center",fontSize:9.5,color:C.inkSubtle,marginTop:10,lineHeight:1.5}}>{aiBrief?.method==="web_search" ? "🌐 Claude가 실제 웹 검색으로 가져온 정보야" : "🤖 Claude가 분석해서 작성한 정보야 (웹검색 미사용)"}</div>
            </div>

            {/* 💼 내 보유종목 (실시간 수익률) */}
            {(()=>{
              const fx = liveMacro?.usdkrw?.price || BUY_FX;
              const find = (sym)=> liveStocks?.items?.find(s=>s.code===sym && s.market==="US");
              let totalCost=0, totalVal=0, hasData=false;
              const rows = HOLDINGS.map(h=>{
                const q=find(h.sym);
                const shares=h.krAmount/(h.buyUsd*BUY_FX);
                const curUsd=q?.price ?? null;
                const curVal=curUsd!=null ? shares*curUsd*fx : null;
                totalCost+=h.krAmount;
                if(curVal!=null){ totalVal+=curVal; hasData=true; }
                const pnlPct=curVal!=null ? (curVal/h.krAmount-1)*100 : null;
                const pnl=curVal!=null ? curVal-h.krAmount : null;
                return {h,q,curUsd,curVal,pnl,pnlPct,shares};
              });
              const totalPnl=hasData ? totalVal-totalCost : null;
              const totalPct=hasData ? (totalVal/totalCost-1)*100 : null;
              const tup=(totalPct||0)>=0;
              return (
                <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:14,marginBottom:12,overflow:"hidden"}}>
                  <div style={{padding:"12px 16px",borderBottom:`1px solid ${C.border}`,display:"flex",justifyContent:"space-between",alignItems:"center"}}>
                    <span style={{fontSize:14,fontWeight:700,letterSpacing:"-0.3px"}}>💼 내 보유종목</span>
                    {liveStocks?.fetchedAt && <span style={{fontSize:9.5,color:C.inkSubtle}}>{timeAgo(liveStocks.fetchedAt)}</span>}
                  </div>
                  {/* 총 평가손익 */}
                  <div style={{padding:"14px 16px",borderBottom:`1px solid ${C.border}`,background:C.bg}}>
                    <div style={{fontSize:10.5,color:C.inkMute,marginBottom:4}}>총 평가손익 (원금 ₩{FMT(Math.round(totalCost))})</div>
                    {hasData ? (
                      <div style={{display:"flex",alignItems:"baseline",gap:8}}>
                        <span style={{fontFamily:MO,fontSize:22,fontWeight:800,color:tup?C.red:C.blue}}>{tup?"+":""}{FMT(Math.round(totalPnl))}원</span>
                        <span style={{fontFamily:MO,fontSize:13,fontWeight:700,color:tup?C.red:C.blue}}>({tup?"+":""}{totalPct.toFixed(2)}%)</span>
                      </div>
                    ) : <div style={{fontSize:12,color:C.inkMute}}>🔄 갱신하면 실시간 평가</div>}
                  </div>
                  {rows.map((r,i)=>{
                    const up=(r.pnlPct||0)>=0;
                    const col=up?C.red:C.blue;
                    return (
                      <div key={i} style={{padding:"12px 16px",borderBottom:i<rows.length-1?`1px solid ${C.border}`:"none"}}>
                        <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:6}}>
                          <div style={{flex:1,minWidth:0}}>
                            <div style={{fontSize:13,fontWeight:700,letterSpacing:"-0.3px"}}>{r.h.name} <span style={{fontSize:9,color:C.inkSubtle,fontWeight:500}}>🇺🇸 {r.h.sec}</span></div>
                            <div style={{fontSize:9.5,color:C.inkSubtle,fontFamily:MO,marginTop:1}}>{r.shares.toFixed(2)}주 · 매수 ${r.h.buyUsd} → 현재 {r.curUsd!=null?`$${r.curUsd}`:"—"}</div>
                          </div>
                          <div style={{textAlign:"right"}}>
                            <div style={{fontFamily:MO,fontSize:13,fontWeight:700}}>{r.curVal!=null?`₩${FMT(Math.round(r.curVal))}`:"—"}</div>
                            <div style={{fontFamily:MO,fontSize:11,fontWeight:700,color:col,marginTop:1}}>{r.pnlPct!=null?`${up?"▲":"▼"} ${Math.abs(r.pnlPct).toFixed(2)}%`:"—"}</div>
                          </div>
                        </div>
                        {/* 목표 참고선 (52주 고/저) */}
                        {r.q?.low52w && r.q?.high52w && (
                          <div style={{display:"flex",gap:6,fontSize:9.5,fontFamily:MO}}>
                            <span style={{flex:1,color:C.blue,background:`${C.blue}12`,borderRadius:6,padding:"4px 8px"}}>📉 참고매수 ${r.q.low52w} <span style={{color:C.inkSubtle}}>(52주저)</span></span>
                            <span style={{flex:1,color:C.red,background:`${C.red}12`,borderRadius:6,padding:"4px 8px",textAlign:"right"}}>참고매도 ${r.q.high52w} <span style={{color:C.inkSubtle}}>(52주고)</span> 📈</span>
                          </div>
                        )}
                      </div>
                    );
                  })}
                  <div style={{padding:"8px 16px 10px",fontSize:9,color:C.inkSubtle,lineHeight:1.5}}>
                    ※ 매수단가는 5/21 미국 종가 추정 · 환율 {Math.round(fx)}원 적용 · 참고선은 52주 고저(분석용, 추천 아님)
                  </div>
                </div>
              );
            })()}

            {/* ⭐ 관심종목 (추천 미국주 + 한국주) */}
            {(()=>{
              const watchUsItems = WATCH_US.map(w=>{
                const q=liveStocks?.items?.find(s=>s.code===w.sym && s.market==="US");
                return q ? {...q, name:w.name, sec:w.sec} : null;
              }).filter(Boolean);
              const krItems = liveStocks?.items?.filter(s=>s.market==="KR") || [];
              const all=[...watchUsItems, ...krItems];
              return (
                <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:14,marginBottom:12,overflow:"hidden"}}>
                  <div style={{padding:"12px 16px",borderBottom:`1px solid ${C.border}`,fontSize:14,fontWeight:700,letterSpacing:"-0.3px"}}>⭐ 관심종목</div>
                  {all.length ? all.map((s,i)=>{
                    const up=(s.changePct||0)>=0; const col=up?C.red:C.blue;
                    return (
                      <div key={i} style={{display:"flex",alignItems:"center",gap:10,padding:"10px 16px",borderBottom:i<all.length-1?`1px solid ${C.border}`:"none"}}>
                        <div style={{flex:1,minWidth:0}}>
                          <div style={{fontSize:13,fontWeight:700,letterSpacing:"-0.3px"}}>{s.name} <span style={{fontSize:9,color:C.inkSubtle,fontWeight:500}}>{s.market==="US"?"🇺🇸":"🇰🇷"} {s.sec}</span></div>
                          <div style={{fontSize:9.5,color:C.inkSubtle,fontFamily:MO,marginTop:1}}>거래량 {FMT(s.volume)}</div>
                        </div>
                        <div style={{textAlign:"right"}}>
                          <div style={{fontFamily:MO,fontSize:13,fontWeight:700}}>{s.market==="US"?"$":"₩"}{FMT(s.price)}</div>
                          <div style={{fontFamily:MO,fontSize:10.5,fontWeight:700,color:col,marginTop:1}}>{up?"▲":"▼"} {s.changePct==null?"—":Math.abs(s.changePct).toFixed(2)+"%"}</div>
                        </div>
                      </div>
                    );
                  }) : <div style={{padding:"20px 16px",textAlign:"center",fontSize:12,color:C.inkMute,lineHeight:1.6}}>🔄 갱신하면 실시간 시세가 떠</div>}
                </div>
              );
            })()}

            {/* 🌍 미국 시장 + 💱 환율·원자재 */}
            {liveMacro && (()=>{
              const fc=(v)=>v==null?"—":(v>=0?"+":"")+Number(v).toFixed(2)+"%";
              const f=(v,d=2)=>v==null?"—":Number(v).toLocaleString("ko-KR",{maximumFractionDigits:d});
              const cell=(label,obj,prefix="",sub)=>{
                const up=(obj?.changePct||0)>=0;
                return (
                  <div style={{background:C.bg,borderRadius:8,padding:"10px 10px"}}>
                    <div style={{fontSize:9.5,color:C.inkSubtle,marginBottom:3}}>{label}{sub?` (${sub})`:""}</div>
                    <div style={{fontFamily:MO,fontSize:13,fontWeight:700}}>{obj?.price==null?"—":prefix+f(obj.price)}</div>
                    <div style={{fontFamily:MO,fontSize:10,fontWeight:700,color:up?C.red:C.blue,marginTop:2}}>{fc(obj?.changePct)}</div>
                  </div>
                );
              };
              return (
                <>
                  <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:14,marginBottom:12,overflow:"hidden"}}>
                    <div style={{padding:"12px 16px",borderBottom:`1px solid ${C.border}`,fontSize:14,fontWeight:700,letterSpacing:"-0.3px"}}>🌍 미국 시장</div>
                    <div style={{padding:12,display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:6}}>
                      {cell("S&P500",liveMacro.sp500,"",liveMacro.sp500?.tracker)}
                      {cell("나스닥",liveMacro.nasdaq,"",liveMacro.nasdaq?.tracker)}
                      {cell("다우",liveMacro.dow,"",liveMacro.dow?.tracker)}
                    </div>
                    <div style={{padding:"0 14px 10px",fontSize:9,color:C.inkSubtle,lineHeight:1.5}}>※ 지수는 추종 ETF 가격 — 변동률은 실제 지수와 동일</div>
                  </div>

                  <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:14,marginBottom:12,overflow:"hidden"}}>
                    <div style={{padding:"12px 16px",borderBottom:`1px solid ${C.border}`,fontSize:14,fontWeight:700,letterSpacing:"-0.3px"}}>💱 환율 · 원자재</div>
                    <div style={{padding:12,display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:6}}>
                      {cell("원/달러",liveMacro.usdkrw,"₩")}
                      {cell("금",liveMacro.gold,"$")}
                      {cell("WTI유",liveMacro.wti,"$",liveMacro.wti?.tracker)}
                    </div>
                  </div>
                </>
              );
            })()}

            {/* 📚 초보 투자 원칙 */}
            <div style={{background:`linear-gradient(135deg,${C.coral}12,${C.surface})`,border:`1px solid ${C.coral}40`,borderRadius:14,padding:"14px 16px",marginBottom:12}}>
              <div style={{fontSize:13,fontWeight:800,color:C.coral,marginBottom:10,letterSpacing:"-0.3px"}}>📚 초보 투자 원칙</div>
              <div style={{fontSize:11.5,lineHeight:1.9,color:C.ink}}>
                ① <b>분할 매수</b> — 한 번에 몰빵 금지, 나눠서 진입<br/>
                ② <b>손절선 먼저</b> — 사기 전에 "얼마 빠지면 판다" 정하기<br/>
                ③ <b>분할 익절</b> — 목표 도달 시 일부라도 차익 실현<br/>
                ④ <b>현금 20~30%</b> — 기회는 또 오니까 실탄 남기기<br/>
                ⑤ <b>변동률(%) 먼저</b> — 가격보다 흐름을 봐
              </div>
              <div style={{marginTop:10,padding:"8px 10px",background:`${C.amber}15`,border:`1px solid ${C.amber}40`,borderRadius:8,fontSize:10.5,color:C.amber,lineHeight:1.5,fontWeight:600}}>
                ⚠ 이 앱은 분석 도구야 — 매매 추천이 아니야. 최종 판단·책임은 동하 본인.
              </div>
            </div>

          </>
        )}

        {tab==="signals" && (
          <>
            <div style={{background:`linear-gradient(135deg,${C.coral},${C.coralDark})`,borderRadius:14,padding:18,marginBottom:14,color:"#fff"}}>
              <div style={{fontSize:11,opacity:.85,marginBottom:2}}>2026.04.23 · 컨센서스 + 기술적 분석</div>
              <div style={{fontSize:18,fontWeight:800,letterSpacing:"-0.5px"}}>🎯 오늘의 매매 타이밍 5선</div>
              <div style={{fontSize:12,opacity:.95,lineHeight:1.6,marginTop:8}}>다수 증권사 컨센 + 기술적 지지/저항선 기반 <b>참고 가이드</b>야. 진입가·손절·익절 분할 명시.</div>
            </div>

            <div style={{background:`${C.amber}15`,border:`1px solid ${C.amber}40`,borderRadius:12,padding:"12px 14px",marginBottom:14,display:"flex",gap:10}}>
              <span style={{fontSize:18}}>⚠</span>
              <div style={{fontSize:12,lineHeight:1.6}}><b style={{color:C.amber}}>이건 추천이 아니야 — 참고 가이드야.</b> 시장은 본질적으로 불확실해. 손절선 꼭 지켜.</div>
            </div>

            {SIGNALS.map((s,idx)=>{
              const col = s.actCol==="green"?C.green:s.actCol==="amber"?C.amber:C.red;
              const isOpen = openSig===idx;
              return (
                <div key={idx} style={{background:C.surface,border:`1px solid ${isOpen?col+"60":C.border}`,borderRadius:12,marginBottom:12,overflow:"hidden"}}>
                  <div style={{padding:"14px 16px",cursor:"pointer",background:C.surfaceLight}} onClick={()=>setOpenSig(isOpen?null:idx)}>
                    <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:8}}>
                      <div style={{background:col,color:"#fff",fontSize:13,fontWeight:800,width:30,height:30,borderRadius:15,display:"flex",alignItems:"center",justifyContent:"center"}}>{idx+1}</div>
                      <div style={{flex:1,minWidth:0}}>
                        <div style={{fontSize:14,fontWeight:800,letterSpacing:"-0.3px"}}>{s.t} <span style={{fontFamily:MO,fontSize:11,color:C.inkSubtle,fontWeight:500,marginLeft:4}}>{s.code}</span></div>
                        <div style={{fontFamily:MO,fontSize:11,color:C.inkMute,marginTop:1}}>현재가 ₩{FMT(s.cur)}</div>
                      </div>
                      <div style={{textAlign:"right"}}>
                        <div style={{background:col,color:"#fff",fontSize:11,fontWeight:700,padding:"3px 9px",borderRadius:12}}>{s.action}</div>
                        <div style={{fontFamily:MO,fontSize:10,color:C.inkSubtle,marginTop:3}}>신뢰도 {s.conf}%</div>
                      </div>
                    </div>
                    <div style={{display:"flex",gap:8,padding:"8px 10px",background:C.bg,borderRadius:8,border:`1px solid ${C.border}`}}>
                      <span style={{fontSize:14}}>⏰</span>
                      <div style={{fontSize:11,lineHeight:1.5}}>{s.timing}</div>
                    </div>
                    <div style={{textAlign:"center",fontSize:10,color:C.inkSubtle,marginTop:8}}>{isOpen?"▲ 접기":"▼ 매수/매도 가격 자세히"}</div>
                  </div>

                  {isOpen && (
                    <div style={{padding:16,background:C.surface}}>
                      <div style={{marginBottom:14}}>
                        <div style={{fontSize:12,fontWeight:700,color:C.green,marginBottom:8}}>📥 매수 진입 (분할)</div>
                        {s.entry.map((e,i)=>(
                          <div key={i} style={{display:"flex",gap:10,padding:"10px 12px",background:`${C.green}10`,border:`1px solid ${C.green}30`,borderRadius:8,marginBottom:5}}>
                            <span style={{minWidth:90,fontSize:11,fontWeight:700}}>{e.l}</span>
                            <span style={{minWidth:100,fontFamily:MO,fontSize:13,fontWeight:700,color:C.green}}>₩{e.p}</span>
                            <span style={{flex:1,fontSize:10.5,color:C.inkMute,lineHeight:1.5}}>{e.r}</span>
                          </div>
                        ))}
                      </div>

                      <div style={{marginBottom:14}}>
                        <div style={{fontSize:12,fontWeight:700,color:C.coral,marginBottom:8}}>📤 익절 매도 (분할)</div>
                        {s.exit.map((e,i)=>(
                          <div key={i} style={{display:"flex",gap:10,padding:"10px 12px",background:`${C.coral}10`,border:`1px solid ${C.coral}30`,borderRadius:8,marginBottom:5}}>
                            <span style={{minWidth:90,fontSize:11,fontWeight:700}}>{e.l}</span>
                            <span style={{minWidth:100,fontFamily:MO,fontSize:13,fontWeight:700,color:C.coral}}>₩{e.p}</span>
                            <span style={{flex:1,fontSize:10.5,color:C.inkMute,lineHeight:1.5}}>{e.r}</span>
                          </div>
                        ))}
                      </div>

                      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8,marginBottom:14}}>
                        <div style={{padding:"10px 12px",background:`${C.red}10`,border:`1px solid ${C.red}30`,borderRadius:8}}>
                          <div style={{fontSize:10,color:C.red,fontWeight:700,marginBottom:4}}>🛑 손절선</div>
                          <div style={{fontFamily:MO,fontSize:13,fontWeight:700,color:C.red}}>{s.stop}</div>
                        </div>
                        <div style={{padding:"10px 12px",background:`${C.blue}10`,border:`1px solid ${C.blue}30`,borderRadius:8}}>
                          <div style={{fontSize:10,color:C.blue,fontWeight:700,marginBottom:4}}>⏳ 보유</div>
                          <div style={{fontSize:12,fontWeight:700}}>{s.hold}</div>
                        </div>
                      </div>

                      <div style={{padding:12,background:`${C.green}08`,borderLeft:`3px solid ${C.green}`,borderRadius:8,marginBottom:8}}>
                        <div style={{fontSize:11,fontWeight:700,color:C.green,marginBottom:4}}>✅ Bull Case</div>
                        <div style={{fontSize:11,lineHeight:1.6}}>{s.bull}</div>
                      </div>
                      <div style={{padding:12,background:`${C.red}08`,borderLeft:`3px solid ${C.red}`,borderRadius:8,marginBottom:14}}>
                        <div style={{fontSize:11,fontWeight:700,color:C.red,marginBottom:4}}>⚠ Bear Case</div>
                        <div style={{fontSize:11,lineHeight:1.6}}>{s.bear}</div>
                      </div>

                      <a href={naverUrl(s.code)} target="_blank" rel="noopener noreferrer" style={{textDecoration:"none",display:"block"}}>
                        <button style={{width:"100%",background:"#03C75A",border:"none",color:"#fff",fontFamily:KR,fontSize:13,fontWeight:700,padding:13,borderRadius:10,cursor:"pointer",display:"flex",alignItems:"center",justifyContent:"center",gap:8}}>
                          <span style={{width:20,height:20,borderRadius:10,background:"#fff",display:"flex",alignItems:"center",justifyContent:"center",fontSize:11,fontWeight:900,color:"#03C75A"}}>N</span>
                          네이버 금융에서 실시간 가격 →
                        </button>
                      </a>
                    </div>
                  )}
                </div>
              );
            })}

            <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,padding:"14px 16px",marginTop:6}}>
              <div style={{fontSize:12,fontWeight:700,color:C.coral,marginBottom:8}}>💭 동하야 꼭 기억해</div>
              <div style={{fontSize:11.5,lineHeight:1.7}}>
                ① <b>분할 매수가 핵심</b> — 몰빵 금지<br/>
                ② <b>손절선 무조건 지키기</b> — "조금만 더"가 가장 위험<br/>
                ③ <b>익절도 분할로</b> — 1차 도달 시 일부 차익실현<br/>
                ④ <b>현금 20-30% 유지</b> — 기회는 또 와
              </div>
            </div>
          </>
        )}

        {tab==="news" && (
          <>
            {/* 🔴 실시간 뉴스 (Yahoo Finance RSS 자동 갱신) */}
            {liveNews && liveNews.items && liveNews.items.length > 0 && (
              <div style={{background:`linear-gradient(135deg,${C.green}25,${C.surface})`,border:`2px solid ${C.green}60`,borderRadius:14,padding:14,marginBottom:14}}>
                <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:10}}>
                  <span style={{fontSize:18}}>🔴</span>
                  <div style={{flex:1}}>
                    <div style={{fontSize:13,fontWeight:800,letterSpacing:"-0.3px"}}>실시간 뉴스 (Yahoo Finance)</div>
                    <div style={{fontSize:10,color:C.inkSubtle,marginTop:1}}>마지막 갱신 {timeAgo(liveNews.fetchedAt)} · 5분마다 자동</div>
                  </div>
                </div>
                {liveNews.items.slice(0,10).map((n,i)=>(
                  <a key={i} href={n.link} target="_blank" rel="noopener noreferrer" style={{textDecoration:"none",display:"block",marginBottom:6}}>
                    <div style={{padding:"10px 12px",background:C.bg,borderRadius:8,borderLeft:`3px solid ${C.green}`}}>
                      <div style={{display:"flex",gap:6,marginBottom:4,fontSize:9.5,color:C.inkSubtle,alignItems:"center"}}>
                        <span style={{color:C.green,fontWeight:700}}>#{i+1}</span>
                        <span>·</span>
                        <span>{n.src}</span>
                        {n.date && <><span>·</span><span>{new Date(n.date).toLocaleDateString("ko-KR",{month:"2-digit",day:"2-digit"})}</span></>}
                      </div>
                      <div style={{fontSize:12,fontWeight:700,lineHeight:1.5,color:C.ink,letterSpacing:"-0.2px"}}>{n.title}</div>
                      {n.summary && <div style={{fontSize:10.5,color:C.inkMute,marginTop:4,lineHeight:1.5}}>{n.summary.slice(0,120)}...</div>}
                    </div>
                  </a>
                ))}
              </div>
            )}

            {(!liveNews || !liveNews.items?.length) && (
              <div style={{textAlign:"center",padding:"24px 16px",fontSize:12,color:C.inkMute,lineHeight:1.6}}>
                📰 상단 "🔄 갱신" 버튼을 누르면<br/>Yahoo Finance 실시간 뉴스를 가져와.
              </div>
            )}
          </>
        )}

        {tab==="stoplaps" && (() => {
          const s = STOCKS[slStock];
          const live = livePrice[slStock];
          // 🔄 사용자 입력 가격이 있으면 그걸 현재가로 사용 + 모든 레벨을 비례 재계산
          const liveCur = live?.price || s.cur;
          const ratio = liveCur / s.cur; // 비례 계수
          const lv = {
            target2: s.levels.target2 * ratio,
            target1: s.levels.target1 * ratio,
            center: s.levels.center * ratio,
            defense1: s.levels.defense1 * ratio,
            defense2: s.levels.defense2 * ratio,
            buyTarget2: s.levels.buyTarget2 * ratio,
            buyTarget1: s.levels.buyTarget1 * ratio,
            buyCenter: s.levels.buyCenter * ratio,
            buyDef1: s.levels.buyDef1 * ratio,
            buyDef2: s.levels.buyDef2 * ratio,
            sellTarget2: s.levels.sellTarget2 * ratio,
            sellTarget1: s.levels.sellTarget1 * ratio,
            sellCenter: s.levels.sellCenter * ratio,
            sellDef1: s.levels.sellDef1 * ratio,
            sellDef2: s.levels.sellDef2 * ratio,
            afterMarket: s.levels.afterMarket * ratio,
          };
          // 매수 진입가 = 기준가 × 1.003
          const buyEntries = {
            target2: lv.buyTarget2, target1: lv.buyTarget1, center: lv.buyCenter,
            defense1: lv.buyDef1, defense2: lv.buyDef2,
          };
          const sellTargets = {
            target2: lv.sellTarget2, target1: lv.sellTarget1, center: lv.sellCenter,
            defense1: lv.sellDef1, defense2: lv.sellDef2,
          };
          const baseLevels = {
            target2: lv.target2, target1: lv.target1, center: lv.center,
            defense1: lv.defense1, defense2: lv.defense2,
          };
          // 수량 계산: 시드 / (진입가 × 환율)
          const calcQty = price => Math.floor(slSeed / US2KRW(price));
          const buyQty = calcQty(buyEntries[slBuyLevel]);
          const buyTotal = buyQty * US2KRW(buyEntries[slBuyLevel]);
          // 예상 수익률: 매도 목표가 / 매수 진입가 - 1
          const expReturn = ((sellTargets[slSellLevel] / buyEntries[slBuyLevel]) - 1) * 100;
          const expProfit = Math.round(buyTotal * expReturn / 100);
          const aiBuyRec = s.aiRec.buy;
          const aiSellRec = s.aiRec.sell;

          return (
            <>
              {/* 헤더: 종목 선택 */}
              <div style={{background:`linear-gradient(135deg,${C.coral},${C.coralDark})`,borderRadius:14,padding:16,marginBottom:12,color:"#fff"}}>
                <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:6}}>
                  <span style={{fontSize:22}}>📈</span>
                  <div style={{fontSize:17,fontWeight:800,letterSpacing:"-0.5px"}}>스토랩스</div>
                </div>
                <div style={{fontSize:11,opacity:.92,lineHeight:1.5}}>스토캐스틱 + 다층 매수/매도 포지션 시뮬레이터</div>
              </div>

              {/* 종목 선택 + 라이브 가격 표시 */}
              <div style={{background:C.surface,border:`1.5px solid ${live ? C.green+"60" : C.border}`,borderRadius:12,padding:"14px 16px",marginBottom:8,display:"flex",alignItems:"center",gap:12}}>
                <span style={{fontSize:18}}>{s.flag}</span>
                <div style={{flex:1}}>
                  <div style={{fontSize:14,fontWeight:800,letterSpacing:"-0.3px"}}>{s.name} · {s.ticker}</div>
                  <div style={{fontSize:10.5,color:C.inkSubtle,marginTop:2}}>현재가 ${liveCur.toFixed(2)} · {s.change>0?"+":""}{s.change}%{live && <span style={{color:C.green,marginLeft:6}}>● LIVE</span>}</div>
                </div>
                <div style={{background:`${C.green}20`,color:C.green,fontSize:11,fontWeight:700,padding:"4px 10px",borderRadius:10}}>✓ 선택됨</div>
              </div>

              {/* 🔄 가격 직접 입력 (정직한 갱신) */}
              <div style={{background:`${C.green}10`,border:`1px solid ${C.green}40`,borderRadius:12,padding:"14px 16px",marginBottom:12}}>
                <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:8}}>
                  <span style={{fontSize:14}}>📡</span>
                  <span style={{fontSize:12,fontWeight:700,color:C.green,letterSpacing:"-0.2px"}}>실시간 가격 직접 입력</span>
                </div>
                <div style={{fontSize:10.5,color:C.inkMute,lineHeight:1.5,marginBottom:10}}>
                  네이버/Yahoo에서 본 현재가를 입력하면 모든 매수/매도 테이블이 비례 재계산돼.
                  {live && <><br/><span style={{color:C.green}}>● 마지막 입력: ${live.price} ({timeAgo(live.at)})</span></>}
                </div>
                <div style={{display:"flex",gap:6,marginBottom:8}}>
                  <a href={`https://finance.yahoo.com/quote/${s.ticker}`} target="_blank" rel="noopener noreferrer" style={{flex:1,textDecoration:"none"}}>
                    <button style={{width:"100%",background:"#5F01D1",border:"none",color:"#fff",fontFamily:KR,fontSize:11,fontWeight:700,padding:"9px",borderRadius:8,cursor:"pointer"}}>📊 Yahoo에서 보기</button>
                  </a>
                  <a href={`https://m.stock.naver.com/worldstock/stock/${s.ticker}.O/total`} target="_blank" rel="noopener noreferrer" style={{flex:1,textDecoration:"none"}}>
                    <button style={{width:"100%",background:"#03C75A",border:"none",color:"#fff",fontFamily:KR,fontSize:11,fontWeight:700,padding:"9px",borderRadius:8,cursor:"pointer"}}>📡 네이버에서 보기</button>
                  </a>
                </div>
                <div style={{display:"flex",gap:6}}>
                  <input type="text" value={priceInput} placeholder={`예: ${liveCur.toFixed(2)}`} onChange={e=>{const v=e.target.value.replace(/[^0-9.]/g,"");setPriceInput(v);}} style={{flex:1,background:C.bg,border:`1px solid ${C.border}`,color:C.ink,fontFamily:MO,fontSize:13,padding:"10px 12px",borderRadius:8,outline:"none"}}/>
                  <button onClick={()=>{if(priceInput && parseFloat(priceInput)>0){applyLivePrice(slStock,priceInput);setPriceInput("");}}} style={{background:C.green,border:"none",color:"#fff",fontFamily:KR,fontSize:12,fontWeight:700,padding:"10px 16px",borderRadius:8,cursor:"pointer",letterSpacing:"-0.2px"}}>적용</button>
                  {live && <button onClick={()=>{const u={...livePrice};delete u[slStock];setLivePrice(u);try{localStorage.setItem("ct_live_price",JSON.stringify(u));}catch{};setToast("초기화됨");setTimeout(()=>setToast(null),2000);}} style={{background:C.bg,border:`1px solid ${C.border}`,color:C.inkMute,fontFamily:KR,fontSize:11,padding:"10px 12px",borderRadius:8,cursor:"pointer"}}>↻</button>}
                </div>
              </div>

              {/* 매크로 6개 그리드 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,marginBottom:12,overflow:"hidden"}}>
                <div style={{padding:"12px 14px",borderBottom:`1px solid ${C.border}`,fontSize:13,fontWeight:700,letterSpacing:"-0.3px"}}>🌍 매크로 대시보드</div>
                <div style={{padding:12,display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:6}}>
                  {(()=>{
                    const f=(v,d=2)=>v==null?"—":Number(v).toLocaleString("ko-KR",{maximumFractionDigits:d});
                    const fc=(v)=>v==null?"":(v>=0?"+":"")+Number(v).toFixed(2)+"%";
                    const LM=liveMacro;
                    const rows = LM ? [
                      {k:"S&P500", sub:LM.sp500?.tracker, v:f(LM.sp500?.price), c:fc(LM.sp500?.changePct), up:(LM.sp500?.changePct||0)>=0},
                      {k:"나스닥",  sub:LM.nasdaq?.tracker, v:f(LM.nasdaq?.price), c:fc(LM.nasdaq?.changePct), up:(LM.nasdaq?.changePct||0)>=0},
                      {k:"USD/KRW", v:f(LM.usdkrw?.price)+"원", c:fc(LM.usdkrw?.changePct), up:(LM.usdkrw?.changePct||0)>=0, blue:true},
                      {k:"DXY",    sub:LM.dxy?.tracker, v:f(LM.dxy?.price), c:fc(LM.dxy?.changePct), up:(LM.dxy?.changePct||0)>=0},
                      {k:"WTI",    sub:LM.wti?.tracker, v:"$"+f(LM.wti?.price), c:fc(LM.wti?.changePct), up:(LM.wti?.changePct||0)>=0},
                      {k:"금",     v:"$"+f(LM.gold?.price), c:fc(LM.gold?.changePct), up:(LM.gold?.changePct||0)>=0},
                    ] : MACRO;
                    return rows.map((m,i)=>(
                      <div key={i} style={{background:C.bg,borderRadius:8,padding:"10px 8px"}}>
                        <div style={{fontSize:9,color:C.inkSubtle,marginBottom:4}}>{m.k}{m.sub?` (${m.sub})`:""}</div>
                        <div style={{fontFamily:MO,fontSize:13,fontWeight:700,letterSpacing:"-0.3px"}}>{m.v}</div>
                        <div style={{fontSize:9,color:m.blue?C.blue:m.up?C.red:C.blue,marginTop:2}}>{m.c}</div>
                      </div>
                    ));
                  })()}
                </div>
                {liveMacro && (
                  <div style={{padding:"0 14px 10px",fontSize:9,color:C.inkSubtle,lineHeight:1.5}}>
                    ※ 지수는 추종 ETF(SPY/QQQ/UUP/USO) 가격 — 변동률은 실제 지수와 동일
                  </div>
                )}
              </div>

              {/* 매수 시드 선택 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,marginBottom:12,overflow:"hidden"}}>
                <div style={{padding:"12px 14px",borderBottom:`1px solid ${C.border}`,fontSize:13,fontWeight:700,letterSpacing:"-0.3px"}}>💰 매수 시드</div>
                <div style={{padding:14}}>
                  <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:6,marginBottom:8}}>
                    {SEED_PRESETS.slice(0,3).map((p,i)=>(
                      <button key={i} onClick={()=>{setSlSeed(p.v);setSlSeedInput("");}} style={{background:slSeed===p.v?C.coral:C.bg,border:`1px solid ${slSeed===p.v?C.coral:C.border}`,color:slSeed===p.v?"#fff":C.ink,fontFamily:KR,fontSize:13,fontWeight:700,padding:"12px 8px",borderRadius:10,cursor:"pointer",letterSpacing:"-0.3px"}}>{p.l}</button>
                    ))}
                  </div>
                  <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:6,marginBottom:10}}>
                    {SEED_PRESETS.slice(3,5).map((p,i)=>(
                      <button key={i} onClick={()=>{setSlSeed(p.v);setSlSeedInput("");}} style={{background:slSeed===p.v?C.coral:C.bg,border:`1px solid ${slSeed===p.v?C.coral:C.border}`,color:slSeed===p.v?"#fff":C.ink,fontFamily:KR,fontSize:13,fontWeight:700,padding:"12px 8px",borderRadius:10,cursor:"pointer",letterSpacing:"-0.3px"}}>{p.l}</button>
                    ))}
                    <button onClick={()=>{setSlSeed(20000000);setSlSeedInput("");}} style={{background:C.bg,border:`1px solid ${C.border}`,color:C.inkMute,fontFamily:KR,fontSize:13,fontWeight:700,padding:"12px 8px",borderRadius:10,cursor:"pointer"}}>↻ 리셋</button>
                  </div>
                  <div style={{padding:"10px 12px",background:C.bg,borderRadius:8,fontSize:11,marginBottom:10}}>
                    <span style={{color:C.inkMute}}>선택 금액 </span>
                    <span style={{fontWeight:700,color:C.coral}}>{(slSeed/10000).toLocaleString()}만원 ({slSeed.toLocaleString()}원)</span>
                  </div>
                  <div style={{fontSize:11,color:C.inkMute,marginBottom:5}}>직접 입력 (원)</div>
                  <input type="text" value={slSeedInput} placeholder="예: 1,500,000 또는 150만" onChange={e=>{const v=e.target.value.replace(/[^0-9]/g,"");setSlSeedInput(v);if(v)setSlSeed(parseInt(v)||0);}} style={{width:"100%",background:C.bg,border:`1px solid ${C.border}`,color:C.ink,fontFamily:MO,fontSize:13,padding:"10px 12px",borderRadius:8,outline:"none"}}/>
                </div>
              </div>

              {/* 시그널 카드 1: 시장 추세 (스토캐스틱) */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,padding:"14px 16px",marginBottom:10}}>
                <div style={{fontSize:11,color:C.inkMute,marginBottom:6,fontWeight:600}}>📊 시장 추세</div>
                <div style={{display:"flex",alignItems:"baseline",gap:6,marginBottom:10}}>
                  <span style={{color:C.red,fontSize:14}}>↑</span>
                  <span style={{fontFamily:MO,fontSize:24,fontWeight:800,color:C.red}}>{s.stoch.market}</span>
                </div>
                <div style={{height:8,background:C.bg,borderRadius:4,overflow:"hidden",position:"relative",marginBottom:6}}>
                  <div style={{position:"absolute",left:0,top:0,bottom:0,width:"20%",background:C.blue+"60"}}/>
                  <div style={{position:"absolute",right:0,top:0,bottom:0,width:"20%",background:C.red+"60"}}/>
                  <div style={{position:"absolute",left:`${s.stoch.market}%`,top:-2,width:12,height:12,borderRadius:6,background:C.red,transform:"translateX(-6px)"}}/>
                </div>
                <div style={{display:"flex",justifyContent:"space-between",fontSize:9,color:C.inkSubtle}}>
                  <span>20</span><span>80</span>
                </div>
                <div style={{fontSize:10,color:C.inkSubtle,marginTop:6}}>%K {s.stoch.market} · %D {s.stoch.marketD}</div>
              </div>

              {/* 시그널 카드 2: 나스닥 주간 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,padding:"14px 16px",marginBottom:10}}>
                <div style={{fontSize:11,color:C.inkMute,marginBottom:6,fontWeight:600}}>나스닥 주간</div>
                <div style={{display:"flex",alignItems:"baseline",gap:6,marginBottom:10}}>
                  <span style={{color:C.red,fontSize:14}}>↑</span>
                  <span style={{fontFamily:MO,fontSize:24,fontWeight:800,color:C.red}}>{s.stoch.weekly}</span>
                </div>
                <div style={{height:8,background:C.bg,borderRadius:4,overflow:"hidden",position:"relative",marginBottom:6}}>
                  <div style={{position:"absolute",left:0,top:0,bottom:0,width:"20%",background:C.blue+"60"}}/>
                  <div style={{position:"absolute",right:0,top:0,bottom:0,width:"20%",background:C.red+"60"}}/>
                  <div style={{position:"absolute",left:`${Math.min(s.stoch.weekly,98)}%`,top:-2,width:12,height:12,borderRadius:6,background:C.red,transform:"translateX(-6px)"}}/>
                </div>
                <div style={{display:"flex",justifyContent:"space-between",fontSize:9,color:C.inkSubtle}}>
                  <span>20</span><span>80</span>
                </div>
                <div style={{fontSize:10,color:C.inkSubtle,marginTop:6}}>%K {s.stoch.weekly} · %D {s.stoch.weeklyD}</div>
              </div>

              {/* PP 회복 시그널 */}
              <div style={{background:`${C.blue}15`,border:`1px solid ${C.blue}40`,borderRadius:12,padding:"14px 16px",marginBottom:12}}>
                <div style={{fontSize:11,color:C.blue,fontWeight:700,marginBottom:6,letterSpacing:"-0.2px"}}>🤖 AI 시그널</div>
                <div style={{fontSize:12,lineHeight:1.6,marginBottom:6}}>{s.signals.ppRecover}</div>
                <div style={{fontSize:10.5,color:C.inkMute,lineHeight:1.5}}>{s.signals.stochSummary}</div>
              </div>

              {/* 핵심: 매수·매도 종합 카드 */}
              <div style={{background:C.surface,border:`2px solid ${C.coral}40`,borderRadius:14,padding:"16px",marginBottom:12}}>
                <div style={{fontSize:13,fontWeight:800,marginBottom:12,letterSpacing:"-0.3px",color:C.coral}}>지금 어디서 살까요? / 팔까요?</div>
                <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10}}>
                  <div style={{background:`${C.red}15`,border:`1px solid ${C.red}40`,borderRadius:10,padding:"12px"}}>
                    <div style={{fontSize:10,color:C.inkMute,marginBottom:4}}>매수 · {LEVEL_LABELS[slBuyLevel]} 🤖</div>
                    <div style={{fontFamily:MO,fontSize:22,fontWeight:800,color:C.red,letterSpacing:"-0.5px"}}>${buyEntries[slBuyLevel].toFixed(2)}</div>
                    <div style={{fontSize:9.5,color:C.inkSubtle,marginTop:3}}>진입가 (+0.3%)</div>
                  </div>
                  <div style={{background:`${C.blue}15`,border:`1px solid ${C.blue}40`,borderRadius:10,padding:"12px"}}>
                    <div style={{fontSize:10,color:C.inkMute,marginBottom:4}}>매도 · {LEVEL_LABELS[slSellLevel]} 🤖</div>
                    <div style={{fontFamily:MO,fontSize:22,fontWeight:800,color:C.blue,letterSpacing:"-0.5px"}}>${sellTargets[slSellLevel].toFixed(2)}</div>
                    <div style={{fontSize:9.5,color:C.inkSubtle,marginTop:3}}>목표가 (-0.3%)</div>
                  </div>
                </div>
                <div style={{height:1,background:C.border,margin:"14px 0"}}/>
                <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10}}>
                  <div>
                    <div style={{fontSize:10,color:C.inkMute,marginBottom:3}}>수량 / 총액</div>
                    <div style={{fontSize:18,fontWeight:800}}>{buyQty}주</div>
                    <div style={{fontSize:10,color:C.inkSubtle,marginTop:2}}>≈ {buyTotal.toLocaleString()}원</div>
                  </div>
                  <div>
                    <div style={{fontSize:10,color:C.inkMute,marginBottom:3}}>예상 수익률</div>
                    <div style={{fontSize:18,fontWeight:800,color:expReturn>=0?C.red:C.blue}}>{expReturn>=0?"+":""}{expReturn.toFixed(2)}%</div>
                    <div style={{fontSize:10,color:C.inkSubtle,marginTop:2}}>{expProfit>=0?"+":""}{Math.round(expProfit/10000)}만원</div>
                  </div>
                </div>
              </div>

              {/* 매수 테이블 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,marginBottom:12,overflow:"hidden"}}>
                <div style={{padding:"12px 14px",borderBottom:`1px solid ${C.border}`,display:"flex",alignItems:"center",gap:8}}>
                  <span style={{fontSize:14}}>📈</span>
                  <span style={{fontSize:13,fontWeight:700,color:C.red,letterSpacing:"-0.3px"}}>매수 테이블</span>
                  <span style={{background:C.bg,fontSize:9,color:C.inkSubtle,padding:"2px 7px",borderRadius:8}}>04/17 기준</span>
                  <span style={{flex:1}}/>
                  <span style={{fontSize:9,color:C.inkSubtle}}>×1.003</span>
                </div>
                <div style={{padding:8}}>
                  <div style={{display:"grid",gridTemplateColumns:"1.2fr 1fr 1fr 0.8fr",gap:6,padding:"8px 8px",fontSize:9.5,color:C.inkSubtle,fontWeight:600,borderBottom:`1px solid ${C.border}`}}>
                    <span>레벨</span><span>기준가</span><span>매수 진입가</span><span>수량</span>
                  </div>
                  {["target2","target1","center","defense1","defense2"].map(k=>{
                    const isAi = k===aiBuyRec;
                    const isSel = k===slBuyLevel;
                    const qty = calcQty(buyEntries[k]);
                    return (
                      <div key={k} onClick={()=>setSlBuyLevel(k)} style={{display:"grid",gridTemplateColumns:"1.2fr 1fr 1fr 0.8fr",gap:6,padding:"10px 8px",fontSize:11,alignItems:"center",cursor:"pointer",background:isSel?`${C.coral}20`:"transparent",borderRadius:6,marginTop:4,borderLeft:isAi?`3px solid ${C.coral}`:"3px solid transparent"}}>
                        <span style={{fontWeight:700}}>{LEVEL_LABELS[k]}{isAi&&<span style={{display:"block",fontSize:8.5,color:C.coral,marginTop:1}}>● AI 추천</span>}</span>
                        <span style={{fontFamily:MO}}>${baseLevels[k].toFixed(2)}</span>
                        <span style={{fontFamily:MO,fontWeight:700,color:C.red}}>${buyEntries[k].toFixed(2)}</span>
                        <span style={{fontFamily:MO,fontWeight:700}}>{qty}주</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* 매수 레벨 선택 토글 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,marginBottom:12,overflow:"hidden"}}>
                <div style={{padding:"10px 14px",fontSize:11,color:C.inkMute,fontWeight:600}}>매수 레벨 선택</div>
                <div style={{padding:"0 10px 10px",display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:6}}>
                  {["target2","target1","center"].map(k=>(
                    <button key={k} onClick={()=>setSlBuyLevel(k)} style={{padding:"10px 6px",background:slBuyLevel===k?C.coral:C.bg,border:`1px solid ${slBuyLevel===k?C.coral:C.border}`,color:slBuyLevel===k?"#fff":C.ink,fontFamily:KR,fontSize:11.5,fontWeight:700,borderRadius:8,cursor:"pointer",letterSpacing:"-0.2px"}}>{k===aiBuyRec?"🤖 ":""}{LEVEL_LABELS[k]}</button>
                  ))}
                </div>
                <div style={{padding:"0 10px 12px",display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:6}}>
                  {["defense1","defense2"].map(k=>(
                    <button key={k} onClick={()=>setSlBuyLevel(k)} style={{padding:"10px 6px",background:slBuyLevel===k?C.coral:C.bg,border:`1px solid ${slBuyLevel===k?C.coral:C.border}`,color:slBuyLevel===k?"#fff":C.ink,fontFamily:KR,fontSize:11.5,fontWeight:700,borderRadius:8,cursor:"pointer"}}>{LEVEL_LABELS[k]}</button>
                  ))}
                  <button onClick={()=>setSlBuyLevel(aiBuyRec)} style={{padding:"10px 6px",background:C.bg,border:`1px solid ${C.border}`,color:C.inkMute,fontFamily:KR,fontSize:11.5,fontWeight:700,borderRadius:8,cursor:"pointer"}}>↻ AI</button>
                </div>
              </div>

              {/* 매도 테이블 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,marginBottom:12,overflow:"hidden"}}>
                <div style={{padding:"12px 14px",borderBottom:`1px solid ${C.border}`,display:"flex",alignItems:"center",gap:8}}>
                  <span style={{fontSize:14}}>📉</span>
                  <span style={{fontSize:13,fontWeight:700,color:C.blue,letterSpacing:"-0.3px"}}>매도 테이블</span>
                  <span style={{background:C.bg,fontSize:9,color:C.inkSubtle,padding:"2px 7px",borderRadius:8}}>04/17 기준</span>
                  <span style={{flex:1}}/>
                  <span style={{fontSize:9,color:C.inkSubtle}}>중심가 ${lv.buyCenter}</span>
                </div>
                <div style={{padding:8}}>
                  <div style={{display:"grid",gridTemplateColumns:"1.2fr 1fr 1fr 0.8fr",gap:6,padding:"8px 8px",fontSize:9.5,color:C.inkSubtle,fontWeight:600,borderBottom:`1px solid ${C.border}`}}>
                    <span>레벨</span><span>기준가</span><span>매도 목표가</span><span>수익률</span>
                  </div>
                  {["target2","target1","center","defense1","defense2"].map(k=>{
                    const isAi = k===aiSellRec;
                    const isSel = k===slSellLevel;
                    const ret = ((sellTargets[k] / lv.buyCenter) - 1) * 100;
                    return (
                      <div key={k} onClick={()=>setSlSellLevel(k)} style={{display:"grid",gridTemplateColumns:"1.2fr 1fr 1fr 0.8fr",gap:6,padding:"10px 8px",fontSize:11,alignItems:"center",cursor:"pointer",background:isSel?`${C.blue}20`:"transparent",borderRadius:6,marginTop:4,borderLeft:isAi?`3px solid ${C.blue}`:"3px solid transparent"}}>
                        <span style={{fontWeight:700}}>{LEVEL_LABELS[k]}{isAi&&<span style={{display:"block",fontSize:8.5,color:C.blue,marginTop:1}}>● AI 추천</span>}</span>
                        <span style={{fontFamily:MO}}>${baseLevels[k].toFixed(2)}</span>
                        <span style={{fontFamily:MO,fontWeight:700,color:C.blue}}>${sellTargets[k].toFixed(2)}</span>
                        <span style={{fontFamily:MO,fontWeight:700,color:ret>=0?C.red:C.blue}}>{ret>=0?"+":""}{ret.toFixed(1)}%</span>
                      </div>
                    );
                  })}
                  <div style={{display:"grid",gridTemplateColumns:"1.2fr 1fr 1fr 0.8fr",gap:6,padding:"10px 8px",fontSize:11,alignItems:"center",borderTop:`1px dashed ${C.amber}`,borderBottom:`1px dashed ${C.amber}`,marginTop:6,background:`${C.amber}10`}}>
                    <span style={{fontWeight:700,color:C.amber,fontSize:10}}>RKLB 애프터마켓</span>
                    <span style={{fontFamily:MO,color:C.amber,fontWeight:700}}>${lv.afterMarket}</span>
                    <span style={{color:C.inkSubtle}}>—</span>
                    <span style={{fontFamily:MO,color:C.blue}}>-1.0%</span>
                  </div>
                </div>
              </div>

              {/* 매도 레벨 선택 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,marginBottom:12,overflow:"hidden"}}>
                <div style={{padding:"10px 14px",fontSize:11,color:C.inkMute,fontWeight:600}}>매도 레벨 선택</div>
                <div style={{padding:"0 10px 10px",display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:6}}>
                  {["target2","target1","center"].map(k=>(
                    <button key={k} onClick={()=>setSlSellLevel(k)} style={{padding:"10px 6px",background:slSellLevel===k?C.coral:C.bg,border:`1px solid ${slSellLevel===k?C.coral:C.border}`,color:slSellLevel===k?"#fff":C.ink,fontFamily:KR,fontSize:11.5,fontWeight:700,borderRadius:8,cursor:"pointer"}}>{k===aiSellRec?"🤖 ":""}{LEVEL_LABELS[k]}</button>
                  ))}
                </div>
                <div style={{padding:"0 10px 12px",display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:6}}>
                  {["defense1","defense2"].map(k=>(
                    <button key={k} onClick={()=>setSlSellLevel(k)} style={{padding:"10px 6px",background:slSellLevel===k?C.coral:C.bg,border:`1px solid ${slSellLevel===k?C.coral:C.border}`,color:slSellLevel===k?"#fff":C.ink,fontFamily:KR,fontSize:11.5,fontWeight:700,borderRadius:8,cursor:"pointer"}}>{LEVEL_LABELS[k]}</button>
                  ))}
                  <button onClick={()=>setSlSellLevel(aiSellRec)} style={{padding:"10px 6px",background:C.bg,border:`1px solid ${C.border}`,color:C.inkMute,fontFamily:KR,fontSize:11.5,fontWeight:700,borderRadius:8,cursor:"pointer"}}>↻ AI</button>
                </div>
              </div>

              {/* 중기 목표 시그널 */}
              <div style={{background:`${C.red}15`,border:`1px solid ${C.red}40`,borderRadius:12,padding:"14px 16px",marginBottom:10}}>
                <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:6}}>
                  <span style={{fontSize:14}}>📅</span>
                  <span style={{fontSize:11,color:C.red,fontWeight:700}}>중기 목표 🎯</span>
                </div>
                <div style={{fontSize:18,fontWeight:800,color:C.red,marginBottom:4}}>목표 달성!</div>
                <div style={{fontSize:11,color:C.inkMute}}>${lv.target1.toFixed(2)} 기준 · +{((liveCur/lv.target1-1)*100).toFixed(1)}% {liveCur>=lv.target1?"상회":"하회"} 중</div>
                <div style={{fontSize:10.5,color:C.inkSubtle,marginTop:4}}>중기 목표를 이미 달성했어요. 장기 목표를 참고하세요.</div>
              </div>

              {/* 장기 목표 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,padding:"14px 16px",marginBottom:10}}>
                <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:6}}>
                  <span style={{fontSize:14}}>📅</span>
                  <span style={{fontSize:11,color:C.inkMute,fontWeight:700}}>장기 목표</span>
                </div>
                <div style={{fontSize:22,fontWeight:800,marginBottom:4}}>${lv.target2.toFixed(2)}</div>
                <div style={{fontSize:11,color:C.red,fontWeight:700,marginBottom:6}}>+{((lv.target2/liveCur-1)*100).toFixed(1)}%</div>
                <div style={{fontSize:10.5,color:C.inkSubtle}}>강한 추세에서 노릴 수 있는 장기 목표예요</div>
              </div>

              {/* 1차 방어선 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,padding:"14px 16px",marginBottom:10}}>
                <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:6}}>
                  <span style={{fontSize:14}}>🛡️</span>
                  <span style={{fontSize:11,color:C.inkMute,fontWeight:700}}>중기 방어선</span>
                </div>
                <div style={{fontSize:22,fontWeight:800,marginBottom:4}}>${lv.defense1.toFixed(2)}</div>
                <div style={{fontSize:11,color:C.blue,fontWeight:700,marginBottom:6}}>{((lv.defense1/liveCur-1)*100).toFixed(1)}%</div>
                <div style={{fontSize:10.5,color:C.inkSubtle}}>이 가격 아래로 내려가면 추가 하락 위험이 있어요</div>
              </div>

              {/* 2차 방어선 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,padding:"14px 16px",marginBottom:10}}>
                <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:6}}>
                  <span style={{fontSize:14}}>🏰</span>
                  <span style={{fontSize:11,color:C.inkMute,fontWeight:700}}>장기 방어선</span>
                </div>
                <div style={{fontSize:22,fontWeight:800,marginBottom:4}}>${lv.defense2.toFixed(2)}</div>
                <div style={{fontSize:11,color:C.blue,fontWeight:700,marginBottom:6}}>{((lv.defense2/liveCur-1)*100).toFixed(1)}%</div>
                <div style={{fontSize:10.5,color:C.inkSubtle}}>{s.signals.defenseNote}</div>
              </div>

              {/* 거래량 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,padding:"14px 16px",marginBottom:10}}>
                <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:6}}>
                  <span style={{fontSize:14}}>📊</span>
                  <span style={{fontSize:11,color:C.inkMute,fontWeight:700}}>이번 주 거래량</span>
                </div>
                <div style={{fontSize:22,fontWeight:800,marginBottom:4}}>{s.weekVolRatio.toFixed(1)}배</div>
                <div style={{fontSize:10.5,color:C.inkMute,marginBottom:6}}>20주 평균 대비 (직전 주 기준)</div>
                <div style={{fontSize:10.5,color:C.inkSubtle}}>{s.signals.volNote}</div>
              </div>

              {/* 52주 신고가 대비 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,padding:"14px 16px",marginBottom:10}}>
                <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:6}}>
                  <span style={{fontSize:14}}>📉</span>
                  <span style={{fontSize:11,color:C.coral,fontWeight:700}}>52주 신고가 대비</span>
                </div>
                <div style={{display:"flex",alignItems:"baseline",gap:6,marginBottom:8}}>
                  <span style={{fontSize:22,fontWeight:800}}>{s.drawdown}%</span>
                  <span style={{fontSize:11,color:C.inkMute}}>조정 구간</span>
                </div>
                <div style={{height:6,background:C.bg,borderRadius:3,overflow:"hidden",marginBottom:6}}>
                  <div style={{width:`${s.drawdownPct}%`,height:"100%",background:C.red,borderRadius:3}}/>
                </div>
                <div style={{fontSize:10,color:C.inkSubtle,marginBottom:4}}>신고가 ${s.high52w} 대비 현재 {s.drawdownPct}% 위치</div>
                <div style={{fontSize:10.5,color:C.inkSubtle,lineHeight:1.5}}>{s.signals.drawdownNote}</div>
              </div>

              {/* 5주선 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,padding:"14px 16px",marginBottom:10}}>
                <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:6}}>
                  <span style={{fontSize:14}}>📊</span>
                  <span style={{fontSize:11,color:C.inkMute,fontWeight:700}}>5주 이동평균선</span>
                </div>
                <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:6}}>
                  <span style={{fontSize:22,fontWeight:800}}>5주선 위</span>
                  <span style={{color:C.red,fontSize:14}}>↗</span>
                </div>
                <div style={{fontSize:11,color:C.red,fontWeight:700,marginBottom:6,background:`${C.red}15`,padding:"2px 8px",borderRadius:10,display:"inline-block"}}>+{s.ma5Diff}%</div>
                <div style={{fontSize:10,color:C.inkSubtle,marginTop:4,marginBottom:6}}>5주선 ${s.monthMA5} · 우상향 ↗</div>
                <div style={{fontSize:10.5,color:C.inkSubtle,lineHeight:1.5}}>{s.signals.ma5Note}</div>
              </div>

              {/* 다음 실적 발표 */}
              <div style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,padding:"14px 16px",marginBottom:14}}>
                <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:6}}>
                  <span style={{fontSize:14}}>📅</span>
                  <span style={{fontSize:11,color:C.inkMute,fontWeight:700}}>다음 실적 발표</span>
                </div>
                <div style={{fontSize:22,fontWeight:800,marginBottom:4}}>D-{s.earningsDays}</div>
                <div style={{fontSize:10.5,color:C.inkSubtle,marginBottom:6}}>{s.nextEarnings}</div>
                <div style={{fontSize:10.5,color:C.inkSubtle,lineHeight:1.5}}>{s.signals.earningsNote}</div>
              </div>

              {/* 데이터 소스 */}
              <div style={{textAlign:"center",fontSize:9.5,color:C.inkSubtle,padding:"10px 0",lineHeight:1.6}}>
                ● 스토캐스틱 소스: Alpha Vantage · 실시간<br/>
                ⚠ 컨센서스·기술적 분석 기반 시뮬레이션. 매매 추천 아니야.
              </div>
            </>
          );
        })()}

        {tab==="watch" && (
          <>
            <div style={{padding:"14px 4px",fontSize:14,fontWeight:700,letterSpacing:"-0.3px"}}>⭐ 주목 종목</div>
            {Object.entries(TICKERS).map(([t,d])=>(
              <div key={t} style={{background:C.surface,border:`1px solid ${C.border}`,borderRadius:12,marginBottom:12,overflow:"hidden"}}>
                <div style={{padding:14,display:"flex",alignItems:"center",gap:12}}>
                  <div style={{flex:1,minWidth:0}}>
                    <div style={{fontSize:14,fontWeight:700,letterSpacing:"-0.3px"}}>{t}</div>
                    <div style={{fontSize:10.5,color:C.inkSubtle,marginTop:2}}>{d.kr} · {d.sec}</div>
                  </div>
                  <div style={{fontFamily:MO,fontSize:14,fontWeight:700}}>₩{FMT(d.cur)}</div>
                </div>
                <div style={{padding:"0 14px 14px"}}>
                  <a href={naverUrl(d.kr)} target="_blank" rel="noopener noreferrer" style={{textDecoration:"none",display:"block"}}>
                    <button style={{width:"100%",background:"#03C75A",border:"none",color:"#fff",fontFamily:KR,fontSize:12,fontWeight:700,padding:10,borderRadius:8,cursor:"pointer"}}>📡 네이버 실시간 →</button>
                  </a>
                </div>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}

export default function App(){
  return <ErrBoundary><AppInner/></ErrBoundary>;
}
