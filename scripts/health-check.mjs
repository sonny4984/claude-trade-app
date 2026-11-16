// 주간 점검: 실제 사이트에서 '종합의견 만들기'가 끝까지 되는지 확인한다.
// 사용: GEMINI_KEY=... node scripts/health-check.mjs [사이트주소]
// 1) 사이트 응답  2) 키로 쓸 수 있는 모델 목록과 앱 기본 목록 비교  3) 모델별 실제 응답 속도
// 4) 브라우저로 사진 3장을 올려 종합의견 생성 (실제 사용과 같은 경로)
// 테스트 사진은 합성한 활동지라 개인정보가 없다.
import { readFileSync } from "fs";
import { createRequire } from "module";

const SITE = process.argv[2] || "https://claude-trade-app.vercel.app/";
const KEY = process.env.GEMINI_KEY;
if (!KEY) {
  console.error("GEMINI_KEY 환경변수가 필요합니다.");
  process.exit(2);
}
const API = "https://generativelanguage.googleapis.com/v1beta/models";
const ROOT = new URL("..", import.meta.url).pathname;
const problems = [];
const t = (ms) => (ms / 1000).toFixed(1) + "s";

// 1) 사이트
const page0 = await fetch(SITE);
const bundle = (await page0.text()).match(/assets\/index-[^"]+\.js/)?.[0];
console.log(`[사이트] ${page0.status} · ${bundle}`);
if (!page0.ok || !bundle) problems.push("사이트가 열리지 않음");

// 2) 모델 목록
const appModels = [...readFileSync(ROOT + "src/App.jsx", "utf8").match(/const MODELS = \[([\s\S]*?)\]/)[1].matchAll(/"([^"]+)"/g)].map((m) => m[1]);
const listed = await (await fetch(`${API}?pageSize=200`, { headers: { "X-goog-api-key": KEY } })).json();
if (listed.error) {
  problems.push(`키 오류: ${listed.error.message}`);
  console.log("[키] ❌", listed.error.message);
} else {
  const avail = listed.models.filter((m) => m.supportedGenerationMethods?.includes("generateContent")).map((m) => m.name.replace("models/", ""));
  const gone = appModels.filter((m) => !avail.includes(m));
  console.log(`[모델] 앱 기본 목록 ${appModels.length}개 중 사용 불가: ${gone.join(", ") || "없음"}`);
  if (gone.length > appModels.length / 2) problems.push(`기본 모델 대부분이 없어짐: ${gone.join(", ")}`);
}

// 3) 모델별 속도 (작은 요청)
const png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==";
let fastOk = 0;
for (const m of appModels) {
  const s = Date.now();
  try {
    const r = await fetch(`${API}/${m}:generateContent`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-goog-api-key": KEY },
      signal: AbortSignal.timeout(45000),
      body: JSON.stringify({ contents: [{ parts: [{ text: '{"ok":true} 만 답해' }, { inline_data: { mime_type: "image/png", data: png } }] }] }),
    });
    const j = await r.json();
    console.log(`  ${m.padEnd(24)} ${r.status} ${t(Date.now() - s)} ${r.ok ? "" : (j.error?.message || "").slice(0, 60)}`);
    if (r.ok && Date.now() - s < 10000) fastOk++;
  } catch (e) {
    console.log(`  ${m.padEnd(24)} 무응답 ${t(Date.now() - s)}`);
  }
}
if (!fastOk) problems.push("10초 안에 답하는 기본 모델이 하나도 없음");

// 4) 브라우저 실사용 점검
const { chromium } = createRequire(import.meta.url)("playwright");
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
const errs = [];
const calls = [];
page.on("pageerror", (e) => errs.push(e.message));
await page.addInitScript((k) => localStorage.setItem("gemini_api_key", k), KEY);
// 이 점검 환경의 브라우저는 구글 API에 직접 못 나가므로 Node에서 대신 보내 준다(내용은 그대로)
await page.route("**/generativelanguage.googleapis.com/**", async (route) => {
  const req = route.request();
  const model = req.url().match(/models\/([^:?]+):/)?.[1] || "(목록)";
  const s = Date.now();
  try {
    const res = await fetch(req.url(), { method: req.method(), headers: req.headers(), body: req.postData() });
    calls.push(`${model}→${res.status}(${t(Date.now() - s)})`);
    await route.fulfill({ status: res.status, contentType: "application/json", body: await res.text() });
  } catch {
    calls.push(`${model}→중단`);
    await route.abort("failed").catch(() => {});
  }
});
await page.goto(SITE, { waitUntil: "load" });
const img = readFileSync(ROOT + "scripts/fixtures/worksheet.jpg");
await page.setInputFiles('input[type="file"]', [0, 1, 2].map((i) => ({ name: `p${i}.jpg`, mimeType: "image/jpeg", buffer: img })));
await page.waitForTimeout(1500);
const s = Date.now();
await page.getByRole("button", { name: "종합의견 만들기" }).click();
let opinion = "", shown = "";
for (let i = 0; i < 60 && !opinion; i++) {
  await page.waitForTimeout(2000);
  ({ opinion, shown } = await page.evaluate(() => ({
    opinion: [...document.querySelectorAll("textarea")].map((x) => x.value).find((v) => v.trim().length > 40) || "",
    shown: (document.body.innerText.match(/지금 AI 서버[^\n]*|API 키[^\n]*|오류[^\n]*/) || [""])[0],
  })));
  if (shown && !opinion) break;
}
console.log(`[실사용] ${t(Date.now() - s)} ${opinion ? `✅ 종합의견 ${opinion.length}자` : `❌ ${shown || "결과 없음"}`}`);
console.log(`  호출: ${calls.join(" , ")}`);
if (!opinion) problems.push(`실사용 생성 실패: ${shown || "결과 없음"}`);
if (errs.length) problems.push(`화면 JS 오류: ${errs.join(" / ")}`);
await browser.close();

console.log(problems.length ? `\n❌ 문제 ${problems.length}건\n- ${problems.join("\n- ")}` : "\n✅ 정상");
process.exit(problems.length ? 1 : 0);
