/* Unit Testing in Python: shared course behaviour.
   1. Syntax colouring + copy buttons for <figure class="code py">
      (Python) and <figure class="code sh"> / <figure class="code toml">
      (terminal commands and settings files).
   2. Multiple-choice quizzes for <section class="quiz" data-quiz="id">.
   3. Progress ticks on the course home page.

   Quiz markup (works without JavaScript too):
     <section class="quiz" data-quiz="lesson-1">
       <ol class="questions">
         <li class="q">
           <p class="stem">Question text</p>
           <ul class="opts">
             <li data-correct>Right answer</li>
             <li>Wrong answer</li>
           </ul>
           <p class="why">Shown after answering.</p>
         </li>
       </ol>
     </section>
*/
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  /* ---------- storage (optional; pages work without it) ---------- */
  var KEY = "python-unit-testing:scores";
  function readScores() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function saveScore(id, right, total) {
    try {
      var s = readScores();
      s[id] = { right: right, total: total };
      localStorage.setItem(KEY, JSON.stringify(s));
    } catch (e) { /* private mode: ignore */ }
  }

  /* ---------- highlighting ---------- */
  var KEYWORDS = /^(def|return|if|elif|else|for|while|in|import|from|as|with|assert|not|and|or|is|None|True|False|raise|try|except|finally|lambda|pass|class)$/;
  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function span(cls, text) {
    return '<span class="tok-' + cls + '">' + esc(text) + "</span>";
  }

  /* Python: comments, strings (with r/b/f prefixes and triple quotes),
     numbers, keywords, and names that are being called. */
  function highlightPython(src) {
    var re = /(#[^\n]*)|((?:[rRbBfF]{1,2})?(?:"""[\s\S]*?"""|'''[\s\S]*?'''|"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'))|(\b\d+\.?\d*(?:e[+-]?\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)(\s*\()?/g;
    var out = "", last = 0, m;
    while ((m = re.exec(src)) !== null) {
      out += esc(src.slice(last, m.index));
      if (m[1]) out += span("c", m[1]);
      else if (m[2]) out += span("s", m[2]);
      else if (m[3]) out += span("n", m[3]);
      else if (KEYWORDS.test(m[4])) out += span("k", m[4]) + esc(m[5] || "");
      else if (m[5]) out += span("f", m[4]) + esc(m[5]);
      else out += esc(m[4]);
      last = re.lastIndex;
    }
    return out + esc(src.slice(last));
  }

  /* Terminal commands and TOML: comments and quoted strings only. */
  function highlightPlain(src) {
    var re = /((?:^|[ \t])#[^\n]*)|("(?:[^"\\\n]|\\.)*"|'[^'\n]*')/gm;
    var out = "", last = 0, m;
    while ((m = re.exec(src)) !== null) {
      out += esc(src.slice(last, m.index));
      out += m[1] ? span("c", m[1]) : span("s", m[2]);
      last = re.lastIndex;
    }
    return out + esc(src.slice(last));
  }

  function addCopyButton(fig, src) {
    var cap = fig.querySelector("figcaption");
    if (!cap || !navigator.clipboard) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(src).then(function () {
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = "Copy"; }, 1500);
      }, function () { btn.textContent = "Select and copy by hand"; });
    });
    cap.appendChild(btn);
  }

  function enhanceCode() {
    [["figure.code.py", highlightPython],
     ["figure.code.sh", highlightPlain],
     ["figure.code.toml", highlightPlain]].forEach(function (pair) {
      document.querySelectorAll(pair[0]).forEach(function (fig) {
        var code = fig.querySelector("pre code");
        if (!code) return;
        var src = code.textContent;
        code.innerHTML = pair[1](src);
        addCopyButton(fig, src);
      });
    });
    document.querySelectorAll(".quiz pre.py code").forEach(function (code) {
      code.innerHTML = highlightPython(code.textContent);
    });
  }

  /* ---------- quizzes ---------- */
  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function buildQuiz(quiz) {
    var id = quiz.getAttribute("data-quiz");
    var questions = Array.prototype.slice.call(quiz.querySelectorAll(".q"));
    var data = questions.map(function (q) {
      return Array.prototype.map.call(q.querySelectorAll(".opts > li"), function (li) {
        return { html: li.innerHTML, correct: li.hasAttribute("data-correct") };
      });
    });
    var tally = document.createElement("div");
    tally.className = "tally";
    tally.setAttribute("aria-live", "polite");
    var status = document.createElement("span");
    var again = document.createElement("button");
    again.type = "button";
    again.textContent = "Try again, reshuffled";
    tally.appendChild(status);
    tally.appendChild(again);
    quiz.appendChild(tally);

    var right, answered;

    function update() {
      if (answered < questions.length) {
        status.textContent = answered + " of " + questions.length + " answered";
        again.hidden = true;
      } else {
        status.textContent = "Score: " + right + " of " + questions.length +
          (right === questions.length ? ". All correct." : ". Reread the explanations, then try again tomorrow.");
        again.hidden = false;
        if (id) saveScore(id, right, questions.length);
      }
    }

    function render() {
      right = 0; answered = 0;
      questions.forEach(function (q, qi) {
        q.classList.remove("answered");
        var why = q.querySelector(".why");
        var old = why && why.querySelector(".verdict");
        if (old) old.remove();
        var ul = q.querySelector(".opts");
        ul.innerHTML = "";
        shuffle(data[qi].slice()).forEach(function (opt, oi) {
          var li = document.createElement("li");
          var b = document.createElement("button");
          b.type = "button";
          b.className = "opt";
          b.innerHTML = '<span class="mark">' + "ABCDEF".charAt(oi) + "</span><span>" + opt.html + "</span>";
          b.addEventListener("click", function () {
            if (q.classList.contains("answered")) return;
            q.classList.add("answered");
            answered++;
            if (opt.correct) right++;
            ul.querySelectorAll("button").forEach(function (other) {
              other.disabled = true;
              if (other._correct) other.classList.add("is-correct");
            });
            if (!opt.correct) b.classList.add("is-wrong");
            if (why) {
              var v = document.createElement("span");
              v.className = "verdict " + (opt.correct ? "good" : "bad");
              v.textContent = opt.correct ? "Correct." : "Not quite.";
              why.insertBefore(v, why.firstChild);
            }
            update();
          });
          b._correct = opt.correct;
          li.appendChild(b);
          ul.appendChild(li);
        });
      });
      update();
    }

    again.addEventListener("click", function () {
      render();
      quiz.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    render();
  }

  /* ---------- home page progress ---------- */
  function showProgress() {
    var scores = readScores();
    document.querySelectorAll("[data-progress]").forEach(function (el) {
      var s = scores[el.getAttribute("data-progress")];
      if (!s) return;
      var tag = document.createElement("span");
      tag.className = "done";
      tag.textContent = "quiz " + s.right + "/" + s.total;
      el.appendChild(tag);
    });
  }

  function init() {
    enhanceCode();
    document.querySelectorAll(".quiz").forEach(buildQuiz);
    showProgress();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
