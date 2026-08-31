# SITE-REVIEW.md — Post-Deploy Audit, georgealexandervela.com

Full audit of the **live** site as a visitor/search engine sees it — sitemap crawl, every internal link
and anchor, image/schema/meta correctness, sales-claim truth-checks against real Amazon listings,
newsletter verification, and blog-freshness consistency. All fixes below are committed on `main`,
**not pushed yet** (per instructions). Ordered by impact on a reader or a buyer, not by page.

---

## FIXED — mechanical, one commit per class

### 1. Dead Amazon link for an entire book (highest impact)
Every "Buy on Amazon" button, schema `isbn`/`url`/`offers`, and mid-essay book-pointer for
**Hercules and the Cradle of Thunder** pointed to ASIN `B0GTC4ZMWC`, which 404s on Amazon
("Sorry, we couldn't find that page" — confirmed live). Found the real, live ASIN
(`B0GSX1RH2V`) by searching Amazon directly and confirming via the author's own Amazon
storefront "All Books" listing. Fixed in 17 tracked files (schema + every buy button + every
mid-essay pointer) plus the gitignored `scheduled-posts/week-07-hercules-guilt.html` draft.
`B0GTC4ZMWC` remains correct in exactly one place — the author's Amazon storefront URL
(`/stores/George-Vela/author/B0GTC4ZMWC`), a different identifier that happens to share the string.
— commit `d854673`

### 2. False "ebook and paperback" claims — every book is Kindle-only
Live-checked all 6 books' actual Amazon listings, logged in as the author. **None of the six have
a paperback edition.** Every one is Kindle Edition only, all enrolled in Kindle Unlimited. Fixed 5
false "available in ebook and paperback" claims (about.html, books.html hero, two lines on
contact.html — including a bookseller invitation that specifically referenced paperback stock)
to state the true format. Also fixed blog-harpies.html's post-cta box, a pre-Architect-of-Ithaca
leftover calling The Dragon's Teeth "the concluding volume of the series" and "available... in
paperback" — both false since the series is now six books and ebook-only.
— commits `b40aae0`, and format table below

| Book | Format live on Amazon | KU? |
|---|---|---|
| The Fall from Heaven | Kindle only | Yes |
| Hercules and the Cradle of Thunder | Kindle only | Yes |
| The Hound of Troy | Kindle only | Yes |
| The Amazon's End | Kindle only | Yes |
| The Dragon's Teeth | Kindle only | Yes |
| The Architect of Ithaca (EN) | Kindle only | Yes |
| El arquitecto de Ítaca (ES) | Kindle only | Yes |

### 3. Homepage "Latest Essays" was stale
Showed Palamedes (30 Aug, correct) + The Cretan Bull (3 May) + The Furies (4 May) — both older
than posts that already existed live, including **The Twelve Labours of Hercules** (8 Aug,
genuinely the 2nd-newest essay on the whole site) and **Tithonus** (5 May), neither ever surfaced
there. Replaced Cretan Bull/Furies with Twelve Labours + Tithonus, the true 2nd/3rd newest by
each post's own posted date. (Tithonus was tied on date with Lycaon — picking one over the other
was an editorial call, not a freshness correction.)
— commit `d977176`

### 4. Missing newsletter section
`blog-thyestes.html` was the only real content page (of 59 that should carry it) missing the
mailing-list section entirely — went straight from comments into the footer. Added the standard
block, byte-identical to every sibling post.
— commit `db73849`

### 5. Pre-existing blog-hector.html bug (the outstanding follow-up task)
Fixed as instructed. A stray, unopened `</script>` tag with mangled duplicate GA-init content sat
in the page head; removed it. Confirmed nowhere else on the site.
— commit `4d243c1`

### 6. Image aspect-ratio / dimension mismatches (layout-shift + mis-cropped previews)
`bellerophon.jpg` (native 800×1280, aspect 0.625) and `architect-of-ithaca.webp` (native
1024×1637, aspect 0.6255) were declared everywhere as if they were 2:3 like the site's other four
covers. CSS uses `height:auto` so nothing visibly stretched, but the wrong declared box means the
browser reserves the wrong space before the image loads (a real Core Web Vitals layout shift), and
social platforms crop `og:image` previews to the declared box. Corrected 18 `<img>` occurrences
across 9 files to the true ratio, and `og:image:width/height` on the 10 pages that declare it for
`bellerophon.jpg`. No visible change to the images themselves — just accurate metadata.
— commits `deba1ad`, `6a13053`

### 7. Two oversized images
`img/architect-of-ithaca.webp` (356KB) and `.jpg` (461KB, the `og:image` target) were the only two
covers over the site's ~300KB norm. Re-saved at WEBP quality=82/method=6 → 254KB and JPEG
quality=78/optimize+progressive → 275KB. Pixel dimensions unchanged; verified visually via a
downscaled preview — no visible artifacts.
— commit `705b558`

### 8. 13 meta descriptions over 160 characters
Including one from this week's own Palamedes essay (177 chars). Trimmed each to keep the core
claim and main search phrase; where `og:description`/`twitter:description` matched the meta tag
verbatim, trimmed those identically to avoid creating a new mismatch.
— commit `49ff27f`

---

## VERIFIED CLEAN — checked, nothing wrong

- **Sitemap & crawl:** all 62 sitemap URLs return 200 live; zero dead entries. Full BFS crawl
  (sitemap + everything linked from nav/footer/body) found exactly one page outside the sitemap —
  an intentional pre-existing redirect-shell stub from the Aug 2026 Hercules consolidation,
  correctly excluded by design.
- **Links & anchors:** every internal link on every crawled page resolves. All 63 in-page `#anchor`
  references (including `books.html`'s `#free-book`, confirmed as a genuine same-page anchor) match
  a real `id` on their target page.
- **Images:** every `<img>` has alt text and (now) accurate declared dimensions; no image is
  missing or broken.
- **Schema:** every JSON-LD block across all 63 live pages parses as valid JSON; spot-checked
  several against visible page content; book series `position` (1–6) is consistent across every
  book page, index.html, and books.html.
- **Titles/descriptions:** zero duplicate `<title>` tags and zero duplicate meta descriptions
  across the whole site.
- **Amazon links:** all 7 unique ASINs referenced site-wide (6 English books + the Spanish
  Architect of Ithaca edition) are now confirmed live and correct; every visible "Buy on Amazon"
  link carries `tag=georgevela-20`.
- **Titles vs. Amazon:** every book page's `<title>`, `<h2>`, and subtitle match its real Amazon
  listing title exactly (spot-checked all 6, live).
- **Facts:** Hecuba's "nineteen children" (the canonical Homer/Iliad count you named) is stated
  consistently everywhere it appears (blog-hecuba-troy.html, books.html, hound-of-troy.html).
- **No mixed content:** zero `http://` (non-https) resource references anywhere.
- **Basics:** `robots.txt` is sane and correctly references the sitemap; `404.html` exists and
  serves correctly for broken URLs (confirmed live); favicon present in both `.ico` and `.svg`.
- **Blog freshness:** all 49 essay-craft-pass edits from the last session are confirmed serving
  their new content live (checked every one's new hook against the live HTML).
- **Newsletter:** the Brevo iframe is genuinely embedded (not a raw URL) on all 59/59 pages that
  should carry it — I could not reproduce the "raw URL" symptom you described anywhere, live or in
  the repo. The form itself is live and functional (verified via direct fetch of the iframe's
  source — real email field, submit button, success/error states present). I did **not** submit a
  test entry, since submitting a form needs your explicit go-ahead.
- **Mobile viewport:** verified via source review rather than a rendered screenshot — the
  available browser tool couldn't force a true mobile-width viewport in this environment
  (`window.innerWidth` stayed desktop-sized regardless of the resize call). The CSS breakpoint
  (`@media max-width:640px`, hides `.nav-links`, reveals `.nav-toggle`) and the JS toggle handler
  (`js/main.js`) are both correct and complete, and are identical, unmodified, shared code across
  every page on the site — not something specific to the two newest pages that could plausibly be
  broken there alone. Flagging that this wasn't visually confirmed rather than claiming it was.

---

## FLAGGED — your call, not fixed

1. **bellerophon.jpg and the Architect of Ithaca cover art are genuinely a different shape** than
   the other four covers (0.625/0.6255 aspect vs. true 2:3). I corrected the *metadata* to match
   reality; whether to recrop the actual artwork to match the house 2:3 convention is a creative
   decision.
2. **Your Amazon Author Central page is out of sync with the site.** The "All Books" storefront
   listing shows only 5 titles — Architect of Ithaca isn't there yet — and your author bio (shown
   on every one of your Amazon book pages) still says "His four-book series." Not a website bug,
   but directly surfaced by this review and worth a few minutes on KDP.
3. **blog.html's card-grid dates disagree with the articles themselves** for 3 posts: Arachne,
   Harpies, and Thyestes all show "8 August 2026" on their blog-index card, but their own article
   pages say 29/24/25 April 2026 respectively. I don't know which date is the "true" one (a bulk
   edit on Aug 8 may have touched the cards without meaning to change publish dates, or vice versa),
   so I didn't guess-fix it.
4. **feed.xml only has 14 of the site's 49 real essays** — a much older subset that was never kept
   current (Palamedes is in there at the top from earlier work, but Twelve Labours, Tithonus, and
   33 others never made it in). Bringing it fully current means writing ~35 new `<item>` blocks —
   real content work, out of this pass's mechanical scope.
5. **bellerophon.html's `<title>` tag uses a different pattern** ("The Fall from Heaven — a
   Bellerophon & Pegasus Novel | George Alexander Vela") than the other five book pages (plain
   "Title: Subtitle — George Alexander Vela"). Cosmetic; didn't touch a live-indexed title without
   your sign-off.
6. **Homepage weight** is now ≈930KB (down from ≈1.03MB after this pass's image fixes) for 7
   displayed covers — reasonable, but could go lower still (e.g. converting bellerophon.jpg to
   WebP) if you want to push further.

---

## Three highest-value improvements outside this review's scope

1. **Fix your Amazon Author Central page** — add Architect of Ithaca to "All Books," update the
   stale four-book bio. Zero cost, pure discoverability upside, and this review found it directly.
2. **Bring feed.xml current** (or decide to retire it) — an RSS subscriber right now sees a feed
   frozen months in the past for most of the site's real content.
3. **Apply this review's live-Amazon-verification method to the Spanish edition** and any future
   translations going forward — I did verify `B0HH7V64W2` live as part of this pass (it's correct,
   genuinely live, title matches exactly), but that link was originally added on your say-so
   without a live check at the time; worth making the live-check step standard for every new
   Amazon link before it ships.
