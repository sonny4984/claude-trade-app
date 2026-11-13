"""quiz_data.json + template.html -> index.html (run tools/build_quiz_data.py first)."""
from pathlib import Path
here = Path(__file__).resolve().parent
d = (here / "quiz_data.json").read_text(encoding="utf-8").replace("</", "<\\/")
t = (here / "template.html").read_text(encoding="utf-8")
(here / "index.html").write_text(t.replace("/*DATA*/", d), encoding="utf-8")
print((here / "index.html").stat().st_size // 1024, "KB")
