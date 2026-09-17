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

  // 2a. Permanent per-browser analytics opt-out. Visit /?ga_optout=1 once on each of your
  //     own devices and that browser stops sending data for good; /?ga_optout=0 undoes it.
  //     This exists because the GA4 internal-traffic rule matches a home IP address, and a
  //     residential IP changes whenever the ISP reissues one — at which point George's own
  //     browsing silently re-enters the data. (Safe alongside the canonical redirect above:
  //     that block bails out whenever there is a query string, so ?ga_optout is never
  //     stripped before this runs.) Added 22 Aug 2026.
  try {
    var m = /[?&]ga_optout=([01])/.exec(window.location.search);
    if (m) { localStorage.setItem('ga_optout', m[1]); }
    if (localStorage.getItem('ga_optout') === '1') {
      window['ga-disable-G-ZCDJHG9Q5Y'] = true;
    }
  } catch (_) {}

  // 2b. Automated browsers (headless Chrome, Selenium, Puppeteer scrapers) announce themselves
  //     with navigator.webdriver. They are not readers; keep them out of the numbers.
  //     Added 17 Sep 2026.
  if (navigator.webdriver) { window['ga-disable-G-ZCDJHG9Q5Y'] = true; }

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', 'G-ZCDJHG9Q5Y');

  // 2c. Lead conversion, fired exactly ONCE per session.
  //     Previously thank-you.html and thanks.html each carried their own inline gtag block
  //     that re-configured the tag and re-fired generate_lead on every page load. A single
  //     mailing-list signup that loaded thank-you.html twice was therefore recorded as two
  //     generate_lead events — and a GA4 "create event" rule mirrored each into an
  //     email_signup, so one real signup arrived in reports as FOUR key events. The inline
  //     blocks are gone; this fires the event once, guarded by sessionStorage so a refresh
  //     or a back-button return cannot re-count a conversion. Added 22 Aug 2026.
  try {
    var LEAD_PAGES = {
      '/thank-you.html': 'mailing_list',
      '/thanks.html': 'contact_form'
    };
    var leadMethod = LEAD_PAGES[window.location.pathname];
    if (leadMethod) {
      var leadKey = 'ga_lead_fired_' + leadMethod;
      if (!sessionStorage.getItem(leadKey)) {
        sessionStorage.setItem(leadKey, '1');
        var lead = { method: leadMethod };
        if (leadMethod === 'contact_form') {
          // set by js/main.js on the contact form's submit; tells GA what kind of enquiry it was
          var subj = sessionStorage.getItem('ga_contact_subject');
          var book = sessionStorage.getItem('ga_contact_book');
          var found = sessionStorage.getItem('ga_contact_found');
          if (subj) lead.enquiry_type = subj;
          if (book) lead.book = book;
          if (found) lead.found_via = found;
        }
        gtag('event', 'generate_lead', lead);
      }
    }
  } catch (_) {}

  // 2d. Scroll depth on essays. GA4's built-in scroll event fires only at 90% of the page,
  //     and an essay's page is much longer than the essay (CTA, comments, footer), so almost
  //     no reader ever reached it. This sends the same `scroll` event at 25/50/75% too, using
  //     GA4's built-in percent_scrolled parameter, once each per page load. Added 17 Sep 2026.
  try {
    if (/^\/blog-/.test(window.location.pathname)) {
      var marks = [25, 50, 75], ticking = false;
      var onScroll = function () {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(function () {
          ticking = false;
          var doc = document.documentElement;
          var max = doc.scrollHeight - window.innerHeight;
          if (max <= 0) return;
          var pct = (window.scrollY / max) * 100;
          while (marks.length && pct >= marks[0]) {
            gtag('event', 'scroll', { percent_scrolled: marks.shift() });
          }
          if (!marks.length) window.removeEventListener('scroll', onScroll);
        });
      };
      window.addEventListener('scroll', onScroll, { passive: true });
    }
  } catch (_) {}

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
