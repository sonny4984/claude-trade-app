import { useState, useEffect, Component } from "react";

/*
 * 사랑의 교실 결과통보서 도우미
 * ------------------------------------------------------------
 * 아이가 손으로 작성한 '나?' 자기이해 활동지 사진을 올리면
 * Gemini Vision이 손글씨를 읽어 결과통보서 '종합의견' 초안을 만들어 줍니다.
 *
 * ▸ 자료(활동지 문항 / 예시 의견)를 추가할 때는 아래
 *   WORKSHEET_PROMPTS 와 EXAMPLES 상수만 보완하면 됩니다.
 */

const KR = "'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif";

// Vision 지원 모델 (앞에서부터 시도, 없으면 다음 모델로 자동 대체)
const MODELS = ["gemini-2.5-flash", "gemini-2.0-flash"];

// 밝고 따뜻한 팔레트
const C = {
  bg: "#f4f6f9",
  surface: "#ffffff",
  surfaceSoft: "#f0f3f8",
  primary: "#2f6fed",
  primaryDark: "#1f57c8",
  primarySoft: "#e7effe",
  ink: "#1a1d23",
  inkMute: "#5c6270",
  inkSubtle: "#9aa1ad",
  border: "#e4e8ee",
  green: "#12b76a",
  amber: "#f79009",
  red: "#e5484d",
};

/* ── '나?' 활동지 대표 문항 (자료 추가 시 여기에 보완) ────────────── */
const WORKSHEET_PROMPTS = [
  "나는 (   )를 일생에 꼭 한 번 하고 싶다.",
  "내가 가장 행복했던 말은 (   )이다.",
  "나는 (   )처럼 살고 싶어.",
  "내 생각에 이 세상에서 가장 힘센 것은 (   )이다.",
  "나는 다른 친구들에게 «   »한 사람으로 인정받고 싶다.",
  "내가 (   )했던 걸 잊고 싶다.",
  "(   )처럼 죽고 싶어.",
  "(   )하다면 진짜 행복할 거야.",
  "나는 (   ) 때문에 제일 많이 웃었다.",
  "내게는 (   )가 유일한 희망이었던 적이 있었다.",
  "내가 가장 좋아하는 사람은 (   )이다.",
  "사랑은 (   ).",
  "내가 제일 좋아하는 과목은 (   ), 그 이유는 (   ) 때문에.",
  "화제가 없을 때 나는 (   ).",
  "나는 (   )을 믿는다.",
  "내게 가장 쓸모없는 일은 (   )이다.",
  "나는 (   )는 절대 못 참는다.",
  "(   )할 때는 정말 움직이기 싫다.",
  "내 스트레스는 (   )을 하면 풀린다.",
];

/* ── 실제 상담사 종합의견 예시 (few-shot) ──────────────────────── */
const EXAMPLES = [
  {
    participation: "적극",
    opinion:
      "행복했던 말로 “너 멋지다”라고 하고, 좋은 몸을 가진 사람을 이기고 싶다와 다른 친구들에게 멋진 사람으로 인정받고 싶다는 것으로 보아 타인에게 보여지는 이미지에 관심이 큰 것으로 보인다. 수학, 과학을 풀면 재미있기 때문에 좋아하는 과목이라고 하며, 점수가 잘 나온다는 것으로 보아 학업에 흥미가 있으며 노력하는 것을 보인다. 참여 중 많이 웃고 즐겁게 참여하였으며, 친구들과 이야기할 때 웃는 모습을 보였다. 행복했던 순간으로 친구와 놀 때와 가족과 있을 때라고 한다. 이로보아 가까운 사람들과의 관계 속에서 행복을 느끼는 것으로 보이며, 가족을 중요하게 여기고 실수했던 걸 잊고 싶다는 표현으로 보아 재범의 가능성은 낮아 보인다.",
  },
  {
    participation: "적극",
    opinion:
      "돈 많은 부자로 살고 싶고, 돈이 있으면 무엇이든 할 수 있어서 돈이 필요하다고 한다. 도박에서 돈을 땄을 때 행복하고, 도박중독에서 벗어나고 싶다고 한다. 도박이 나쁜 짓이기 때문에 도박을 안 하는 사람으로 살고 싶다고 하지만 중독이라는 표현을 사용하는 것으로 보아 끊기 힘든 마음으로 보인다. 스트레스는 흡연으로 푼다고 하며, 힘들어했던 것을 잊고 싶다고 한다. 중독이라는 표현으로 보아 스스로 통제가 어려운 듯하며, 현재도 도박으로 인해 돈이 필요한 상태로 보인다. 이로보아 재범의 가능성은 있어 보인다.",
  },
  {
    participation: "적극",
    opinion:
      "시작할 때 거부감이 있는 눈빛과 태도를 보였으나, 참여하며 적극적이고 우호적인 태도를 유지하였다. 가장 행복했던 순간이 놀 때이며, 스트레스도 놀 때 풀리고 놀기는 늘 재미있다고 한다. 배낭여행을 일생에 한 번 하고 싶으며, 체육이 재미있기 때문에 좋다고 한다. 이로보아 외향적인 성향으로 보이며 외부활동을 좋아하는 것으로 보인다. 거짓말과 시비는 못 참으며, 누군가와 싸웠을 때 힘들다는 것으로 보아 사람 관계에서 오는 갈등을 힘들어하는 듯하다. 타인과 좋은 관계를 유지하기 위해 이해하는 것이 중요하다고 하는 것으로 보아 주변 사람과의 좋은 관계를 위해 노력하는 듯하며, 죄책감 때문에 힘들다는 마음과 적극적인 태도 등으로 보아 재범의 가능성은 낮아 보인다.",
  },
];

/* ── 프롬프트 생성 ───────────────────────────────────────────── */
function buildPrompt({ name, notes }) {
  const promptList = WORKSHEET_PROMPTS.map((p) => "- " + p).join("\n");
  const exampleText = EXAMPLES.map(
    (e, i) => `(예시 ${i + 1}) 참여태도: ${e.participation}\n의견: ${e.opinion}`
  ).join("\n\n");

  return `당신은 청소년 상담 전문가입니다. "사랑의 교실"에 참여한 청소년이 직접 손으로 작성한 '나?' 자기이해 활동지(문장완성형) 사진을 보고, 결과통보서에 들어갈 '종합의견'을 작성합니다.

[활동지 설명]
'나?' 활동지는 아래와 같은 문장의 빈칸을 청소년이 손글씨로 채우는 자기이해 검사입니다. 아래는 대표 문항 예시이며, 실제 사진에 있는 문항과 손글씨 답을 정확히 읽어 파악하세요.
${promptList}

[작성 지침]
1. 사진 속 손글씨 답을 최대한 정확히 읽습니다. 판독이 어려우면 문맥으로 추정하되, 확신이 낮은 답은 조심스럽게 다룹니다.
2. 읽어낸 답들을 종합하여 청소년의 성향, 관심사, 대인관계, 스트레스 해소 방식, 가치관 등을 해석합니다.
3. 아래 예시와 같은 문체의 자연스러운 서술형 문단으로 작성합니다. "~로 보아 ~한 것으로 보인다", "~하는 듯하다", "~로 보인다" 같은 해석적 표현을 사용합니다.
4. 문단 마지막은 반드시 재범의 가능성에 대한 소견("재범의 가능성은 낮아 보인다" 또는 "재범의 가능성은 있어 보인다" 등)으로 마무리합니다.
5. 참여태도는 "적극", "보통", "소극" 중 하나로 판단합니다. 사진만으로 태도를 알기 어려우면 답변 내용을 참고하되 기본값은 "적극"으로 합니다.
6. 전문적이고 담담한 어조를 유지하며, 250~380자 내외로 작성합니다. 활동지에 실제로 없는 사실을 지어내지 않습니다.
${name ? `7. 대상 청소년의 이름은 "${name}"입니다.` : ""}
${notes ? `8. 상담사가 관찰한 추가 내용을 종합의견에 자연스럽게 반영하세요: "${notes}"` : ""}

[예시]
${exampleText}

[출력 형식]
반드시 아래 JSON 형식으로만 답하세요. 다른 설명은 붙이지 마세요.
{
  "name": "활동지에서 읽은 이름(없으면 빈 문자열)",
  "participation": "적극|보통|소극 중 하나",
  "answers": [{"q": "문항", "a": "읽어낸 손글씨 답"}],
  "opinion": "종합의견 서술 문단"
}`;
}

/* ── 이미지 → 축소 후 base64 ─────────────────────────────────── */
function readImage(file) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const url = URL.createObjectURL(file);
    img.onload = () => {
      const maxDim = 1600;
      const scale = Math.min(1, maxDim / Math.max(img.width, img.height));
      const w = Math.round(img.width * scale);
      const h = Math.round(img.height * scale);
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext("2d");
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, w, h);
      ctx.drawImage(img, 0, 0, w, h);
      const dataUrl = canvas.toDataURL("image/jpeg", 0.85);
      URL.revokeObjectURL(url);
      resolve({
        preview: dataUrl,
        base64: dataUrl.split(",")[1],
        mimeType: "image/jpeg",
      });
    };
    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error("이미지를 불러올 수 없습니다."));
    };
    img.src = url;
  });
}

/* ── Gemini Vision 호출 (모델 자동 대체) ──────────────────────── */
async function callGeminiVision(prompt, images, apiKey) {
  if (!apiKey) throw new Error("먼저 Gemini API 키를 입력해 주세요. (하단 ⚙️ 설정)");
  const parts = [{ text: prompt }];
  for (const img of images) {
    parts.push({ inline_data: { mime_type: img.mimeType, data: img.base64 } });
  }
  const body = JSON.stringify({
    contents: [{ parts }],
    generationConfig: { temperature: 0.4, responseMimeType: "application/json" },
  });

  let lastErr = null;
  for (const model of MODELS) {
    try {
      const res = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
        { method: "POST", headers: { "Content-Type": "application/json" }, body }
      );
      const data = await res.json();
      if (!res.ok) {
        const msg = data?.error?.message || "생성에 실패했습니다.";
        // 모델을 못 찾는 경우만 다음 모델로 대체, 그 외(키 오류 등)는 즉시 표시
        if (res.status === 404 || /not found|not supported|is not found/i.test(msg)) {
          lastErr = new Error(msg);
          continue;
        }
        if (res.status === 400 && /api key/i.test(msg))
          throw new Error("Gemini API 키가 올바르지 않습니다. 설정에서 다시 확인해 주세요.");
        throw new Error(msg);
      }
      const text = (data.candidates?.[0]?.content?.parts || [])
        .map((p) => p.text || "")
        .join("");
      if (!text) throw new Error("응답이 비어 있습니다. 사진을 다시 확인해 주세요.");
      return text;
    } catch (e) {
      lastErr = e;
      // 네트워크/기타 오류는 다음 모델로 굳이 재시도하지 않음
      if (!/not found|not supported/i.test(e.message)) throw e;
    }
  }
  throw lastErr || new Error("생성에 실패했습니다.");
}

function parseResult(text) {
  let t = text.trim();
  // ```json ... ``` 방어적 제거
  t = t.replace(/^```(json)?/i, "").replace(/```$/i, "").trim();
  // 첫 { 부터 마지막 } 까지
  const s = t.indexOf("{");
  const e = t.lastIndexOf("}");
  if (s !== -1 && e !== -1) t = t.slice(s, e + 1);
  return JSON.parse(t);
}

/* ── 오류 경계 ───────────────────────────────────────────────── */
class ErrBoundary extends Component {
  constructor(p) {
    super(p);
    this.state = { err: null };
  }
  static getDerivedStateFromError(err) {
    return { err };
  }
  render() {
    if (this.state.err)
      return (
        <div style={{ padding: 24, fontFamily: KR, color: C.ink }}>
          <h3>문제가 발생했어요</h3>
          <p style={{ color: C.inkMute }}>{String(this.state.err?.message || this.state.err)}</p>
          <button
            onClick={() => location.reload()}
            style={{ background: C.primary, color: "#fff", border: 0, padding: "10px 18px", borderRadius: 10, fontSize: 15 }}
          >
            새로고침
          </button>
        </div>
      );
    return this.props.children;
  }
}

function todayStr() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}. ${p(d.getMonth() + 1)}. ${p(d.getDate())}.`;
}

/* ── 메인 ────────────────────────────────────────────────────── */
function AppInner() {
  const [images, setImages] = useState([]); // {preview, base64, mimeType}
  const [name, setName] = useState("");
  const [session, setSession] = useState("");
  const [dateStr, setDateStr] = useState(todayStr());
  const [counselor, setCounselor] = useState(() => localStorage.getItem("counselor_name") || "김순연");
  const [notes, setNotes] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null); // {participation, opinion, answers, name}
  const [showAnswers, setShowAnswers] = useState(false);
  const [copied, setCopied] = useState("");

  const [apiKey, setApiKey] = useState(() => localStorage.getItem("gemini_api_key") || "");
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    localStorage.setItem("counselor_name", counselor);
  }, [counselor]);

  const addFiles = async (fileList) => {
    setError("");
    const files = Array.from(fileList || []).filter((f) => f.type.startsWith("image/"));
    if (!files.length) return;
    try {
      const imgs = await Promise.all(files.map(readImage));
      setImages((prev) => [...prev, ...imgs]);
    } catch (e) {
      setError(e.message);
    }
  };

  const removeImage = (i) => setImages((prev) => prev.filter((_, idx) => idx !== i));

  const generate = async () => {
    setError("");
    setCopied("");
    if (!apiKey) {
      setShowSettings(true);
      setError("먼저 Gemini API 키를 입력해 주세요.");
      return;
    }
    if (!images.length) {
      setError("활동지 사진을 먼저 올려 주세요.");
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      const prompt = buildPrompt({ name, notes });
      const text = await callGeminiVision(prompt, images, apiKey);
      const parsed = parseResult(text);
      const part = ["적극", "보통", "소극"].includes(parsed.participation)
        ? parsed.participation
        : "적극";
      setResult({
        participation: part,
        opinion: parsed.opinion || "",
        answers: Array.isArray(parsed.answers) ? parsed.answers : [],
        name: parsed.name || "",
      });
      if (!name && parsed.name) setName(parsed.name);
    } catch (e) {
      setError(e.message || "생성 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  const fullText = () => {
    if (!result) return "";
    const head = [
      name && `이름: ${name}`,
      session && `회기: ${session}`,
      dateStr && `일자: ${dateStr}`,
    ]
      .filter(Boolean)
      .join("    ");
    return `${head ? head + "\n\n" : ""}[참여태도] ${result.participation}\n\n[종합의견]\n${result.opinion}${
      counselor ? `\n\n상담사  ${counselor}` : ""
    }`;
  };

  const copy = async (what) => {
    const text = what === "opinion" ? result.opinion : fullText();
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    setCopied(what);
    setTimeout(() => setCopied(""), 1800);
  };

  const canGenerate = images.length > 0 && !loading;

  return (
    <div style={{ fontFamily: KR, background: C.bg, minHeight: "100vh", color: C.ink }}>
      {/* 헤더 */}
      <header
        style={{
          background: C.surface,
          borderBottom: `1px solid ${C.border}`,
          padding: "14px 18px",
          position: "sticky",
          top: 0,
          zIndex: 5,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 9 }}>
          <span style={{ fontSize: 20 }}>💛</span>
          <div style={{ fontSize: 16, fontWeight: 800 }}>사랑의 교실 · 결과통보서 도우미</div>
        </div>
        <button
          onClick={() => setShowSettings((v) => !v)}
          aria-label="설정"
          style={{ background: "transparent", border: 0, fontSize: 20, cursor: "pointer", color: C.inkMute }}
        >
          ⚙️
        </button>
      </header>

      <main style={{ maxWidth: 640, margin: "0 auto", padding: "16px 16px 120px" }}>
        {/* 설정 패널 */}
        {showSettings && (
          <Card>
            <Label>🔑 Gemini API 키</Label>
            <div style={{ display: "flex", gap: 8 }}>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="AIzaSy..."
                style={inputStyle}
              />
              <button
                onClick={() => {
                  localStorage.setItem("gemini_api_key", apiKey.trim());
                  setApiKey(apiKey.trim());
                  setShowSettings(false);
                }}
                style={btnPrimary}
              >
                저장
              </button>
            </div>
            <div style={{ fontSize: 12, color: C.inkSubtle, marginTop: 8, lineHeight: 1.6 }}>
              키는 이 기기(브라우저)에만 저장되며 서버로 전송되지 않습니다.
              <br />
              무료 발급 → aistudio.google.com/app/apikey
            </div>
          </Card>
        )}

        {/* 안내 */}
        <div
          style={{
            background: C.primarySoft,
            borderRadius: 14,
            padding: "13px 15px",
            fontSize: 13.5,
            color: C.primaryDark,
            lineHeight: 1.6,
            marginBottom: 16,
          }}
        >
          아이가 작성한 <b>‘나?’ 활동지 사진</b>을 올리면 종합의견 <b>초안</b>을 만들어 드려요.
          내용은 반드시 상담사가 확인·수정한 뒤 사용해 주세요.
        </div>

        {/* STEP 1: 사진 */}
        <Card>
          <StepTitle n="1" t="활동지 사진 올리기" />
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(92px, 1fr))", gap: 10, marginTop: 4 }}>
            {images.map((img, i) => (
              <div key={i} style={{ position: "relative", aspectRatio: "3/4", borderRadius: 10, overflow: "hidden", border: `1px solid ${C.border}` }}>
                <img src={img.preview} alt={`활동지 ${i + 1}`} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
                <button
                  onClick={() => removeImage(i)}
                  style={{
                    position: "absolute",
                    top: 4,
                    right: 4,
                    background: "rgba(0,0,0,0.55)",
                    color: "#fff",
                    border: 0,
                    borderRadius: 999,
                    width: 24,
                    height: 24,
                    fontSize: 14,
                    cursor: "pointer",
                    lineHeight: 1,
                  }}
                >
                  ×
                </button>
              </div>
            ))}
            <label
              style={{
                aspectRatio: "3/4",
                border: `2px dashed ${C.border}`,
                borderRadius: 10,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                cursor: "pointer",
                color: C.inkMute,
                background: C.surfaceSoft,
                fontSize: 13,
                gap: 4,
                textAlign: "center",
              }}
            >
              <span style={{ fontSize: 26 }}>＋</span>
              사진 추가
              <input
                type="file"
                accept="image/*"
                multiple
                capture="environment"
                onChange={(e) => {
                  addFiles(e.target.files);
                  e.target.value = "";
                }}
                style={{ display: "none" }}
              />
            </label>
          </div>
          <div style={{ fontSize: 12, color: C.inkSubtle, marginTop: 10 }}>
            여러 장(앞·뒷면)을 함께 올릴 수 있어요. 글씨가 선명하게 나오도록 밝은 곳에서 찍어 주세요.
          </div>
        </Card>

        {/* STEP 2: 기본 정보 */}
        <Card>
          <StepTitle n="2" t="기본 정보 (선택)" />
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
            <Field label="이름">
              <input value={name} onChange={(e) => setName(e.target.value)} placeholder="예: 홍길동" style={inputStyle} />
            </Field>
            <Field label="회기">
              <input value={session} onChange={(e) => setSession(e.target.value)} placeholder="예: 7회기" style={inputStyle} />
            </Field>
            <Field label="일자">
              <input value={dateStr} onChange={(e) => setDateStr(e.target.value)} style={inputStyle} />
            </Field>
            <Field label="상담사">
              <input value={counselor} onChange={(e) => setCounselor(e.target.value)} style={inputStyle} />
            </Field>
          </div>
          <div style={{ marginTop: 12 }}>
            <Field label="상담 중 관찰한 점 (선택)">
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="예: 시작할 때 거부감을 보였으나 이후 적극적으로 참여함"
                rows={2}
                style={{ ...inputStyle, resize: "vertical", lineHeight: 1.5 }}
              />
            </Field>
          </div>
        </Card>

        {/* 생성 버튼 */}
        <button
          onClick={generate}
          disabled={!canGenerate}
          style={{
            width: "100%",
            padding: "16px",
            marginTop: 4,
            borderRadius: 14,
            border: 0,
            fontSize: 17,
            fontWeight: 800,
            color: "#fff",
            background: canGenerate ? C.primary : "#b8c4d6",
            cursor: canGenerate ? "pointer" : "not-allowed",
            boxShadow: canGenerate ? "0 6px 18px rgba(47,111,237,0.30)" : "none",
            transition: "all .15s",
          }}
        >
          {loading ? "생성 중… 잠시만요 ⏳" : "종합의견 만들기"}
        </button>

        {error && (
          <div style={{ marginTop: 12, background: "#fdecec", color: C.red, padding: "12px 14px", borderRadius: 12, fontSize: 14, lineHeight: 1.5 }}>
            {error}
          </div>
        )}

        {/* 결과 */}
        {result && (
          <div style={{ marginTop: 18 }}>
            <Card>
              <StepTitle n="3" t="결과 (수정 가능)" />

              {/* AI가 읽은 답 */}
              {result.answers.length > 0 && (
                <div style={{ marginBottom: 14 }}>
                  <button
                    onClick={() => setShowAnswers((v) => !v)}
                    style={{
                      background: C.surfaceSoft,
                      border: `1px solid ${C.border}`,
                      borderRadius: 10,
                      padding: "9px 12px",
                      fontSize: 13.5,
                      color: C.inkMute,
                      width: "100%",
                      textAlign: "left",
                      cursor: "pointer",
                      fontWeight: 600,
                    }}
                  >
                    {showAnswers ? "▾" : "▸"} AI가 읽은 답 {result.answers.length}개 — 오독이 있는지 확인해 보세요
                  </button>
                  {showAnswers && (
                    <div style={{ marginTop: 8, border: `1px solid ${C.border}`, borderRadius: 10, overflow: "hidden" }}>
                      {result.answers.map((a, i) => (
                        <div
                          key={i}
                          style={{
                            display: "flex",
                            gap: 10,
                            padding: "9px 12px",
                            fontSize: 13,
                            borderBottom: i < result.answers.length - 1 ? `1px solid ${C.border}` : "none",
                            background: i % 2 ? C.surfaceSoft : C.surface,
                          }}
                        >
                          <span style={{ color: C.inkSubtle, flex: 1 }}>{a.q}</span>
                          <span style={{ fontWeight: 700, color: C.ink, flexShrink: 0, maxWidth: "45%", textAlign: "right" }}>
                            {a.a}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* 참여태도 */}
              <Label>참여태도</Label>
              <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
                {["적극", "보통", "소극"].map((p) => {
                  const on = result.participation === p;
                  return (
                    <button
                      key={p}
                      onClick={() => setResult((r) => ({ ...r, participation: p }))}
                      style={{
                        flex: 1,
                        padding: "11px 0",
                        borderRadius: 10,
                        border: `1.5px solid ${on ? C.primary : C.border}`,
                        background: on ? C.primary : C.surface,
                        color: on ? "#fff" : C.inkMute,
                        fontWeight: 700,
                        fontSize: 15,
                        cursor: "pointer",
                      }}
                    >
                      {p}
                    </button>
                  );
                })}
              </div>

              {/* 종합의견 */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                <Label style={{ margin: 0 }}>종합의견</Label>
                <span style={{ fontSize: 12, color: C.inkSubtle }}>{result.opinion.length}자</span>
              </div>
              <textarea
                value={result.opinion}
                onChange={(e) => setResult((r) => ({ ...r, opinion: e.target.value }))}
                rows={10}
                style={{ ...inputStyle, resize: "vertical", lineHeight: 1.75, fontSize: 15 }}
              />

              {/* 복사 */}
              <div style={{ display: "flex", gap: 8, marginTop: 14 }}>
                <button onClick={() => copy("opinion")} style={{ ...btnPrimary, flex: 1, padding: "13px" }}>
                  {copied === "opinion" ? "복사됨 ✓" : "종합의견 복사"}
                </button>
                <button onClick={() => copy("full")} style={{ ...btnGhost, flex: 1, padding: "13px" }}>
                  {copied === "full" ? "복사됨 ✓" : "전체 복사"}
                </button>
              </div>
              <div style={{ fontSize: 12, color: C.inkSubtle, marginTop: 10, lineHeight: 1.55 }}>
                AI가 만든 초안입니다. 사실관계와 표현을 반드시 확인·수정한 뒤 사용해 주세요.
              </div>
            </Card>

            <button onClick={generate} disabled={loading} style={{ ...btnGhost, width: "100%", padding: "13px", marginTop: 10 }}>
              🔄 다시 생성
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

/* ── 작은 UI 조각들 ──────────────────────────────────────────── */
const inputStyle = {
  width: "100%",
  background: C.surface,
  border: `1px solid ${C.border}`,
  color: C.ink,
  padding: "11px 13px",
  borderRadius: 10,
  fontSize: 15,
  fontFamily: KR,
  outline: "none",
};
const btnPrimary = {
  background: C.primary,
  color: "#fff",
  border: 0,
  padding: "11px 18px",
  borderRadius: 10,
  fontWeight: 700,
  fontSize: 15,
  cursor: "pointer",
  whiteSpace: "nowrap",
};
const btnGhost = {
  background: C.surface,
  color: C.primary,
  border: `1.5px solid ${C.primary}`,
  padding: "11px 18px",
  borderRadius: 10,
  fontWeight: 700,
  fontSize: 15,
  cursor: "pointer",
  whiteSpace: "nowrap",
};

function Card({ children }) {
  return (
    <div
      style={{
        background: C.surface,
        border: `1px solid ${C.border}`,
        borderRadius: 16,
        padding: "16px 16px",
        marginBottom: 14,
        boxShadow: "0 1px 2px rgba(16,24,40,0.04)",
      }}
    >
      {children}
    </div>
  );
}
function StepTitle({ n, t }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 9, marginBottom: 12 }}>
      <span
        style={{
          width: 24,
          height: 24,
          borderRadius: 999,
          background: C.primary,
          color: "#fff",
          fontSize: 13,
          fontWeight: 800,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {n}
      </span>
      <span style={{ fontSize: 16, fontWeight: 800 }}>{t}</span>
    </div>
  );
}
function Label({ children, style }) {
  return <div style={{ fontSize: 13.5, fontWeight: 700, color: C.inkMute, marginBottom: 8, ...style }}>{children}</div>;
}
function Field({ label, children }) {
  return (
    <label style={{ display: "block" }}>
      <div style={{ fontSize: 12.5, color: C.inkMute, marginBottom: 6, fontWeight: 600 }}>{label}</div>
      {children}
    </label>
  );
}

export default function App() {
  return (
    <ErrBoundary>
      <AppInner />
    </ErrBoundary>
  );
}
