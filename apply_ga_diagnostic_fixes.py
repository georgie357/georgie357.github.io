# -*- coding: utf-8 -*-
r"""
apply_ga_diagnostic_fixes.py — implements fixes 1-3 from GA_Diagnostic_v1.pdf
(documents/george/intelligenthome/ in household tasks) on georgealexandervela.com.

What this does, across the 50 real blog posts (the 34 blog-hercules-* files are
intentional redirect stubs from the 8 Aug 2026 consolidation and are skipped):

1. Book CTA correctness + cover thumbnails. Every post gets linked to the book
   whose own plot actually contains that myth (per books.html's blurbs), not a
   generic default. Posts about a myth with no matching book link to books.html
   instead. Both the existing end-of-post CTA and a new/repositioned mid-article
   CTA get a real cover-image thumbnail (previously text-only).
2. Mid-article CTA moved to the true midpoint of the essay (paragraph count / 2),
   not wherever it happened to land before (often 1/4 of the way in, or missing
   entirely — blog-trojan-horse.html and blog-circe.html had none at all).
3. Newsletter copy sitewide changed from "...infrequent and worth reading" to a
   monthly-cadence line, across every page that embeds the Brevo/Sendinblue form.

Run from: C:\Users\User\Documents\georgie357.github.io\
  python apply_ga_diagnostic_fixes.py
Prints a per-file change log. Does NOT commit/push — that's a separate explicit step.
"""

import glob
import re
from pathlib import Path

REPO = Path(r"C:\Users\User\Documents\georgie357.github.io")

# ---------------------------------------------------------------------------
# Book metadata (from books.html) — the only source of truth for CTAs.
# ---------------------------------------------------------------------------
BOOKS = {
    "bellerophon": dict(
        title="The Fall from Heaven: The Myth of Bellerophon and Pegasus",
        page="bellerophon.html", asin="B0GT8PBGVZ", cover="img/bellerophon.jpg",
        hook="Hubris, the gods, and the long fall that follows.",
    ),
    "hercules": dict(
        title="Hercules and the Cradle of Thunder",
        page="hercules.html", asin="B0GSX1RH2V", cover="img/hercules.webp",
        hook="The labours as they actually happen \u2014 bare-handed, up close, human.",
    ),
    "hound-of-troy": dict(
        title="The Hound of Troy: The Vengeance of Hecuba",
        page="hound-of-troy.html", asin="B0GTT3H55D", cover="img/hound-of-troy.webp",
        hook="Troy's fall from inside the walls, and the people the epics rush past.",
    ),
    "amazons-end": dict(
        title="The Amazon's End: The Tragedy of Penthesilea",
        page="amazons-end.html", asin="B0GV1VDJNV", cover="img/amazons-end.webp",
        hook="The war seen from the losing side, and the women written out of it.",
    ),
    "dragons-teeth": dict(
        title="The Dragon's Teeth: A Tale of Cadmus and the Founding of Thebes",
        page="dragons-teeth.html", asin="B0D7K5J71W", cover="img/dragons-teeth.webp",
        hook="Cadmus, the serpent, and the city grown from its teeth.",
    ),
    "architect-of-ithaca": dict(
        title="The Architect of Ithaca: The Man Odysseus Erased",
        page="architect-of-ithaca.html", asin="B0HH2YD5J4", cover="img/architect-of-ithaca.webp",
        hook="This is the trial and the man behind it, in full.",
    ),
    "backward-glance": dict(
        title="The Backward Glance: The Descent of Orpheus",
        page="books.html#backward-glance", asin="B0HHHY7GGV", cover="img/backward-glance.jpg",
        hook="The most famous walk in Greek myth, told step by step, doubt by doubt.",
    ),
}

# filename (without .html) -> book key, or None = no matching book -> books.html
POST_BOOK_MAP = {
    # hercules.html — labours + infancy, all literally in the book's plot
    "blog-augean-stables": "hercules",
    "blog-baby-hercules": "hercules",
    "blog-cretan-bull": "hercules",
    "blog-erymanthian-boar": "hercules",
    "blog-golden-hind": "hercules",
    "blog-hydra": "hercules",
    "blog-king-eurystheus": "hercules",
    "blog-nemean-lion": "hercules",
    "blog-stymphalian-birds": "hercules",
    "blog-twelve-labours-of-hercules": "hercules",
    "blog-hercules-he-strangled-two-snakes-in-his-cradle-be": "hercules",
    # dragons-teeth.html — Cadmus's own founding story
    "blog-cadmus": "dragons-teeth",
    "blog-cadmus-kills-dragon": "dragons-teeth",
    "blog-dragon-spring": "dragons-teeth",
    "blog-harmonia": "dragons-teeth",
    "blog-harmonia-necklace": "dragons-teeth",
    "blog-oracle-delphi": "dragons-teeth",
    "blog-spartoi": "dragons-teeth",
    "blog-white-bull": "dragons-teeth",
    # hound-of-troy.html — Hecuba's family / the fall of Troy she survives
    "blog-cassandra": "hound-of-troy",
    "blog-clytemnestra": "hound-of-troy",
    "blog-hector": "hound-of-troy",
    "blog-hecuba-troy": "hound-of-troy",
    "blog-trojan-horse": "hound-of-troy",
    # amazons-end.html — Achilles kills Penthesilea; Patroclus's death drives him there
    "blog-achilles-patroclus": "amazons-end",
    "blog-who-was-penthesilea": "amazons-end",
    # bellerophon.html — Medusa's blood literally makes Pegasus, the book's other lead
    "blog-real-myth-bellerophon": "bellerophon",
    "blog-medusa": "bellerophon",
    # architect-of-ithaca.html — Palamedes is the book's title character
    "blog-palamedes": "architect-of-ithaca",
    # backward-glance (Orpheus's own book — was wrongly pointing elsewhere/missing)
    "blog-furies": "backward-glance",
    "blog-orpheus-eurydice": "backward-glance",
    # blind-exile already correctly self-referential (books.html#blind-exile) —
    # special-cased below (no live ASIN yet, uses the author storefront link)
    "blog-blind-exile": "BLIND_EXILE",
    # No dedicated book covers these myths -> Books page, not a forced match
    "blog-actaeon": "NONE",
    "blog-arachne": "NONE",
    "blog-circe": "NONE",
    "blog-cronus": "NONE",
    "blog-erysichthon": "NONE",
    "blog-harpies": "NONE",
    "blog-ixion": "NONE",
    "blog-jason-medea": "NONE",
    "blog-lycaon": "NONE",
    "blog-minotaur": "NONE",
    "blog-niobe": "NONE",
    "blog-persephone": "NONE",
    "blog-prometheus": "NONE",
    "blog-sisyphus": "NONE",
    "blog-tantalus": "NONE",
    "blog-theseus-minotaur": "NONE",
    "blog-thyestes": "NONE",
    "blog-tithonus": "NONE",
}


def extract_balanced_div(html, start_idx):
    """Given the index of a '<div' opening tag, return (full_div_text, end_idx)
    for the tag and everything up to and including its matching </div>."""
    depth = 0
    i = start_idx
    tag_re = re.compile(r"<div\b|</div>")
    while True:
        m = tag_re.search(html, i)
        if not m:
            raise ValueError("unbalanced div")
        if m.group() == "<div":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = m.end()
                return html[start_idx:end], end
        i = m.end()


def build_thumb_end_cta(title, page, asin, cover, h3, p_html):
    return (
        f'<div class="post-cta">\n'
        f'      <div style="display:flex;gap:1.25rem;align-items:flex-start;flex-wrap:wrap">\n'
        f'        <img src="{cover}" alt="{title} \u2014 cover" width="90" loading="lazy" '
        f'style="width:90px;height:auto;border-radius:3px;flex-shrink:0;box-shadow:0 2px 8px rgba(0,0,0,0.35)">\n'
        f'        <div style="flex:1;min-width:220px">\n'
        f'          <h3 style="margin-top:0">{h3}</h3>\n'
        f'          <p>{p_html}</p>\n'
        f'          <div style="display:flex;gap:1rem;flex-wrap:wrap">\n'
        f'            <a href="{page}" class="btn btn-outline">About the Book</a>\n'
        f'            <a href="https://www.amazon.com/dp/{asin}?tag=georgevela-20" class="btn btn-primary" target="_blank" rel="noopener">Buy on Amazon</a>\n'
        f'          </div>\n'
        f'        </div>\n'
        f'      </div>\n'
        f'    </div>'
    )


def build_series_end_cta():
    return (
        '<div class="post-cta">\n'
        '      <h3>Explore the Full Series</h3>\n'
        '      <p>This myth isn\u2019t the subject of one of my ten novels \u2014 but if this is the kind of '
        'retelling you like, faithful to the ancient sources and told in one voice, the full '
        '<em>Myths of the Ancient World</em> series is built the same way.</p>\n'
        '      <div style="display:flex;gap:1rem;flex-wrap:wrap">\n'
        '        <a href="books.html" class="btn btn-primary">See All 10 Books \u2192</a>\n'
        '      </div>\n'
        '    </div>'
    )


def build_inline_cta(book_key):
    if book_key == "NONE":
        return ('<p class="post-cta-inline">If you like this kind of myth, told the same way: '
                '<a href="books.html">browse the full ten-book series \u2192</a></p>')
    if book_key == "BLIND_EXILE":
        return (
            '<p class="post-cta-inline"><img src="img/blind-exile.jpg" alt="" width="30" loading="lazy" '
            'style="width:30px;height:auto;vertical-align:middle;border-radius:2px;margin-right:0.5rem">'
            'The investigation, the exile, and the walk to Colonus, in full. That\u2019s my new novel '
            '<a href="books.html#blind-exile">The Blind Exile</a>. '
            '<a href="https://www.amazon.com/stores/George-Vela/author/B0GTC4ZMWC" target="_blank" rel="noopener">Coming to Amazon \u2192</a></p>'
        )
    b = BOOKS[book_key]
    return (
        f'<p class="post-cta-inline"><img src="{b["cover"]}" alt="" width="30" loading="lazy" '
        f'style="width:30px;height:auto;vertical-align:middle;border-radius:2px;margin-right:0.5rem">'
        f'{b["hook"]} That\u2019s my novel <a href="{b["page"]}">{b["title"].split(":")[0]}</a>. '
        f'<a href="https://www.amazon.com/dp/{b["asin"]}?tag=georgevela-20" target="_blank" rel="noopener">Read it on Amazon \u2192</a></p>'
    )


def process_post(fname, book_key):
    path = REPO / fname
    html = path.read_text(encoding="utf-8")
    orig = html
    changes = []

    # ---- 1. Remove any existing inline CTA (we rebuild it at the true midpoint) ----
    html, n = re.subn(r'\s*<p class="post-cta-inline">.*?</p>\n?', '\n', html, count=1, flags=re.S)
    if n:
        changes.append("removed old inline CTA")

    # ---- 2. Rebuild the end-of-post CTA ----
    div_start = html.find('<div class="post-cta">')
    if div_start == -1:
        raise ValueError(f"{fname}: no post-cta div found")
    old_div, div_end = extract_balanced_div(html, div_start)

    if book_key == "NONE":
        new_div = build_series_end_cta()
        changes.append("end CTA -> Books page (no matching book)")
    elif book_key == "BLIND_EXILE":
        h3_m = re.search(r"<h3>(.*?)</h3>", old_div, re.S)
        p_m = re.search(r"<p>(.*?)</p>", old_div, re.S)
        h3 = h3_m.group(1) if h3_m else "The Blind Exile: The Fall of Oedipus"
        p_html = p_m.group(1) if p_m else "Submitted for Kindle review; live this week."
        new_div = (
            '<div class="post-cta">\n'
            '      <div style="display:flex;gap:1.25rem;align-items:flex-start;flex-wrap:wrap">\n'
            '        <img src="img/blind-exile.jpg" alt="The Blind Exile cover" width="90" loading="lazy" '
            'style="width:90px;height:auto;border-radius:3px;flex-shrink:0;box-shadow:0 2px 8px rgba(0,0,0,0.35)">\n'
            f'        <div style="flex:1;min-width:220px">\n'
            f'          <h3 style="margin-top:0">{h3}</h3>\n'
            f'          <p>{p_html}</p>\n'
            '          <div style="display:flex;gap:1rem;flex-wrap:wrap">\n'
            '            <a href="books.html#blind-exile" class="btn btn-outline">About the Book</a>\n'
            '            <a href="https://www.amazon.com/stores/George-Vela/author/B0GTC4ZMWC" class="btn btn-primary" target="_blank" rel="noopener">Coming to Amazon</a>\n'
            '          </div>\n'
            '        </div>\n'
            '      </div>\n'
            '    </div>'
        )
        changes.append("end CTA -> added thumbnail (blind-exile, already correctly targeted)")
    else:
        b = BOOKS[book_key]
        # Was this post already pointing at the correct book? If so, keep its
        # bespoke h3/p copy — just add the cover thumbnail. Otherwise regenerate.
        already_correct = f'href="{b["page"]}"' in old_div or (
            "#" in b["page"] and f'href="{b["page"]}"' in old_div
        )
        h3_m = re.search(r"<h3>(.*?)</h3>", old_div, re.S)
        p_m = re.search(r"<p>(.*?)</p>", old_div, re.S)
        if already_correct and h3_m and p_m:
            h3, p_html = h3_m.group(1), p_m.group(1)
            changes.append(f"end CTA -> kept existing {book_key} copy, added thumbnail")
        else:
            h3 = b["title"]
            p_html = b["hook"] + " Told in full in this novel."
            changes.append(f"end CTA -> regenerated, now correctly points to {book_key}")
        new_div = build_thumb_end_cta(b["title"], b["page"], b["asin"], b["cover"], h3, p_html)

    html = html[:div_start] + new_div + html[div_end:]

    # ---- 3. Insert the new inline CTA at the true midpoint of the essay ----
    body_start = html.find('<div class="post-body">')
    cta_start = html.find('<div class="post-cta">')
    region = html[body_start:cta_start]
    para_matches = list(re.finditer(r"<p>.*?</p>", region, re.S))
    inline_html = build_inline_cta(book_key)
    if not para_matches:
        # fallback: right before the end CTA
        html = html[:cta_start] + inline_html + "\n\n    " + html[cta_start:]
    else:
        mid = len(para_matches) // 2
        insert_at_region = para_matches[mid].end()
        insert_at = body_start + insert_at_region
        html = html[:insert_at] + "\n\n" + inline_html + html[insert_at:]
    changes.append(f"inline CTA inserted at paragraph {mid + 1 if para_matches else 0}/{len(para_matches)}")

    if html != orig:
        path.write_text(html, encoding="utf-8")
        print(f"[{fname}] " + "; ".join(changes))
    else:
        print(f"[{fname}] no change")


def main():
    for stem, book_key in POST_BOOK_MAP.items():
        fname = stem + ".html"
        if not (REPO / fname).exists():
            print(f"[{fname}] MISSING, skipped")
            continue
        process_post(fname, book_key)

    # ---------------------------------------------------------------------
    # 4. Newsletter copy, sitewide: replace every "...infrequent and worth
    #    reading" variant with a monthly-cadence line.
    # ---------------------------------------------------------------------
    NEW_COPY = "New myth retellings, monthly \u2014 plus notes on the ancient sources behind them."
    variants = [
        "New essays, new books, notes on the mythology \u2014 infrequent and worth reading.",
        "New essays, new books, notes on the mythology &#x2014; infrequent and worth reading.",
        "New essays, new books, notes on the mythology &mdash; infrequent and worth reading.",
        "New essays, new books, notes on the mythology &#8212; infrequent and worth reading.",
        "New books, notes on the mythology, and dispatches from the series \u2014 infrequent and worth reading.",
    ]
    newsletter_files = 0
    for fname in glob.glob(str(REPO / "*.html")):
        p = Path(fname)
        txt = p.read_text(encoding="utf-8")
        new_txt = txt
        for v in variants:
            new_txt = new_txt.replace(v, NEW_COPY)
        if new_txt != txt:
            p.write_text(new_txt, encoding="utf-8")
            newsletter_files += 1
    print(f"\nNewsletter copy updated in {newsletter_files} files (standard variants).")


if __name__ == "__main__":
    main()
