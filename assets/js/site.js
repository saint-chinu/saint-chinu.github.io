// リンクコピーとカード扇の角度。どちらも無くてもページは成り立つ。
document.querySelectorAll("[data-copy]").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var url = btn.getAttribute("data-copy");
    var done = function () {
      var t = btn.textContent;
      btn.textContent = "コピーしました";
      setTimeout(function () { btn.textContent = t; }, 1800);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(done, function () { window.prompt("このリンクをコピーしてください", url); });
    } else {
      window.prompt("このリンクをコピーしてください", url);
    }
  });
});
document.querySelectorAll(".cardfan li").forEach(function (li, i, all) {
  var mid = (all.length - 1) / 2;
  li.style.setProperty("--i", String(i - mid + 4));
  li.style.setProperty("--d", String(Math.round(Math.pow(i - mid, 2) * 2.2)));
});
