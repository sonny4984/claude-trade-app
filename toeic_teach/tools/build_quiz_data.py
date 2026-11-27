"""폰 퀴즈 앱 데이터: 동하 오답(data/progress.json)에 해당하는 내 문제 은행 문항 + 변형(TEST 38·39) + 유형별 P5 뭉텅이.
ETS/1000제 원문은 넣지 않는다(전부 새로 쓴 문항). -> app/quiz_data.json"""
import glob, importlib, json, os, random, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
src = open(ROOT / "tools/make_bulk_drill.py", encoding="utf-8").read()
ns = {"re": re}; exec(src[src.index("TYPES = ["):src.index("# ---------- 1)")], ns)
classify, TYPES = ns["classify"], ns["TYPES"]
prog = json.load(open(ROOT / "data/progress.json", encoding="utf-8"))
wrong = {}
for k, v in prog.items():
    m = re.match(r"(t\d+|m\d)-(\d+)$", k)
    if m and any(h.get("result") == "wrong" for h in v.get("history", [])):
        mod = m.group(1).replace("m1", "mock1").replace("m2", "mock2")
        wrong[(mod, int(m.group(2)))] = " / ".join(h["note"] for h in v["history"] if h.get("note"))[:160]
rng = random.Random(39)
L = "ABCD"
def place(it):
    stem, ch, note = it[0], it[1], it[2]
    p = it[3] if len(it) == 4 else rng.randrange(4)
    opts = ch if len(it) == 4 else ch[1:p + 1] + [ch[0]] + ch[p + 1:]
    def mp(m):
        j = L.index(m.group(1)); return "(" + L[p if j == 0 else (j - 1 if j - 1 < p else j)]
    if len(it) != 4: note = re.sub(r"\(([ABCD])(?=[ )])", mp, note)
    stem = re.sub(r",? ?line \{LINE:\w+\},?", "", stem)
    return {"s": stem, "o": opts, "a": p, "n": note}
def clean(t): return re.sub(r"\[\[(.+?)\]\]", r"<u>\1</u>", t)
def passage_html(p):
    h = []
    if p.get("url"): h.append(f'<div class="url">{p["url"]}</div>')
    if p.get("site"): h.append(f'<div class="url">{p["site"]}</div>')
    if p.get("title"): h.append(f'<h4>{p["title"]}</h4>')
    if p.get("byline"): h.append(f'<p class="by">{p["byline"]}</p>')
    if p.get("hdr"): h.append('<div class="hdr">' + "".join(f"<div><b>{a}</b> {b}</div>" for a, b in p["hdr"]) + "</div>")
    intro = p.get("intro")
    for t in (intro if isinstance(intro, list) else [intro] if intro else []): h.append(f"<p>{clean(t)}</p>")
    if p.get("rows"):
        r = p["rows"]
        if r and isinstance(r[0], (list, tuple)):
            h.append('<div class="tw"><table>' + "".join("<tr>" + "".join(f"<{'th' if i == 0 else 'td'}>{c}</{'th' if i == 0 else 'td'}>" for c in row) + "</tr>" for i, row in enumerate(r)) + "</table></div>")
    for key in ("body", "col1", "col2"):
        for t in p.get(key, []) or []:
            if isinstance(t, str): h.append(f"<p>{clean(t)}</p>")
    if p.get("list_title"): h.append(f"<p><b>{p['list_title']}</b></p>")
    if p.get("bullets"): h.append("<ul>" + "".join(f"<li>{b}</li>" for b in p["bullets"]) + "</ul>")
    for t in p.get("after", []) or []: h.append(f"<p>{clean(t)}</p>")
    if p.get("quote"): h.append(f"<p><i>{p['quote']}</i></p>")
    if p.get("msgs"): h.append("".join(f'<div class="msg"><b>{a}</b> <span>{b}</span><br>{c}</div>' for a, b, c in p["msgs"]))
    return "".join(h) or "<p>(지문 형식을 표시할 수 없음)</p>"
p5_mine, p5_type, p6, p7s, p7m = [], {n: [] for n, _, _ in TYPES}, [], [], []
ALWAYS = {"t38", "t39"}
for f in sorted(glob.glob(str(ROOT / "tools/*_items.py"))):
    name = os.path.basename(f)[:-3]
    if name in ("check_items", "p5_items"): continue
    mod = importlib.import_module(name); short = name.replace("_items", "")
    for i, it in enumerate(getattr(mod, "PART5", [])):
        if len(it) < 3 or len(it[1]) != 4: continue
        q = place(it); q["id"] = f"{short}-{101 + i}"; q["t"] = classify(it[2])
        if (short, 101 + i) in wrong or short in ALWAYS:
            q["w"] = wrong.get((short, 101 + i), ""); p5_mine.append(q)
        elif q["t"] in p5_type: p5_type[q["t"]].append(q)
    for si, s in enumerate(getattr(mod, "PART6", [])):
        lo = 131 + si * 4; nums = range(lo, lo + len(s["qs"]))
        hit = [n for n in nums if (short, n) in wrong]
        if not hit and short not in ALWAYS: continue
        if "body" not in s: continue  # mock1/2 use an older block format
        body = "".join(f"<p>{t}</p>" for t in s["body"])
        for n in range(131, 147): body = body.replace("{%d}" % n, f'<b class="bl">__{n}__</b>')
        head = (f"<h4>{s['title']}</h4>" if s.get("title") else "") + ('<div class="hdr">' + "".join(f"<div><b>{a}:</b> {b}</div>" for a, b in s["hdr"]) + "</div>" if s.get("hdr") else "")
        qs = []
        for n, it in zip(nums, s["qs"]):
            q = place(it); q["id"] = f"{short}-{n}"; q["s"] = f"빈칸 {n}"; q["w"] = wrong.get((short, n), ""); q["hit"] = n in hit; qs.append(q)
        p6.append({"id": f"{short}-{lo}", "kind": s["intro"], "tabs": [{"l": s["intro"], "h": head + body}], "qs": qs})
    n = 147
    for s in getattr(mod, "PART7", []):
        n = s.get("start", n); nums = list(range(n, n + len(s["qs"]))); n += len(s["qs"])
        hit = [x for x in nums if (short, x) in wrong]
        if not hit and short not in ALWAYS: continue
        kinds = [k.strip() for k in re.split(r",| and ", s["intro"]) if k.strip()]
        tabs = [{"l": (kinds[i] if i < len(kinds) and len(kinds) == len(s["passages"]) else f"지문 {i + 1}"), "h": passage_html(p)} for i, p in enumerate(s["passages"])]
        qs = []
        for x, it in zip(nums, s["qs"]):
            q = place(it); q["id"] = f"{short}-{x}"; q["w"] = wrong.get((short, x), ""); q["hit"] = x in hit; qs.append(q)
        (p7m if len(tabs) > 1 else p7s).append({"id": f"{short}-{nums[0]}", "kind": s["intro"], "tabs": tabs, "qs": qs})
# P5 Test A-H (tools/p5_items.py): tA ids are positional; others are matched by the English words in the logged note
import p5_items as _p5
for k, v in prog.items():
    m = re.match(r"t([A-H])-(\d+)$", k)
    if not m or not any(h.get("result") == "wrong" for h in v.get("history", [])): continue
    T = getattr(_p5, "TEST_" + m.group(1), []); note = " / ".join(h["note"] for h in v["history"] if h.get("note"))
    it = None
    if m.group(1) == "A":
        i = int(m.group(2)) - 101; it = T[i] if 0 <= i < len(T) else None
    else:
        words = set(w.lower() for w in re.findall(r"[A-Za-z]{3,}", note))
        best = max(T, key=lambda x: len(words & set(w.lower() for w in re.findall(r"[A-Za-z]{3,}", x[0] + " " + x[1][0] + " " + x[2]))), default=None)
        if best and len(words & set(w.lower() for w in re.findall(r"[A-Za-z]{3,}", best[0] + " " + best[1][0] + " " + best[2]))) >= 2: it = best
    if it and len(it[1]) == 4:
        q = place(it); q["id"] = k; q["t"] = classify(it[2]); q["w"] = note[:160]; p5_mine.append(q)
for v in p5_type.values(): rng.shuffle(v)
data = {"p5_mine": p5_mine, "p5_type": [{"name": n, "algo": a, "qs": p5_type[n][:40]} for n, a, _ in TYPES], "p6": p6, "p7s": p7s, "p7m": p7m}
out = ROOT / "app/quiz_data.json"; out.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
print("p5_mine", len(p5_mine), "p5_type", sum(len(x["qs"]) for x in data["p5_type"]), "p6 sets", len(p6), sum(len(s["qs"]) for s in p6),
      "p7 single", len(p7s), sum(len(s["qs"]) for s in p7s), "p7 multi", len(p7m), sum(len(s["qs"]) for s in p7m), out.stat().st_size // 1024, "KB")
print("unmapped wrong ids:", sorted(k for k in wrong if not any(q["id"] == f"{k[0]}-{k[1]}" for q in p5_mine + [q for s in p6 + p7s + p7m for q in s["qs"]]))[:40])
