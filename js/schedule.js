/* Auto-publish scheduled blog cards.
   When a card's data-publish date has arrived AND its target post actually exists,
   flip it from "Scheduled" to live automatically — no manual edit needed.
   Static-site safe: pure client-side, with an existence guard so a scheduled card
   never turns into a broken (404) link if the post has not been written yet. */
(function () {
  var cards = document.querySelectorAll('.blog-card[data-live="false"][data-publish]');
  if (!cards.length) return;

  var today = new Date();
  today.setHours(0, 0, 0, 0);

  cards.forEach(function (card) {
    var d = card.getAttribute('data-publish');
    var pub = new Date(d + 'T00:00:00');
    if (isNaN(pub.getTime()) || pub > today) return; // not due yet

    var link = card.querySelector('.blog-card-title a[data-href], .blog-card-title a.when-live');
    var target = link ? (link.getAttribute('data-href') || link.getAttribute('href')) : null;

    var goLive = function () {
      if (link && link.getAttribute('data-href')) {
        link.setAttribute('href', link.getAttribute('data-href'));
      }
      card.setAttribute('data-live', 'true'); // CSS reveals the live link, hides the "Scheduled" badge
    };

    if (!target) { goLive(); return; }

    // Existence guard: only publish once the post file is actually live.
    fetch(target, { method: 'HEAD' })
      .then(function (r) { if (r.ok) goLive(); })
      .catch(function () { /* offline or missing — stay scheduled */ });
  });
})();
