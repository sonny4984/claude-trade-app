"""Pre-release checks for an items module, from the 11/6 measurement of real tests (data/analysis/real_3tests_measured.md).
Usage: python3 tools/check_items.py t30_items
Flags: Part 7 questions whose correct option is the single longest (real: 12%), and P6 passages outside 60-140 words."""
import importlib, re, sys
sys.path.insert(0, "tools")
m = importlib.import_module(sys.argv[1])
W = lambda t: re.findall(r"[A-Za-z0-9$'’-]+", re.sub(r"<[^>]+>|\{\d+\}|\{LINE:\w+\}|\[\[|\]\]", " ", t))
bad, n = [], 0
for s in getattr(m, "PART7", []):
    for q in s["qs"]:
        if len(q) == 4 or "closest in meaning" in q[0]:
            continue
        L = [len(W(x)) for x in q[1]]
        n += 1
        if L[0] == max(L) and L.count(L[0]) == 1:
            bad.append(q[1][0])
if n:
    print(f"P7 correct option uniquely longest: {len(bad)}/{n} ({100 * len(bad) // n}%, real 12%)")
    for b in bad:
        print("   -", b)
for s in getattr(m, "PART6", []):
    w = sum(len(W(t)) for t in s["body"])
    if not 60 <= w <= 140:
        print(f"P6 passage '{s.get('title', s['intro'])}': {w} words (real 60-140)")
