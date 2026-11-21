// Two-step quiz: (1) pick the part of speech the blank needs, (2) pick the word.
// Markup: <div class="q" data-pos="noun" data-answer="3" data-why="...">
//           <p class="stem">...</p><div class="word-opts" data-opts='["a","b","c","d"]'></div></div>
(function () {
  var POS = [["noun", "명사"], ["adj", "형용사"], ["adv", "부사"], ["verb", "동사"]];
  var total = 0, correct = 0, done = 0;
  var qs = document.querySelectorAll(".q");
  total = qs.length;

  function button(label, cls) {
    var b = document.createElement("button");
    b.type = "button"; b.textContent = label;
    if (cls) b.className = cls;
    return b;
  }

  qs.forEach(function (q) {
    var posKey = q.dataset.pos;
    var answer = parseInt(q.dataset.answer, 10);
    var why = q.dataset.why;
    var opts = JSON.parse(q.querySelector(".word-opts").dataset.opts);

    var step1 = document.createElement("div");
    step1.innerHTML = '<p class="step">1단계 · 보기를 보지 말고, 빈칸에 필요한 품사는?</p>';
    var row1 = document.createElement("div"); row1.className = "opts";
    var fb = document.createElement("p"); fb.className = "fb";
    var step2 = document.createElement("div"); step2.style.display = "none";
    step2.innerHTML = '<p class="step">2단계 · 그 품사의 단어를 고르세요.</p>';
    var row2 = document.createElement("div"); row2.className = "opts";

    POS.forEach(function (p) {
      var b = button(p[1]);
      b.onclick = function () {
        if (p[0] === posKey) {
          b.className = "ok";
          row1.querySelectorAll("button").forEach(function (x) { x.disabled = true; });
          fb.className = "fb ok"; fb.textContent = "맞아요. 이제 보기를 보세요.";
          step2.style.display = "block";
        } else {
          b.className = "bad"; b.disabled = true;
          fb.className = "fb bad"; fb.textContent = "자리를 다시 보세요. 빈칸 앞뒤 단어가 힌트입니다.";
        }
      };
      row1.appendChild(b);
    });
    step1.appendChild(row1);

    opts.forEach(function (w, i) {
      var b = button(w);
      b.onclick = function () {
        row2.querySelectorAll("button").forEach(function (x) { x.disabled = true; });
        done++;
        if (i === answer) {
          b.className = "ok"; correct++;
          fb.className = "fb ok"; fb.textContent = "정답. " + why;
        } else {
          b.className = "bad";
          row2.querySelectorAll("button")[answer].className = "ok";
          fb.className = "fb bad"; fb.textContent = "오답. " + why;
        }
        if (done === total) {
          document.getElementById("score").textContent = "결과: " + total + "문제 중 " + correct + "문제 정답";
        }
      };
      row2.appendChild(b);
    });
    step2.appendChild(row2);

    q.appendChild(step1); q.appendChild(step2); q.appendChild(fb);
  });
})();
