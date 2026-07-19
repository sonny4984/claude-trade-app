import { useState, useEffect, Component } from "react";
import { downloadReportDocx } from "./reportDoc.js";

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
// gemini-flash-latest: 항상 최신 Flash를 가리키는 별칭. 신규 발급 키는 구버전
// 모델(2.5/2.0)을 못 쓰는 경우가 있어 별칭을 1순위로 둔다.
const MODELS = ["gemini-flash-latest", "gemini-2.5-flash", "gemini-2.0-flash"];

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

/* ── '나?' 활동지 문항 (앞장: 문장완성) ───────────────────────── */
const PAGE1_PROMPTS = [
  "나는 (   )를 일생에 꼭 한 번 하고 싶다.",
  "내가 가장 행복했던 말은 (   )이다.",
  "내게 (   )는 늘 신선하다.",
  "내 생각에 이 세상에서 가장 힘센 것은 (   )이다.",
  "나는 (   )처럼 살고 싶어.",
  "나는 다른 친구들에게 «   »한 사람으로 인정받고 싶다.",
  "나는 [   ]처럼 죽고 싶어.",
  "내가 (   )했던 걸 잊고 싶다.",
  "무엇보다 (   )가 필요해.",
  "(   )하다면 진짜 행복할 거야.",
  "내게 (   )가 유일한 희망이었던 적이 있었다.",
  "나는 (   ) 때문에 제일 많이 울었다.",
  "나는 [   ] 덕분에 제일 많이 웃었다.",
  "내게는 (   )가 지나치다.",
  "(   )는 늘 흥미롭다.",
  "내가 가장 좋아하는 사람은 (   )이고, 나를 가장 좋아하는 사람은 (   )이다.",
  "사랑은 {   }해야 한다고 생각한다.",
  "내가 제일 좋아하는 과목은 (   )이고, 그 이유는 (   )이다.",
  "화제가 없을 때 나는 <   > 얘기를 꺼낸다.",
  "나는 늘 (   )는 이기고 싶었다.",
  "나는 (   )을 믿는다.",
  "내게 가장 쓸모없는 일은 (   )이다.",
  "나는 (   )는 절대 못 참는다.",
  "(   )에 가는 것이 제일 싫다.",
  "(   )할 때는 정말 움직이기 싫다.",
  "내 스트레스는 (   )을 하면 풀린다.",
];

/* ── 뒷장: 순간·선택 문항 ─────────────────────────────────────── */
const PAGE2_PROMPTS = [
  "내가 가장 행복했던 순간은 (   )이다.",
  "내가 가장 힘들고 슬펐던 순간은 (   )이다.",
  "내가 가장 잘 선택했던 것(일, 사람, 경험)은 (   )이다.",
  "내가 가장 버리고 싶은 것(일, 사람, 경험, 습관 등)은 (   )이다.",
  "나는 (   ) 사람으로 살고 싶다. 이유는 (   )이며,",
  "30년 후 나는 (   ) 모습으로 살고 있을 것이다.",
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
  {
    participation: "적극",
    opinion:
      "여기에 온 이유로 “남의 물건에 손을 대서”라고 명확히 인지하고 있으며, “다음부턴 그러지 않겠다”고 다짐하는 것으로 보아 자신의 잘못을 반성하고 있는 것으로 보인다. ‘가족’을 유일한 희망이자 가장 좋아하고 믿는 대상으로 반복해 꼽고 있으며, ‘대인관계’ 때문에 제일 많이 울었다고 답하는 것으로 보아 타인과의 관계, 특히 가족과 친구와의 유대감을 매우 중요하게 여기고 정서적으로 의존하는 성향이 크다. 또한 ‘소년원’에 가는 것이 제일 싫고 ‘먼저 치는 것’을 절대 못 참는다고 표현하는 점, 싸웠던 것을 잊고 싶어 하는 점으로 미루어 보아 갈등 상황을 회피하고자 하며 올바른 생활에 대한 의지가 있는 것으로 판단된다. 체육을 가장 좋아하고 놀 때 스트레스가 풀린다고 하여 외향적이고 에너지가 많은 편이다. 가족의 지지와 관계 회복을 중요시하며, 자신의 행동이 가져올 부정적 결과를 기피하는 마음이 확고하여 재범의 가능성은 낮아 보인다.",
  },
  {
    participation: "적극",
    opinion:
      "“모르는 메시지로 협박해서”라는 비행 사실을 정확히 인지하고 “다음부터는 안 그러겠다”고 작성한 것으로 보아 자신의 잘못된 행동을 수용하고 반성하는 태도를 보인다. 설문 전반에 걸쳐 ‘태권도 선수’가 되고 싶고, 태권도를 할 때 진정 행복하며 유일한 희망이라고 답할 정도로 뚜렷한 진로 목표와 특기에 대한 강한 자부심을 가지고 있다. 부모님과 친구를 깊이 의지하며, 특히 ‘친구를 때리는 것’을 절대 참지 못하고 친구가 필요하다고 하는 점에서 또래 관계와 의리를 매우 중시하는 성향이다. 짜증 날 때 울고 욱하는 기질이 다소 엿보이나, ‘무언가를 훔치는 것’을 제일 쓸모없는 일로 치부하고 ‘술집’을 제일 싫어하는 등 나쁜 행동에 대한 나름의 명확한 거부 기준을 가지고 있다. 자신에 대한 믿음이 확고하고 태권도라는 건전한 목표와 스트레스 해소구가 뚜렷하게 존재하므로, 충동 조절 훈련이 병행된다면 재범의 가능성은 낮아 보인다.",
  },
  {
    participation: "적극",
    opinion:
      "친구의 장난감을 훔친 사실을 인정하며 “안 그러게 노력 중”이라고 표현하여, 비행 행동을 뉘우치고 스스로 개선하려는 의지를 보이고 있다. 생일 선물이 망가져 슬펐지만 친구가 놀아주어 기분이 좋아졌다고 세세히 서술하고 웃는 모습을 그린 것으로 보아, 또래의 정서적 지지에 긍정적으로 반응하고 교우 관계에서 큰 안정감을 느끼는 것으로 보인다. 축구와 이강인 선수를 좋아하며 체육과 운동으로 스트레스를 푸는 매우 외향적이고 활동적인 성향이다. 설문에서 ‘여자친구’를 가장 좋아하고 믿는 대상으로 반복해서 적는 등 현재 이성 교제와 대인관계에 에너지가 집중되어 있다. ‘동물 학대’를 절대 참지 못한다고 답하여 타인이나 약자에 대한 기본적 공감 능력을 갖추고 있는 것으로 파악되며, 나쁜 행동을 고치고자 하는 자발적 노력과 주변과의 긍정적인 관계망이 형성되어 있으므로 재범의 가능성은 낮아 보인다.",
  },
];

/* ── 프롬프트 생성 ───────────────────────────────────────────── */
function buildPrompt({ name, notes }) {
  const p1 = PAGE1_PROMPTS.map((p) => "- " + p).join("\n");
  const p2 = PAGE2_PROMPTS.map((p) => "- " + p).join("\n");
  const exampleText = EXAMPLES.map(
    (e, i) => `(예시 ${i + 1}) 참여태도: ${e.participation}\n의견: ${e.opinion}`
  ).join("\n\n");

  return `당신은 청소년 상담 전문가입니다. "사랑의 교실"에 참여한 청소년이 직접 손으로 작성한 '나?' 자기이해 활동지 사진을 보고, 결과통보서에 들어갈 '종합의견'을 작성합니다.

[활동지 구성]
사진은 한 청소년이 작성한 활동지 여러 장(앞장·뒷장·그림)일 수 있습니다. 위쪽 "이름" 칸에 손글씨 이름이 적혀 있습니다.

① 앞장(문장완성) — 아래 문장의 빈칸을 손글씨로 채웁니다:
${p1}

② 뒷장(순간·선택):
${p2}

③ 그림(자아상 그리기) — 자신·가족·좋아하는 것 등을 자유롭게 그립니다. 그림이 있으면 등장 인물(이름 표기 포함), 표정, 반복되는 소재, 글자 메모 등을 관찰해 해석에 활용하세요.

④ 일부 활동지에는 "여기에 온 이유", "앞으로의 다짐" 등을 적는 문항이 있을 수 있습니다. 있으면 반드시 읽어 반영하세요.

[손글씨 읽기 규칙]
1. 사진 속 손글씨를 최대한 정확히 읽습니다. 판독이 어려우면 문맥으로 조심스럽게 추정합니다.
2. 줄을 긋거나 덧칠해 지운 답은 억지로 읽지 않습니다. 지운 뒤 옆이나 위에 새로 쓴 답이 있으면 새 답을 최종 답으로 봅니다.
3. 활동지에 실제로 없는 내용은 지어내지 않으며, 비어 있는 문항은 건너뜁니다.

[종합의견 작성 지침]
1. 서술 구조: ① 아이가 쓴 답·발언·그림 같은 객관적 근거를 먼저 제시하고 → ② 이를 바탕으로 심리 상태·성향·관심사·대인관계·스트레스 해소 방식·가치관을 유추하며 → ③ 마지막 문장은 반드시 재범의 가능성에 대한 결론("재범의 가능성은 낮아 보인다" / "있어 보인다" / "높아 보인다" 등)으로 마무리합니다.
2. "여기에 온 이유"·"앞으로의 다짐" 문항이 있으면, 비행 사실을 스스로 인지하고 반성하는지를 문단 앞부분에서 먼저 다룹니다.
3. 아래 예시와 같은 문체의 자연스러운 서술형 문단으로 작성합니다. "~로 보아 ~한 것으로 보인다", "~하는 듯하다", "~로 보인다" 같은 해석적 표현을 사용합니다.
4. 참여태도는 "적극", "보통", "소극" 중 하나로 판단합니다. 사진만으로 태도를 알기 어려우면 답변 내용을 참고하되 기본값은 "적극"으로 합니다.
5. 전문적이고 담담한 어조를 유지하며, 250~380자 내외로 작성합니다.
${name ? `6. 대상 청소년의 이름은 "${name}"입니다.` : ""}
${notes ? `7. 상담사가 관찰한 추가 내용을 종합의견에 자연스럽게 반영하세요: "${notes}"` : ""}

[예시]
${exampleText}

[출력 형식]
반드시 아래 JSON 형식으로만 답하세요. 다른 설명은 붙이지 마세요.
키 순서를 꼭 지키세요(name → participation → opinion → answers).
answers의 "a" 값 안에서는 큰따옴표(") 대신 작은따옴표(')를 사용하세요.
{
  "name": "활동지 이름 칸에서 읽은 이름(없으면 빈 문자열)",
  "participation": "적극|보통|소극 중 하나",
  "opinion": "종합의견 서술 문단",
  "answers": [{"q": "문항(그림 관찰은 '그림')", "a": "읽어낸 손글씨 답 또는 그림 관찰 내용"}]
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
    generationConfig: { temperature: 0.4, responseMimeType: "application/json", maxOutputTokens: 8192 },
  });

  let lastErr = null;
  for (const model of MODELS) {
    try {
      // 키는 URL이 아닌 헤더로 전달 (신형 AQ. 키·구형 AIza 키 모두 지원)
      const res = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-goog-api-key": apiKey },
          body,
        }
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

/* ── 관대한 JSON 파서 ────────────────────────────────────────────
 * 응답이 토큰 한도로 중간에 잘리거나, 따옴표·제어문자가 어긋나도
 * 복구를 시도한다. 어떤 경우에도 JSON.parse 원시 오류를 밖으로
 * 던지지 않는다(실패 시 null → 호출부에서 자동 재시도). */
function tryParse(t) {
  try {
    const v = JSON.parse(t);
    return v && typeof v === "object" ? v : undefined;
  } catch {
    return undefined;
  }
}

// 문자열 내부 제어문자를 이스케이프하면서 괄호·문자열 상태를 추적
function cleanScan(t) {
  let out = "";
  const stack = [];
  let inStr = false;
  let esc = false;
  for (let i = 0; i < t.length; i++) {
    const c = t[i];
    if (inStr) {
      if (esc) {
        esc = false;
        out += c;
      } else if (c === "\\") {
        esc = true;
        out += c;
      } else if (c === '"') {
        inStr = false;
        out += c;
      } else if (c === "\n") out += "\\n";
      else if (c === "\r") continue;
      else if (c === "\t") out += "\\t";
      else out += c;
      continue;
    }
    if (c === '"') {
      inStr = true;
      out += c;
    } else if (c === "{" || c === "[") {
      stack.push(c === "{" ? "}" : "]");
      out += c;
    } else if (c === "}" || c === "]") {
      stack.pop();
      out += c;
    } else out += c;
  }
  return { out, stack, inStr };
}

// 열린 문자열/괄호를 닫아서 파싱 가능한 형태로 마감
function closeUp(t) {
  const { out, stack, inStr } = cleanScan(t);
  let s = out;
  if (inStr) s += '"';
  for (let i = stack.length - 1; i >= 0; i--) {
    s = s.replace(/,\s*$/, "").replace(/"[^"]*"\s*:\s*$/, "").replace(/,\s*$/, "");
    s += stack[i];
  }
  return s;
}

function repairJson(raw) {
  let t = String(raw ?? "").trim().replace(/```(json)?/gi, "").trim();
  const s = t.indexOf("{");
  if (s > 0) t = t.slice(s);
  if (!t.startsWith("{")) return null;
  let v = tryParse(t) || tryParse(closeUp(t));
  if (v) return v;
  // 문자열 밖 콤마 위치를 모아 뒤에서부터 잘라 가며 복구
  const commas = [];
  let inStr = false;
  let esc = false;
  for (let i = 0; i < t.length; i++) {
    const c = t[i];
    if (inStr) {
      if (esc) esc = false;
      else if (c === "\\") esc = true;
      else if (c === '"') inStr = false;
    } else if (c === '"') inStr = true;
    else if (c === ",") commas.push(i);
  }
  for (let k = commas.length - 1, n = 0; k >= 0 && n < 80; k--, n++) {
    v = tryParse(closeUp(t.slice(0, commas[k])));
    if (v) return v;
  }
  return null;
}

function parseResult(text) {
  const v = repairJson(text);
  if (v) return v;
  // 마지막 안전망: 원문에서 핵심 필드만 직접 추출
  const pick = (key) => {
    const m = String(text ?? "").match(new RegExp(`"${key}"\\s*:\\s*"((?:[^"\\\\]|\\\\.)*)`));
    return m ? m[1].replace(/\\n/g, "\n").replace(/\\"/g, '"').replace(/\\\\/g, "\\") : "";
  };
  const opinion = pick("opinion");
  if (opinion.trim()) {
    return { name: pick("name"), participation: pick("participation") || "적극", answers: [], opinion: opinion.trim() };
  }
  return null;
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
  return `${d.getFullYear()}. ${p(d.getMonth() + 1)}. ${p(d.getDate())}`;
}

// 직전 관리번호에서 다음 번호를 제안 (예: 2026-080 → 2026-081)
function suggestNextDocNo(prev) {
  const m = String(prev || "").match(/^(.*?)(\d+)\s*$/);
  if (m) {
    const n = String(Number(m[2]) + 1).padStart(m[2].length, "0");
    return m[1] + n;
  }
  return `${new Date().getFullYear()}-`;
}

// 생년월일 6자리(YYMMDD) → 연나이 (통보서 표기 방식: 올해 - 출생연도)
function calcAge(birth6) {
  const yy = Number(String(birth6).slice(0, 2));
  const now = new Date().getFullYear();
  const year = 2000 + yy > now ? 1900 + yy : 2000 + yy;
  return now - year;
}

const DEFAULT_SESSIONS = [
  { date: "", content: "오리엔테이션 및 미술치료(이수)", hours: "3시간" },
  { date: "", content: "독서치료를 통한 감정표현 프로그램(이수)", hours: "4시간" },
  { date: "", content: "공감능력 및 자아존중감 향상 프로그램(이수)", hours: "3시간" },
];

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
  const [toast, setToast] = useState("");

  // 통보서(최종 제출 문서) 정보 — 기관·프로그램 정보는 기기에 저장해 재사용
  const [form, setForm] = useState(() => {
    let saved = {};
    try {
      saved = JSON.parse(localStorage.getItem("report_form") || "{}");
    } catch (e) {}
    return {
      recipient: saved.recipient || "삼산 경찰서",
      docNo: suggestNextDocNo(saved.docNo),
      birth: "",
      age: "",
      job: "중학생",
      offense: "특별교육",
      org: saved.org || "(사단법인)한국청소년지원센터장",
      sessions: saved.sessions && saved.sessions.length ? saved.sessions : DEFAULT_SESSIONS,
    };
  });
  const setF = (k, v) => setForm((f) => ({ ...f, [k]: v }));
  const setSessionRow = (i, k, v) =>
    setForm((f) => ({ ...f, sessions: f.sessions.map((s, j) => (j === i ? { ...s, [k]: v } : s)) }));

  useEffect(() => {
    localStorage.setItem("counselor_name", counselor);
  }, [counselor]);

  // 원클릭 키 등록: 주소 뒤에 #key=AIza... 를 붙여 열면 키가 자동 저장됩니다.
  // (키는 주소창의 # 뒤에만 있어 서버로 전송되지 않으며, 저장 즉시 주소에서 지웁니다)
  useEffect(() => {
    const m = location.hash.match(/[#&]key=([^&\s]+)/);
    if (m) {
      const k = decodeURIComponent(m[1]).trim();
      if (k) {
        localStorage.setItem("gemini_api_key", k);
        setApiKey(k);
        setToast("✓ API 키가 자동으로 저장되었어요. 이제 그냥 쓰시면 됩니다!");
        setTimeout(() => setToast(""), 6000);
      }
      history.replaceState(null, "", location.pathname + location.search);
    }
  }, []);

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
      // 응답 JSON이 잘리거나 어긋나면 복구하고, 그래도 안 되면 한 번 더 자동 재시도
      let parsed = null;
      let lastErr = null;
      for (let attempt = 0; attempt < 2 && !parsed; attempt++) {
        try {
          const text = await callGeminiVision(prompt, images, apiKey);
          parsed = parseResult(text);
          if (parsed && !String(parsed.opinion || "").trim()) parsed = null;
        } catch (e) {
          lastErr = e;
          if (/API 키/i.test(e.message || "")) throw e;
        }
      }
      if (!parsed) {
        throw lastErr || new Error("AI 응답을 정리하지 못했어요. 잠시 후 버튼을 한 번만 다시 눌러 주세요.");
      }
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

  // 통보서에 들어갈 전체 데이터
  const reportData = () => ({
    ...form,
    name,
    participation: result?.participation || "적극",
    opinion: result?.opinion || "",
    counselor,
    issueDate: dateStr,
  });

  const saveFormDefaults = () => {
    localStorage.setItem(
      "report_form",
      JSON.stringify({ recipient: form.recipient, docNo: form.docNo, org: form.org, sessions: form.sessions })
    );
  };

  const downloadDocx = async () => {
    try {
      saveFormDefaults();
      await downloadReportDocx(reportData());
      setToast("✓ 파일이 저장되었어요. 한글2020에서 열어 확인하세요!");
      setTimeout(() => setToast(""), 5000);
    } catch (e) {
      setError("파일 생성 오류: " + (e.message || e));
    }
  };


  return (
    <div style={{ fontFamily: KR, background: C.bg, minHeight: "100vh", color: C.ink }}>
      {/* 헤더 */}
      <header
        className="no-print"
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

      <main className="no-print" style={{ maxWidth: 640, margin: "0 auto", padding: "16px 16px 120px" }}>
        {/* 설정 패널 */}
        {showSettings && (
          <Card>
            <Label>🔑 Gemini API 키</Label>
            <div style={{ display: "flex", gap: 8 }}>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="발급받은 키 붙여넣기 (AIza… 또는 AQ.…)"
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
            {apiKey && (
              <div style={{ fontSize: 12.5, color: C.green, marginTop: 8, fontWeight: 700 }}>
                ✓ 키가 등록되어 있어요
              </div>
            )}
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
              {/* capture 속성을 빼서 카메라/갤러리를 선택할 수 있게 한다 */}
              <input
                type="file"
                accept="image/*"
                multiple
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

            {/* STEP 4: 통보서 완성 */}
            <Card>
              <StepTitle n="4" t="통보서 완성 (한글 제출용)" />
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                <Field label="수신 (경찰서)">
                  <input value={form.recipient} onChange={(e) => setF("recipient", e.target.value)} style={inputStyle} />
                </Field>
                <Field label="관리번호">
                  <input value={form.docNo} onChange={(e) => setF("docNo", e.target.value)} placeholder="예: 2026-081" style={inputStyle} />
                </Field>
                <Field label="생년월일 (6자리)">
                  <input
                    value={form.birth}
                    inputMode="numeric"
                    onChange={(e) => {
                      const v = e.target.value;
                      setForm((f) => ({ ...f, birth: v, age: /^\d{6}$/.test(v) ? String(calcAge(v)) : f.age }));
                    }}
                    placeholder="예: 100803"
                    style={inputStyle}
                  />
                </Field>
                <Field label="나이 (자동계산)">
                  <input value={form.age} onChange={(e) => setF("age", e.target.value)} style={inputStyle} />
                </Field>
                <Field label="직업">
                  <input value={form.job} onChange={(e) => setF("job", e.target.value)} placeholder="예: 중학생" style={inputStyle} />
                </Field>
                <Field label="비행내용">
                  <input value={form.offense} onChange={(e) => setF("offense", e.target.value)} placeholder="예: 특별교육" style={inputStyle} />
                </Field>
              </div>

              <div style={{ marginTop: 14 }}>
                <Label>교육내용 (일자 · 내용 · 시간)</Label>
                {form.sessions.map((s, i) => (
                  <div key={i} style={{ display: "grid", gridTemplateColumns: "86px 1fr 62px", gap: 6, marginBottom: 6 }}>
                    <input
                      value={s.date}
                      onChange={(e) => setSessionRow(i, "date", e.target.value)}
                      placeholder="07월08일"
                      style={{ ...inputStyle, padding: "9px 8px", fontSize: 13 }}
                    />
                    <input
                      value={s.content}
                      onChange={(e) => setSessionRow(i, "content", e.target.value)}
                      style={{ ...inputStyle, padding: "9px 10px", fontSize: 13 }}
                    />
                    <input
                      value={s.hours}
                      onChange={(e) => setSessionRow(i, "hours", e.target.value)}
                      placeholder="3시간"
                      style={{ ...inputStyle, padding: "9px 8px", fontSize: 13 }}
                    />
                  </div>
                ))}
              </div>

              <div style={{ marginTop: 8 }}>
                <Field label="발급 기관장 명의">
                  <input value={form.org} onChange={(e) => setF("org", e.target.value)} style={inputStyle} />
                </Field>
              </div>

              <div style={{ marginTop: 14 }}>
                <button onClick={downloadDocx} style={{ ...btnPrimary, width: "100%", padding: "13px" }}>
                  📄 한글용 통보서 파일 받기
                </button>
              </div>
              <div style={{ fontSize: 12, color: C.inkSubtle, marginTop: 10, lineHeight: 1.55 }}>
                받은 파일(.docx)은 한글2020에서 바로 열립니다. 내용 확인 후 저장·출력하고, 직인은 기존 방식대로
                날인해 주세요. 수신·관리번호·교육내용은 다음에도 자동으로 기억됩니다.
              </div>
            </Card>

            <button onClick={generate} disabled={loading} style={{ ...btnGhost, width: "100%", padding: "13px", marginTop: 10 }}>
              🔄 다시 생성
            </button>
          </div>
        )}
      </main>

      {toast && (
        <div
          className="no-print"
          style={{
            position: "fixed",
            bottom: 28,
            left: "50%",
            transform: "translateX(-50%)",
            background: C.green,
            color: "#fff",
            padding: "13px 22px",
            borderRadius: 999,
            fontSize: 14.5,
            fontWeight: 700,
            boxShadow: "0 6px 20px rgba(0,0,0,0.22)",
            zIndex: 50,
            maxWidth: "92vw",
            textAlign: "center",
          }}
        >
          {toast}
        </div>
      )}
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

/* ── 인쇄 전용 통보서 (화면에는 숨김, 인쇄할 때만 A4 양식으로 표시) ── */
function PrintSheet({ data }) {
  const td = { border: "1px solid #000", padding: "4px 7px", textAlign: "center", verticalAlign: "middle" };
  const th = { ...td, fontWeight: 700 };
  const p = data.participation || "적극";
  const mark = (v) => (p === v ? "✔" : "   ");
  const sessions = [...(data.sessions || [])];
  while (sessions.length < 5) sessions.push({ date: "", content: "", hours: "" });
  const opinionParas = String(data.opinion || "").split(/\n+/).filter((t) => t.trim());
  return (
    <div
      className="print-sheet"
      style={{ fontFamily: "'Batang', '바탕', serif", color: "#000", fontSize: "10.5pt", lineHeight: 1.55 }}
    >
      <div style={{ textAlign: "center", fontSize: "15pt", fontWeight: 800, marginBottom: "5mm" }}>
        「전문기관 연계 선도프로그램(사랑의 교실)」 교육결과 통보서
      </div>
      <table style={{ borderCollapse: "collapse", width: "100%", tableLayout: "fixed" }}>
        <colgroup>
          {Array.from({ length: 24 }).map((_, i) => (
            <col key={i} style={{ width: `${100 / 24}%` }} />
          ))}
        </colgroup>
        <tbody>
          <tr>
            <td colSpan={4} style={th}>수    신</td>
            <td colSpan={8} style={td}>{data.recipient}</td>
            <td colSpan={4} style={th}>관리번호</td>
            <td colSpan={8} style={td}>{data.docNo}</td>
          </tr>
          <tr>
            <td colSpan={24} style={th}>인    적    사    항</td>
          </tr>
          <tr>
            <td colSpan={4} style={th}>성    명</td>
            <td colSpan={4} style={td}>{data.name}</td>
            <td colSpan={4} style={th}>생년월일</td>
            <td colSpan={4} style={td}>{data.birth}</td>
            <td colSpan={4} style={th}>나    이</td>
            <td colSpan={4} style={td}>{data.age}</td>
          </tr>
          <tr>
            <td colSpan={4} style={th}>직    업</td>
            <td colSpan={8} style={td}>{data.job}</td>
            <td colSpan={4} style={th}>비행내용</td>
            <td colSpan={8} style={td}>{data.offense}</td>
          </tr>
          <tr>
            <td colSpan={24} style={th}>교    육    내    용</td>
          </tr>
          <tr>
            <td colSpan={4} style={th}>교육일자</td>
            <td colSpan={14} style={th}>내용 및 결과</td>
            <td colSpan={3} style={th}>운영시간</td>
            <td colSpan={3} style={th}>강사명</td>
          </tr>
          {sessions.map((s, i) => (
            <tr key={i}>
              <td colSpan={4} style={td}>{s.date || "월      일"}</td>
              <td colSpan={14} style={{ ...td, textAlign: "left" }}>{s.content}</td>
              <td colSpan={3} style={td}>{s.hours}</td>
              <td colSpan={3} style={td}>{s.date || s.content ? data.counselor : ""}</td>
            </tr>
          ))}
          <tr>
            <td colSpan={24} style={th}>종    합    의    견</td>
          </tr>
          <tr>
            <td colSpan={4} style={th}>참여태도</td>
            <td colSpan={20} style={{ ...td, textAlign: "left" }}>
              {`적극(  ${mark("적극")}  ),      보통(  ${mark("보통")}  ),      소극(  ${mark("소극")}  )`}
            </td>
          </tr>
          <tr>
            <td colSpan={4} style={th}>의    견</td>
            <td colSpan={20} style={{ ...td, textAlign: "left", height: "85mm", padding: "8px 10px" }}>
              {opinionParas.map((t, i) => (
                <div key={i} style={{ textAlign: "justify", marginBottom: "3mm", textIndent: "0.5em" }}>
                  {t}
                </div>
              ))}
              <div style={{ textAlign: "right", marginTop: "6mm" }}>상담사    {data.counselor}      </div>
            </td>
          </tr>
          <tr>
            <td colSpan={24} style={{ ...td, fontSize: "12pt", padding: "7px" }}>{data.issueDate}</td>
          </tr>
          <tr>
            <td colSpan={24} style={{ ...td, fontSize: "15pt", fontWeight: 800, padding: "8px" }}>{data.org}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default function App() {
  return (
    <ErrBoundary>
      <AppInner />
    </ErrBoundary>
  );
}
