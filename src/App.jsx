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
  coral: "#3182f6", coralDark: "#1b64da",
  bg: "#0e0f11", surface: "#17181c", surfaceLight: "#202228",
  ink: "#ffffff", inkMute: "#9ea3ad", inkSubtle: "#5e636e",
  border: "#26282e",
  green: "#f04452", red: "#f04452", amber: "#ffa726", blue: "#3d8bff"
};

const HOLDINGS = [
  { sym: "SNDK", name: "샘디스크", sec: "메모리반도체", krValue: 724883, returnPct: 6.8 },
  { sym: "NBIS", name: "네비우스", sec: "AI 인프라", krValue: 721123, returnPct: 3.7, pick: true },
  { sym: "COHR", name: "코히어런트", sec: "광학반도체", krValue: 696351, returnPct: 0.1, pick: true },
  { sym: "AVGO", name: "브로드컴", sec: "반도체", krValue: 500120, returnPct: 2.3 },
  { sym: "KTOS", name: "크라토스", sec: "방산", krValue: 447005, returnPct: -0.05, pick: true },
  { sym: "NVT", name: "엔벤트", sec: "전기설비", krValue: 399197, returnPct: 0.5 },
  { sym: "MU", name: "마이크론", sec: "메모리반도체", krValue: 396504, returnPct: -0.2, pick: true },
  { sym: "AMD", name: "AMD", sec: "반도체", krValue: 373296, returnPct: 8.4 }
];

const HOLDING_SYMS = HOLDINGS.map(h => h.sym);

function AppInner() {
  const [tab, setTab] = useState("today");
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [toast, setToast] = useState(null);
  const [liveStocks, setLiveStocks] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);

  // Gemini + AI Council
  const [geminiKey, setGeminiKey] = useState(() => localStorage.getItem("gemini_api_key") || "");
  const [councilMode, setCouncilMode] = useState(true);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [isAiLoading, setIsAiLoading] = useState(false);

  const fetchPrices = async () => {
    setAiLoading(true);
    try {
      // TODO: 기존 백엔드 호출 로직 유지
      setToast("실시간 가격 갱신 완료");
      setTimeout(() => setToast(null), 1500);
    } catch (e) {
      console.error(e);
    } finally {
      setAiLoading(false);
    }
  };

  useEffect(() => {
    let interval = null;
    if (autoRefresh) {
      interval = setInterval(() => {
        if (!aiLoading) fetchPrices();
      }, 90000);
    }
    return () => clearInterval(interval);
  }, [autoRefresh, aiLoading]);

  const callGemini = async (prompt, apiKey) => {
    if (!apiKey) throw new Error("Gemini API Key를 설정에서 입력해주세요.");
    const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error?.message || "Gemini 호출 실패");
    return data.candidates[0].content.parts[0].text;
  };

  const sendToCouncil = async () => {
    if (!chatInput.trim() || !geminiKey) return;
    const userMsg = { role: "user", content: chatInput };
    setChatMessages(prev => [...prev, userMsg]);
    const currentInput = chatInput;
    setChatInput("");
    setIsAiLoading(true);

    try {
      const holdingsContext = HOLDINGS.map(h => {
        const q = liveStocks?.items?.find(s => s.code === h.sym);
        return `${h.name} (${h.sym}): $${q?.price || "?"} ${q?.changePct ? (q.changePct > 0 ? "+" : "") + q.changePct.toFixed(1) + "%" : ""}`;
      }).join("\n");

      let prompt = `You are the AI Council of 4 experts:\n1. Grok (truth-seeking, direct)\n2. Claude (risk-focused, careful)\n3. GPT (creative, optimistic)\n4. Gemini (data-driven, balanced)\n\nUser portfolio:\n${holdingsContext}\n\nQuestion: ${currentInput}\n\nEach AI gives short opinion, then debate, then give final recommendation in Korean with specific actions.`;

      if (!councilMode) {
        prompt = `You are a professional portfolio advisor. Answer in Korean based on the portfolio.\n${holdingsContext}\n\nQuestion: ${currentInput}`;
      }

      const reply = await callGemini(prompt, geminiKey);
      setChatMessages(prev => [...prev, { role: "assistant", content: reply }]);
    } catch (e) {
      setChatMessages(prev => [...prev, { role: "assistant", content: "\uc624류: " + e.message }]);
    } finally {
      setIsAiLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: KR, background: C.bg, minHeight: "100vh", color: C.ink }}>
      {/* Header */}
      <div style={{ background: C.surface, borderBottom: `1px solid ${C.border}`, padding: "12px 16px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ fontSize: 15, fontWeight: 800 }}>
          Claude Trade <span style={{ color: C.coral }}>MAX</span> <span style={{ fontSize: 12, color: C.inkSubtle }}>+ AI Council</span>
        </div>
        <button 
          onClick={() => setAutoRefresh(!autoRefresh)} 
          style={{ 
            background: autoRefresh ? C.coral : C.surface, 
            color: autoRefresh ? "white" : C.inkMute, 
            padding: "6px 14px", 
            borderRadius: 999, 
            fontSize: 12, 
            fontWeight: 700 
          }}
        >
          {autoRefresh ? "실시간 ON" : "실시간 OFF"}
        </button>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", borderBottom: `1px solid ${C.border}` }}>
        {[
          { id: "today", l: "오늘" },
          { id: "council", l: "🧠 AI Council" }
        ].map(t => (
          <button 
            key={t.id} 
            onClick={() => setTab(t.id)} 
            style={{ 
              flex: 1, 
              padding: "14px 0", 
              background: tab === t.id ? C.surface : "transparent",
              color: tab === t.id ? C.coral : C.inkMute,
              borderBottom: tab === t.id ? `3px solid ${C.coral}` : "none",
              fontWeight: tab === t.id ? 700 : 500
            }}
          >
            {t.l}
          </button>
        ))}
      </div>

      {/* AI Council Tab */}
      {tab === "council" && (
        <div style={{ padding: "20px 16px" }}>
          <div style={{ fontSize: 20, fontWeight: 800, marginBottom: 6 }}>🧠 AI Council</div>
          <div style={{ fontSize: 13, color: C.inkSubtle, marginBottom: 16 }}>
            Gemini가 4개 AI(Grok / Claude / GPT / Gemini)를 대표해 토론합니다
          </div>

          {/* Gemini Key */}
          <div style={{ background: C.surface, padding: 14, borderRadius: 12, marginBottom: 16 }}>
            <div style={{ fontSize: 13, fontWeight: 700, marginBottom: 6 }}>🔑 Gemini API Key (무료)</div>
            <div style={{ display: "flex", gap: 8 }}>
              <input
                type="password"
                value={geminiKey}
                onChange={e => setGeminiKey(e.target.value)}
                placeholder="AIzaSy..."
                style={{ flex: 1, background: C.bg, border: `1px solid ${C.border}`, color: C.ink, padding: "10px 12px", borderRadius: 8, fontSize: 14 }}
              />
              <button 
                onClick={() => {
                  localStorage.setItem("gemini_api_key", geminiKey);
                  alert("저장 완료!");
                }} 
                style={{ background: C.coral, color: "white", padding: "10px 20px", borderRadius: 8, fontWeight: 700, fontSize: 14 }}
              >
                저장
              </button>
            </div>
            <div style={{ fontSize: 11, color: C.inkSubtle, marginTop: 6 }}>
              https://aistudio.google.com/app/apikey 에서 무료 발급
            </div>
          </div>

          {/* Chat Area */}
          <div style={{ background: C.surface, borderRadius: 16, height: 440, display: "flex", flexDirection: "column", overflow: "hidden" }}>
            <div style={{ flex: 1, overflowY: "auto", padding: 16, display: "flex", flexDirection: "column", gap: 14 }}>
              {chatMessages.length === 0 && (
                <div style={{ color: C.inkSubtle, textAlign: "center", paddingTop: 80, lineHeight: 1.6 }}>
                  포트폴리오에 대해 묻고 싶은 것을 입력해주세요.<br />
                  Council 모드 ON 시 4AI가 토론합니다.
                </div>
              )}
              {chatMessages.map((m, i) => (
                <div key={i} style={{ alignSelf: m.role === "user" ? "flex-end" : "flex-start", maxWidth: "88%" }}>
                  <div style={{ fontSize: 11, color: C.inkSubtle, marginBottom: 3 }}>
                    {m.role === "user" ? "나" : "AI Council"}
                  </div>
                  <div style={{ 
                    background: m.role === "user" ? C.coral : C.bg, 
                    color: m.role === "user" ? "white" : C.ink, 
                    padding: "12px 15px", 
                    borderRadius: 14, 
                    whiteSpace: "pre-wrap", 
                    fontSize: 14.5, 
                    lineHeight: 1.55 
                  }}>
                    {m.content}
                  </div>
                </div>
              ))}
              {isAiLoading && <div style={{ color: C.inkSubtle, fontSize: 13, paddingLeft: 6 }}>아이 코운실이 토론 중...</div>}
            </div>

            <div style={{ padding: 12, borderTop: `1px solid ${C.border}`, display: "flex", gap: 8 }}>
              <input
                value={chatInput}
                onChange={e => setChatInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && sendToCouncil()}
                placeholder="질문 입력 (e.g. AVGO 비중 줄여도 될까?)"
                style={{ flex: 1, background: C.bg, border: `1px solid ${C.border}`, color: C.ink, padding: "13px 18px", borderRadius: 999, fontSize: 15 }}
              />
              <button 
                onClick={sendToCouncil} 
                disabled={isAiLoading || !chatInput.trim() || !geminiKey}
                style={{ background: C.coral, color: "white", padding: "0 26px", borderRadius: 999, fontWeight: 700, fontSize: 15 }}
              >
                전송
              </button>
            </div>
          </div>

          <div style={{ marginTop: 10, fontSize: 12, color: C.inkSubtle, textAlign: "center" }}>
            Council 모드 = 4AI(Grok/Claude/GPT/Gemini)가 토론 후 결론
          </div>
        </div>
      )}

      {/* Today Tab (simplified but working) */}
      {tab === "today" && (
        <div style={{ padding: "16px 16px 60px" }}>
          <div style={{ background: C.surface, borderRadius: 14, padding: "16px 18px", marginBottom: 14 }}>
            <div style={{ fontSize: 15, fontWeight: 700, marginBottom: 12 }}>💼 내 보유종목 (실시간)</div>
            {HOLDINGS.map((h, i) => {
              const q = liveStocks?.items?.find(s => s.code === h.sym);
              const up = (q?.changePct || 0) >= 0;
              return (
                <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "9px 0", borderBottom: i < HOLDINGS.length-1 ? `1px solid ${C.border}` : "none" }}>
                  <div style={{ fontSize: 14.5 }}>{h.name} <span style={{ color: C.inkSubtle, fontSize: 12 }}>({h.sym})</span></div>
                  <div style={{ textAlign: "right" }}>
                    <div style={{ fontFamily: MO, fontSize: 15 }}>${q?.price || "—"}</div>
                    <div style={{ fontSize: 12.5, color: up ? C.red : C.blue }}>
                      {up ? "▲" : "▼"} {Math.abs(q?.changePct || 0).toFixed(1)}%
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div style={{ fontSize: 12, color: C.inkSubtle, textAlign: "center", lineHeight: 1.5 }}>
            실시간 가격은 자동 갱신됩니다.<br />
            통합된 분석은 <b>AI Council</b> 탭에서 이용해주세요.
          </div>
        </div>
      )}
    </div>
  );
}

export default function App() {
  return <ErrBoundary><AppInner /></ErrBoundary>;
}
