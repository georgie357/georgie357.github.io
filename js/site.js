// site.js — consolidated inline scripts for CSP compliance.
// Replaces three inline blocks (canonical redirect, GA4 config, footer year)
// with one external file so CSP can drop 'unsafe-inline' from script-src.

(function () {
  'use strict';

  // 1. Canonical redirect — if browser landed on a non-canonical path,
  //    rewrite to the canonical href declared in <link rel="canonical">.
  try {
    var canon = document.querySelector('link[rel="canonical"]');
    if (canon && canon.href) {
      var canonPath = new URL(canon.href).pathname;
      var here = window.location.pathname;
      // Normalise trailing slash for the homepage
      var hereNorm = here === '' ? '/' : here;
      if (canonPath && hereNorm !== canonPath && !window.location.search) {
        // Avoid loops by checking we're actually on a different path
        if (hereNorm.replace(/\/+$/, '/') !== canonPath.replace(/\/+$/, '/')) {
          window.location.replace(canonPath + window.location.hash);
          return;
        }
      }
    }
  } catch (_) {}

  // 2. Google Analytics 4 init
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', 'G-ZCDJHG9Q5Y');

  // 3. Footer year
  function setYear() {
    var el = document.getElementById('footer-year');
    if (el) el.textContent = new Date().getFullYear();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setYear);
  } else {
    setYear();
  }
})();
