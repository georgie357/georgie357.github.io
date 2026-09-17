// stub-redirect.js — used ONLY by the Hercules redirect-stub pages (the old video-linked
// blog-hercules-*.html URLs kept alive for YouTube descriptions).
//
// Why: a bare <meta refresh> makes the stub itself the referrer of the real post, and GA4
// ignores same-site referrers — so every YouTube click through a stub was being reported as
// "Direct". This forwards the visitor exactly as before but labels where they came from.
// The meta refresh stays in a <noscript> as the no-JS fallback. Added 17 Sep 2026.
(function () {
  'use strict';
  var canon = document.querySelector('link[rel="canonical"]');
  if (!canon || !canon.href) return;
  var target = new URL(canon.href).pathname;
  var host = '';
  try { host = document.referrer ? new URL(document.referrer).hostname : ''; } catch (_) {}
  var utm = '';
  if (host.indexOf('georgealexandervela.com') === -1) {
    var se = /(google|bing|duckduckgo|yahoo|ecosia|brave|yandex|baidu)\./.exec(host);
    if (se) {
      utm = '?utm_source=' + se[1] + '&utm_medium=organic';
    } else if (host && !/youtube\.com$|youtu\.be$/.test(host)) {
      utm = '?utm_source=' + encodeURIComponent(host) + '&utm_medium=referral';
    } else {
      // YouTube referrer, or none at all (the YouTube app sends no referrer)
      utm = '?utm_source=youtube&utm_medium=video&utm_campaign=hercules_video_links';
    }
  }
  window.location.replace(target + utm + window.location.hash);
})();
