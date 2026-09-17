"""Contact-page refresh, 17 Sep 2026: drop the reading-guide offer, list all 11 books,
add a 'how did you find us' question, Quick Answers + Start Here strip, CSS-based hover
(the old inline onmouseover was blocked by CSP), and pass enquiry type to GA's generate_lead."""
import re

p = 'contact.html'
s = open(p, encoding='utf-8').read()


def rep(a, b):
    # whitespace-tolerant literal match (file mixes indentation / CRLF)
    global s
    parts = [re.escape(x) for x in a.split()]
    pat = r'\s+'.join(parts)
    s, n = re.subn(pat, lambda _: b, s, count=1)
    assert n == 1, a[:70]


rep("For reading groups, media enquiries, and everything else. Responses are prompt and personal.",
    "For readers, media and podcast enquiries, booksellers and librarians. Every message is read personally and answered within two working days.")

s, n = re.subn(
    r'<p class="contact-text">\s*Reading group questions.*?</p>\s*<p class="contact-text">\s*For media enquiries.*?</p>\s*<p class="contact-text">\s*Librarians and booksellers.*?</p>',
    """<p class="contact-text">
            Readers first: if one of the books stayed with you, or you have a question about a source, a scene, or a choice I made, write. Those are the messages I most enjoy answering.
          </p>
          <p class="contact-text">
            Media, podcasts and features: interviews about the series, Greek myth, or writing from the ancient sources are welcome. A short bio is on the <a href="about.html">About page</a>, every cover is on the <a href="books.html">Books page</a>, and the full catalogue is on my <a href="https://www.amazon.com/stores/George-Vela/author/B0GTC4ZMWC?tag=georgevela-20" target="_blank" rel="noopener noreferrer">Amazon author page</a>.
          </p>
          <p class="contact-text">
            Booksellers and librarians: review copies of any title are available as an ebook on request, and I am glad to answer questions about stocking or featuring the series. Rights and translation enquiries are also welcome.
          </p>""", s, count=1, flags=re.S)
assert n == 1

rep("""<span class="contact-detail-label">Reading Groups</span>
                <span class="contact-detail-value">Discussion guides available on request for all six books.</span>""",
    """<span class="contact-detail-label">Media &amp; Podcasts</span>
                <span class="contact-detail-value">Interviews and features welcome. Bio on the <a href="about.html">About page</a>; covers on the <a href="books.html">Books page</a>.</span>""")
rep("""<span class="contact-detail-value">Available on Amazon in ebook (Kindle), free with Kindle Unlimited.</span>""",
    """<span class="contact-detail-value">Eleven novels on Amazon in ebook (Kindle), free with Kindle Unlimited. Two are also available in Spanish.</span>""")

rep("All messages are read personally. For reading group enquiries please mention which book (or books) you are working with.",
    "All messages are read personally. If your message is about a particular book, choose it below so I can answer properly.")

rep("""<option value="reading-group">Reading group enquiry</option>
                  <option value="media">Media / press enquiry</option>
                  <option value="bookseller">Bookseller / librarian</option>
                  <option value="general">General message</option>
                  <option value="other">Other</option>""",
    """<option value="reader">A message about the books</option>
                  <option value="media">Media / podcast / press</option>
                  <option value="bookseller">Bookseller / librarian</option>
                  <option value="rights">Rights / translation</option>
                  <option value="other">Other</option>""")

rep("""<option value="fall-from-heaven">The Fall from Heaven (Book I)</option>
                  <option value="hercules">Hercules and the Cradle of Thunder (Book II)</option>
                  <option value="hound-of-troy">The Hound of Troy (Book III)</option>
                  <option value="amazons-end">The Amazon's End (Book IV)</option>
                  <option value="dragons-teeth">The Dragon's Teeth (Book V)</option>""",
    """<optgroup label="The Trojan War Cycle">
                    <option value="brothers-bow">The Brother's Bow</option>
                    <option value="ash-spear">The Ash Spear</option>
                    <option value="architect-of-ithaca">The Architect of Ithaca</option>
                    <option value="amazons-end">The Amazon's End</option>
                    <option value="hound-of-troy">The Hound of Troy</option>
                  </optgroup>
                  <optgroup label="The Theban Cycle">
                    <option value="blind-exile">The Blind Exile</option>
                    <option value="dragons-teeth">The Dragon's Teeth</option>
                  </optgroup>
                  <optgroup label="Heroes &amp; Journeys">
                    <option value="gorgons-reflection">The Gorgon's Reflection</option>
                    <option value="backward-glance">The Backward Glance</option>
                    <option value="hercules">Hercules and the Cradle of Thunder</option>
                    <option value="fall-from-heaven">The Fall from Heaven</option>
                  </optgroup>
                  <optgroup label="En español">
                    <option value="lanza-de-fresno">La lanza de fresno</option>
                    <option value="arquitecto-de-itaca">El arquitecto de Ítaca</option>
                  </optgroup>""")

rep("""<div class="form-group">
                <label for="message">Message</label>""",
    """<div class="form-group">
                <label for="found">How did you find the books? (optional)</label>
                <select id="found" name="found">
                  <option value="">— choose one —</option>
                  <option value="amazon">Browsing Amazon / Kindle Unlimited</option>
                  <option value="search">A web search</option>
                  <option value="youtube">YouTube</option>
                  <option value="instagram">Instagram</option>
                  <option value="friend">A friend or family member</option>
                  <option value="library">A library or bookshop</option>
                  <option value="other">Somewhere else</option>
                </select>
              </div>
              <div class="form-group">
                <label for="message">Message</label>""")

marker = """    <!-- ============================================================
         FOLLOW THE SERIES"""
rep(marker, """    <!-- ============================================================
         QUICK ANSWERS + START HERE
         ============================================================ -->
    <section class="container" style="padding: 3rem 0 0">
      <div class="contact-grid">
        <div>
          <span class="section-label">Before You Write</span>
          <h2 class="section-title" style="font-size:1.7rem">Quick Answers</h2>
          <dl class="quick-answers">
            <dt>How fast will I hear back?</dt>
            <dd>Within two working days, from me, not an assistant.</dd>
            <dt>Where can I buy the books?</dt>
            <dd>All eleven novels are on Amazon as Kindle ebooks and free to read with Kindle Unlimited. <em>The Ash Spear</em> and <em>The Architect of Ithaca</em> are also published in Spanish.</dd>
            <dt>Which book should I start with?</dt>
            <dd>Any of them stands alone. Readers who want the Trojan War from the beginning start with <a href="books.html">The Brother's Bow</a>; readers who want one hero's whole life start with <a href="hercules.html">Hercules and the Cradle of Thunder</a>.</dd>
            <dt>How do I hear about the next release?</dt>
            <dd>Join the mailing list above. You get <em>The Centaur's Gift</em> free at once and one email a month after that.</dd>
          </dl>
        </div>
        <div>
          <span class="section-label">Start Here</span>
          <h2 class="section-title" style="font-size:1.7rem">While You're Here</h2>
          <div class="start-here">
            <a class="social-card" href="free-book.html">
              <img src="img/centaurs-gift.jpg" alt="" width="44" loading="lazy">
              <div><span class="social-card-label">Free novel</span><span>The Centaur's Gift, free when you join the list</span></div>
            </a>
            <a class="social-card" href="free.html">
              <div><span class="social-card-label">Read a sample</span><span>Opening chapters from the series, free to read online</span></div>
            </a>
            <a class="social-card" href="blog-trojan-horse.html">
              <div><span class="social-card-label">Most-read essay</span><span>Is the Trojan Horse in the Iliad? What Homer actually wrote</span></div>
            </a>
            <a class="social-card" href="blog-circe.html">
              <div><span class="social-card-label">Also popular</span><span>Circe in the Odyssey: the witch who turned men into pigs</span></div>
            </a>
          </div>
        </div>
      </div>
    </section>

""" + marker)

s, n1 = re.subn(r'<a href="(https://www\.instagram\.com/mythsoftheancientworld)" target="_blank" rel="noopener noreferrer"\s*style="[^"]*"\s*onmouseover="[^"]*"\s*onmouseout="[^"]*">',
                r'<a class="social-card" href="\1" target="_blank" rel="noopener noreferrer">', s)
s, n2 = re.subn(r'<a href="(https://www\.youtube\.com/@GeorgeAlexanderVela)" target="_blank" rel="noopener noreferrer"\s*style="[^"]*"\s*onmouseover="[^"]*"\s*onmouseout="[^"]*">',
                r'<a class="social-card" href="\1?utm_source=website&amp;utm_medium=contact&amp;utm_campaign=youtube_channel" target="_blank" rel="noopener noreferrer">', s)
assert n1 == 1 and n2 == 1
s = s.replace('<span style="display:block;font-family:var(--ff-small-caps);font-size:0.68rem;letter-spacing:0.18em;text-transform:uppercase;color:var(--gold-dark);margin-bottom:0.15rem">', '<span class="social-card-label">')
s = s.replace('<span style="font-size:0.9rem">@', '<span>@')
s = s.replace('Mythology notes, series updates, and fragments of research — shared on Instagram and YouTube.',
              'Short myth videos, series updates, and fragments of research — on YouTube and Instagram.')
assert 'onmouseover' not in s
open(p, 'w', encoding='utf-8', newline='').write(s)

css = open('css/style.css', encoding='utf-8').read()
assert css.count("/* --- Forms --- */") == 1
css = css.replace("/* --- Forms --- */", """/* --- Contact: social / start-here cards + quick answers --- */
.social-card {
  display: inline-flex;
  align-items: center;
  gap: 0.9rem;
  padding: 0.9rem 1.25rem;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 4px;
  color: var(--text-muted);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color var(--transition), border-color var(--transition), background var(--transition);
}
.social-card:hover,
.social-card:focus-visible {
  color: var(--gold);
  border-color: var(--gold-dark);
  background: var(--gold-faint);
}
.social-card svg { flex-shrink: 0; }
.social-card img { width: 44px; height: auto; border-radius: 2px; flex-shrink: 0; }
.social-card-label {
  display: block;
  font-family: var(--ff-small-caps);
  font-size: 0.68rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold-dark);
  margin-bottom: 0.15rem;
}
.start-here { display: flex; flex-direction: column; gap: 0.75rem; }
.quick-answers { margin: 0; }
.quick-answers dt {
  font-family: var(--ff-small-caps);
  font-size: 0.72rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--gold-dark);
  margin-top: 1.4rem;
}
.quick-answers dt:first-child { margin-top: 0; }
.quick-answers dd {
  margin: 0.35rem 0 0;
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.75;
}
.quick-answers a { color: var(--gold); }

/* --- Forms --- */""", 1)
open('css/style.css', 'w', encoding='utf-8', newline='').write(css)

m = open('js/main.js', encoding='utf-8').read()
a = """  form.addEventListener('submit', function (e) {
    const action = form.getAttribute('action') || '';"""
b = """  form.addEventListener('submit', function (e) {
    // Remember what kind of enquiry this was so site.js can attach it to the
    // generate_lead event on thanks.html (Formspree's redirect can't carry it).
    try {
      ['subject', 'book', 'found'].forEach(function (k) {
        const el = form.querySelector('[name="' + k + '"]');
        if (el && el.value) sessionStorage.setItem('ga_contact_' + k, el.value);
      });
    } catch (_) {}
    const action = form.getAttribute('action') || '';"""
assert m.count(a) == 1
open('js/main.js', 'w', encoding='utf-8', newline='').write(m.replace(a, b))

j = open('js/site.js', encoding='utf-8').read()
a = """        gtag('event', 'generate_lead', { method: leadMethod });"""
b = """        var lead = { method: leadMethod };
        if (leadMethod === 'contact_form') {
          // set by js/main.js on the contact form's submit; tells GA what kind of enquiry it was
          var subj = sessionStorage.getItem('ga_contact_subject');
          var book = sessionStorage.getItem('ga_contact_book');
          var found = sessionStorage.getItem('ga_contact_found');
          if (subj) lead.enquiry_type = subj;
          if (book) lead.book = book;
          if (found) lead.found_via = found;
        }
        gtag('event', 'generate_lead', lead);"""
assert j.count(a) == 1
open('js/site.js', 'w', encoding='utf-8', newline='').write(j.replace(a, b))
print("ok")
