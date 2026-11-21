"""Compare an items module with the 20 real tests measured on 11/10 (ETS 기출 5 ×10 + 1000제 Vol.4 ×10, OCR).
Usage: python3 tools/measure_real.py t36_items        (needs: pip install wordfreq)
Only numbers from the real tests are kept here (REAL); no real text is stored in the repository.
See data/analysis/real_20tests_measured.md for how each number was obtained."""
import collections, importlib, re, statistics as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
try:
    from wordfreq import zipf_frequency as zf
except ImportError:
    zf = None
REAL = {
 "P5 문장 길이(단어)": 13.6, "P5 긴 단어(9자 이상) %": 15.6, "P5 평균 단어 길이": 5.78, "P5 어휘문제 선지 zipf": 4.76,
 "P5 선지가 모두 한 단어 %": 83,
 "P6 지문 단어수": 99.7, "P6 긴 단어 %": 13.9,
 "P7 2문항 지문": 111.5, "P7 3문항 지문": 147.2, "P7 4문항 지문": 190.4, "P7 이중 지문": 284.7, "P7 삼중 지문": 418.4,
 "P7 문장 길이": 17.4, "P7 25단어 이상 문장 %": 18, "P7 긴 단어 %": 14.2, "P7 평균 단어 길이": 5.6,
 "P7 100단어당 숫자": 4.7, "P7 선지 길이": 5.5, "P7 문장형 선지 %": 44, "P7 선지 긴 단어 %": 17.0,
 "P7 주제/목적": 4.9, "P7 사실확인": 8.3, "P7 추론": 13.8, "P7 세부": 20.5, "P7 동의어": 2.5, "P7 삽입": 2.0, "P7 의도": 1.6,
 "P7 정답 선지-지문 겹침 %": 45, "P7 오답 선지-지문 겹침 %": 41, "P7 오답이 더 겹치는 문항 %": 58, "P7 정답이 혼자 제일 긴 문항 %": 12,
}
def W(t): return re.findall(r"[A-Za-z][A-Za-z'’-]*", t)
def clean(t): return re.sub(r"<[^>]+>|— \[\d\] —|\{LINE:\w+\}|\[\[|\]\]|\{\d+\}|-{3,}", " ", t).replace("&amp;", "&")
def sents(t): return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“])", t) if len(W(s)) >= 3]
def low(ws): return [w.lower() for w in ws if len(w) > 2 and not w[0].isupper()]
def long9(ws): ws = low(ws); return 100 * sum(len(w) >= 9 for w in ws) / max(len(ws), 1)
def wlen(ws): ws = low(ws); return st.mean(len(w) for w in ws)
def zmean(ws):
    if zf is None: return float("nan")
    z = [zf(w, "en") for w in low(ws)]; z = [x for x in z if x > 0]
    return st.mean(z) if z else float("nan")
def qtype(s):
    l = s.lower()
    if "positions marked" in l: return "삽입"
    if "closest in meaning" in l: return "동의어"
    if "NOT" in s: return "NOT"
    if re.search(r"most likely mean|mean when|imply when", l): return "의도"
    if re.search(r"purpose|mainly (about|discuss)|main topic|what is the (article|notice|memo|e-mail|letter|review|report|press release|announcement|information|web page) (mainly )?about|what are the writers (mainly )?discussing|what is being (advertised|announced)", l): return "주제/목적"
    if re.search(r"most likely|probably|suggest|impl|infer|can be concluded", l): return "추론"
    if re.search(r"indicated|mentioned|stated|true about|true of", l): return "사실확인"
    return "세부"
def ptext(p):
    out = []
    for k in ("title", "intro", "body", "col1", "col2", "list_title", "bullets", "after"):
        v = p.get(k)
        if isinstance(v, str): out.append(v)
        elif v: out += v
    out += [f"{a} ({b}) {c}" for a, b, c in p.get("msgs", [])]
    out += [" ".join(r) for r in p.get("rows", [])]
    out += [f"{a} {b}" for a, b in p.get("hdr", [])]
    return [clean(x) for x in out]
STOP = set("that this with from have will your their they them were been about which there would could should into also than then when what other such more most only each some many these those over after before under while where because being does doing done just like".split())
def cw(t): return {w.lower()[:6] for w in W(clean(t)) if len(w) >= 4 and w.lower() not in STOP}
m = importlib.import_module(sys.argv[1])
mine = {}
p5 = getattr(m, "PART5", [])
if p5:
    ws = [w for x in p5 for w in W(x[0])]
    mine["P5 문장 길이(단어)"] = st.mean(len(W(x[0])) for x in p5)
    mine["P5 긴 단어(9자 이상) %"] = long9(ws); mine["P5 평균 단어 길이"] = wlen(ws)
    voc = [x for x in p5 if len({o.lower()[:4] for o in x[1]}) >= 3 and all(len(W(o)) == 1 for o in x[1])]
    mine["P5 어휘문제 선지 zipf"] = zmean([w for x in voc for o in x[1] for w in W(o)])
    mine["P5 선지가 모두 한 단어 %"] = 100 * st.mean(all(len(W(o)) == 1 for o in x[1]) for x in p5)
p6 = getattr(m, "PART6", [])
if p6:
    t = [" ".join(clean(x) for x in s["body"]) + " " + s.get("title", "") for s in p6]
    mine["P6 지문 단어수"] = st.mean(len(W(x)) for x in t); mine["P6 긴 단어 %"] = long9([w for x in t for w in W(x)])
p7 = getattr(m, "PART7", [])
if p7:
    by = collections.defaultdict(list); n = 147; allw = []; sl = []; qs = []; C = []; D = []; trap = longest = k = 0; nums = 0
    for s in p7:
        n = s.get("start", n); nq = len(s["qs"])
        txt = " ".join(x for p in s["passages"] for x in ptext(p)); ws = W(txt); allw += ws
        g = {2: "P7 2문항 지문", 3: "P7 3문항 지문", 4: "P7 4문항 지문"}.get(nq, "P7 이중 지문" if n < 186 else "P7 삼중 지문")
        by[g].append(len(ws)); sl += [len(W(x)) for x in sents(txt)]; nums += len(re.findall(r"\d[\d,.:]*", txt))
        for q in s["qs"]:
            stem = clean(q[0]); qs.append((stem, q[1])); ty = qtype(stem)
            if ty not in ("삽입", "동의어"):
                ci = q[3] if len(q) == 4 else 0  # 4-tuples fix the printed position of the answer
                co = len(cw(q[1][ci]) & cw(txt)) / max(len(cw(q[1][ci])), 1)
                ds = [len(cw(o) & cw(txt)) / max(len(cw(o)), 1) for j, o in enumerate(q[1]) if j != ci]
                C.append(co); D.append(st.mean(ds)); trap += max(ds) > co; k += 1
                L = [len(W(o)) for o in q[1]]; longest += L[ci] == max(L) and L.count(L[ci]) == 1
                if "-v" in sys.argv: print(n + s["qs"].index(q), f"{co:.2f}", " ".join(f"{d:.2f}" for d in ds), "*" if max(ds) > co else "", q[1][ci][:40])
        n += nq
    for g, v in by.items(): mine[g] = st.mean(v)
    mine["P7 문장 길이"] = st.mean(sl); mine["P7 25단어 이상 문장 %"] = 100 * st.mean(x >= 25 for x in sl)
    mine["P7 긴 단어 %"] = long9(allw); mine["P7 평균 단어 길이"] = wlen(allw); mine["P7 100단어당 숫자"] = 100 * nums / len(allw)
    opts = [o for stem, os_ in qs for o in os_ if qtype(stem) not in ("삽입", "동의어")]
    mine["P7 선지 길이"] = st.mean(len(W(o)) for o in opts)
    mine["P7 문장형 선지 %"] = 100 * st.mean(o.strip().endswith(".") for stem, os_ in qs for o in os_)
    mine["P7 선지 긴 단어 %"] = long9([w for stem, os_ in qs for o in os_ for w in W(o)])
    ty = collections.Counter(qtype(stem) for stem, _ in qs)
    for t_ in ("주제/목적", "사실확인", "추론", "세부", "동의어", "삽입", "의도"): mine["P7 " + t_] = ty.get(t_, 0)
    mine["P7 정답 선지-지문 겹침 %"] = 100 * st.mean(C); mine["P7 오답 선지-지문 겹침 %"] = 100 * st.mean(D)
    mine["P7 오답이 더 겹치는 문항 %"] = 100 * trap / k; mine["P7 정답이 혼자 제일 긴 문항 %"] = 100 * longest / k
print(f"{'항목':<28}{'실제 20회':>10}{sys.argv[1]:>14}")
for key, r in REAL.items():
    if key in mine:
        v = mine[key]; flag = "" if r == 0 or abs(v - r) / max(abs(r), 1e-9) <= 0.2 or abs(v - r) <= 1.5 else "  <-- 차이 큼"
        print(f"{key:<28}{r:>10.1f}{v:>14.1f}{flag}")
