/* ============================================================
   George Alexander Vela — Author Website
   main.js
   ============================================================ */

/* --- Mobile Navigation --- */
(function () {
  const toggle = document.querySelector('.nav-toggle');
  const links  = document.querySelector('.nav-links');
  if (!toggle || !links) return;

  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    toggle.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open);
  });

  // Close on link click
  links.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      links.classList.remove('open');
      toggle.classList.remove('open');
      toggle.setAttribute('aria-expanded', false);
    });
  });
})();

/* --- Active Nav Link --- */
(function () {
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === page || (page === '' && href === 'index.html') ||
        (page === 'index.html' && href === 'index.html')) {
      a.classList.add('active');
    }
  });
})();

/* --- Scroll Fade-In --- */
(function () {
  const els = document.querySelectorAll('.fade-in');
  if (!els.length) return;

  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    els.forEach(el => obs.observe(el));
  } else {
    els.forEach(el => el.classList.add('visible'));
  }
})();

/* --- Nav shadow on scroll --- */
(function () {
  const nav = document.querySelector('.site-nav');
  if (!nav) return;
  window.addEventListener('scroll', () => {
    nav.style.boxShadow = window.scrollY > 20
      ? '0 4px 30px rgba(0,0,0,0.5)'
      : 'none';
  }, { passive: true });
})();

/* --- Mailing List Form Handler --- */
(function () {
  const forms = document.querySelectorAll('.mailing-form, .mailing-inline, .mailing-signup-form');
  forms.forEach(form => {
    form.addEventListener('submit', function (e) {
      // If action URL is a placeholder, prevent default and show message
      const action = form.getAttribute('action') || '';
      if (!action || action.includes('YOUR_MAILCHIMP') || action === '#') {
        e.preventDefault();
        const input = form.querySelector('input[type="email"]');
        const btn   = form.querySelector('button[type="submit"]');
        if (input && input.value) {
          if (btn) {
            const orig = btn.textContent;
            btn.textContent = 'Thank you!';
            btn.disabled = true;
            input.value = '';
            setTimeout(() => {
              btn.textContent = orig;
              btn.disabled = false;
            }, 3000);
          }
        }
      }
      // Otherwise let the form submit to the real Mailchimp/ConvertKit URL
    });
  });
})();

/* --- Amazon Click Tracking --- */
(function () {
  document.addEventListener('click', function (e) {
    const link = e.target.closest('a[href*="amazon.com"]');
    if (!link) return;
    if (typeof gtag !== 'function') return;
    const url  = link.getAttribute('href') || '';
    const asin = (url.match(/\/dp\/([A-Z0-9]{10})/) || [])[1] || '';
    const text = (link.textContent || '').trim();
    gtag('event', 'amazon_click', {
      link_url:  url,
      asin:      asin,
      link_text: text,
      page_path: location.pathname
    });
  });
})();

/* --- Contact Form Handler --- */
(function () {
  const form = document.querySelector('.contact-form');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    const action = form.getAttribute('action') || '';
    if (!action || action === '#' || action.includes('YOUR_FORM')) {
      e.preventDefault();
      const btn  = form.querySelector('.form-submit .btn');
      const name = form.querySelector('[name="name"]');
      if (btn) {
        const orig = btn.textContent;
        btn.textContent = 'Message received — thank you.';
        btn.disabled = true;
        form.reset();
        setTimeout(() => {
          btn.textContent = orig;
          btn.disabled = false;
        }, 4000);
      }
    }
  });
})();
