# Blog Post Style Guide — georgealexandervela.com
*Reference for writing new posts, extending the pipeline, or resuming in a new session.*

---

## Voice & Narrator Profile

All posts are written in the voice of **George Alexander Vela** — a literary fiction author who has spent years living inside these myths. The voice is intelligent, measured, and opinionated without being academic or casual.

### What the voice sounds like

- **Register:** Literary nonfiction. Not a textbook. Not a blog post trying to be friendly. The way a very well-read person talks when they're genuinely interested in something and assume you are too.
- **Sentence rhythm:** Long sentences that build through subordinate clauses, then a shorter one that lands the point. The rhythm paces the reader rather than letting them skim.
- **Dry wit:** Occasional — never forced. It emerges from the absurdity the myths contain, not from trying to be entertaining.
- **First person:** Restrained. "I" appears only when the author's perspective as a *novelist* is the actual point — when writing the book changed how they read the myth, or when they hold an opinion the ancient sources don't state outright. Never confessional. Never self-promotional.
- **Argument:** Every post argues something. Not "here is the myth of Medusa summarised." But "Medusa was made into a monster — the myth records the process." The thesis is present from the first paragraph.

### What the voice never does

- Bullet points inside the essay body
- Numbered lists in the prose
- Headers that state obvious things ("Introduction", "Conclusion", "What This Means For You")
- Phrases like "let's explore," "in this post I will," "in conclusion"
- SEO throat-clearing at the top (no "Many people wonder about…")
- Starting with a question as a hook ("Have you ever wondered…?")
- Adjectives that are just enthusiasm ("fascinating," "incredible," "amazing")

### The essay structure

1. **Open mid-thought** — drop the reader into something specific: a detail, a source, a fact that is stranger than expected. No warm-up.
2. **First third:** Establish what the myth actually says, with named ancient sources. Note what survives vs. what is lost.
3. **Second third:** The complication — what the myth doesn't say, what the sources disagree on, what gets left out and why.
4. **Final third:** The author's perspective. What the myth means as a *story*. Why it keeps being told. What it gets wrong and what it gets right.
5. **No conclusion paragraph** that summarises the essay. End on the image or the idea that crystallises the whole thing.

### Source referencing style

Always name the source specifically:
- ✅ "Quintus of Smyrna's *Posthomerica*, written in the third or fourth century AD"
- ✅ "The *Aethiopis* — composed by Arctinus of Miletus, and now almost entirely lost"
- ✅ "Hesiod, in the *Theogony*"
- ❌ "The ancient Greeks believed…"
- ❌ "According to mythology…"

Note when sources are lost, fragmentary, or survive only as summaries. This signals genuine scholarship and is also what AI citation systems look for.

### Length

- Minimum: **600 words** of body essay content (not counting HTML boilerplate)
- Target: **700–900 words**
- Maximum: No hard cap — a post earns its length

---

## SEO Settings (Built Into Every Post)

### Head metadata checklist

| Element | Requirement |
|---|---|
| `<title>` | Primary keyword phrase + " — George Alexander Vela" — under 60 chars |
| `<meta name="description">` | One sentence answering "what is this post about" — under 155 chars — no keyword stuffing |
| `<link rel="canonical">` | Full URL: `https://georgealexandervela.com/blog-SLUG.html` |
| `<meta property="og:type">` | **Must be `"article"`** (not `"website"`) for blog posts |
| `<meta property="og:url">` | Same as canonical |
| `<meta property="og:image">` | `https://georgealexandervela.com/img/amazons-end.jpg` (500×750) |
| `<meta name="twitter:card">` | `"summary_large_image"` |
| `<link rel="icon">` | `img/favicon.svg` |

### Schema.org JSON-LD (BlogPosting)

Every post requires this exact structure — do not abbreviate it:

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "TITLE",
  "description": "META DESCRIPTION TEXT",
  "author": {
    "@type": "Person",
    "@id": "https://georgealexandervela.com/#author",
    "name": "George Alexander Vela",
    "url": "https://georgealexandervela.com"
  },
  "datePublished": "YYYY-MM-DD",
  "dateModified": "YYYY-MM-DD",
  "image": "https://georgealexandervela.com/img/amazons-end.jpg",
  "url": "https://georgealexandervela.com/blog-SLUG.html",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://georgealexandervela.com/blog-SLUG.html"
  },
  "publisher": {
    "@type": "Organization",
    "name": "George Alexander Vela",
    "url": "https://georgealexandervela.com"
  },
  "isPartOf": {
    "@type": "Blog",
    "name": "From the Mythology Notes",
    "url": "https://georgealexandervela.com/blog.html"
  },
  "keywords": ["primary keyword", "secondary keyword", "Greek mythology", "George Alexander Vela"]
}
```

**Critical:** The `"@id": "https://georgealexandervela.com/#author"` must be identical across every post. This persistent ID teaches Google's Knowledge Graph that all posts belong to the same author entity.

### On-page SEO

- **H1:** One per post — the post title (in `<header class="post-header">`)
- **H2:** 2–3 per post — natural subheadings, each targeting a question the post answers
- **Internal links:** 2–4 per post, mapped to topically related live posts. See `POST-LINKS.md` for the current link map.
- **No keyword stuffing:** The primary keyword appears naturally in the title, first paragraph, and at least one H2. Not forced.

---

## AI Citation Optimization

These are the elements that increase the probability Google AI Overviews, Perplexity, and ChatGPT cite a post:

### 1. Original framing (most important)
Every post must argue something that generic sources don't. Wikipedia describes Medusa. This blog argues she was made into a monster. That distinction is what AI systems quote.

**The test:** Could a student find this exact take on Wikipedia or SparkNotes? If yes, rewrite until the answer is no.

### 2. Named primary sources with context
AI systems treat sourced claims as more reliable. Name the ancient text, name the author, note when it was written, note if it's lost or fragmentary. This is the signal that differentiates a scholarly perspective from a myth summary.

### 3. Persistent author entity
The `@id` in Schema.org (see above) + the author's name in the domain + the About page together build a verifiable entity in Google's Knowledge Graph. Once established, AI systems preferentially cite content attached to verified entities.

### 4. Feed accessibility
New posts are added to `feed.xml` immediately. Perplexity, some AI crawlers, and MailerLite all follow the RSS feed. Keeping it current maximises how quickly new posts get indexed by AI systems.

---

## Shareability / Virality Settings

### Title formula
The titles that get clicked and reshared follow a pattern of **expectation gap** — they promise the version of the story people don't know:

- "The Monster Who Was *Made*, Not Born" (not just "Who Was Medusa")
- "The Villain the Myths *Needed* You to Hate" (not just "Clytemnestra")
- "What Homer *Actually* Said" (implies the version you know is incomplete)
- "The Man Who *Knew* He Was Going to Lose" (implies interiority the myth doesn't state)

Words that signal this pattern: *actually, really, never, almost forgot, needed, knew, refused, what they got wrong.*

### Social card settings
- `og:type="article"` → Facebook and Pinterest render it as a content card
- `og:image` with explicit width/height → prevents cropping on shares
- `twitter:card="summary_large_image"` → full-width image on X/Twitter shares

### Giscus comments
Every post has Giscus (GitHub Discussions-backed comments) at the bottom. This creates:
- Return visits when someone replies
- Dwell time signals (readers who comment stay longer)
- Community signal that tells Google the content generates engagement

**Do not remove this block.** The config values (repo ID, category ID) are set for `georgie357/georgie357.github.io` and must remain unchanged:
```html
data-repo="georgie357/georgie357.github.io"
data-repo-id="R_kgDORzcVYg"
data-category="Blog Comments"
data-category-id="DIC_kwDORzcVYs4C5u7R"
```

---

## HTML Template Checklist (per post)

Copy structure from `blog-who-was-penthesilea.html` — it is the canonical template.

```
[ ] <head> — charset, CSP, viewport, title, description, canonical
[ ] <head> — og:type="article", og:url, og:title, og:description, og:image (with width/height)
[ ] <head> — twitter:card, twitter:title, twitter:description, twitter:image
[ ] <head> — favicon (img/favicon.svg)
[ ] <head> — css/style.css
[ ] <head> — Schema.org BlogPosting JSON-LD (full structure, with persistent @id)
[ ] <head> — MailerLite Universal script (account 2229252)
[ ] <nav> — identical nav block (copy exactly)
[ ] <header class="post-header"> — post-meta (category + date), h1, p.post-subtitle
[ ] <main class="container"><div class="post-body">
[ ] Back link: <a href="blog.html" class="post-back">← Back to the blog</a>
[ ] Essay body — minimum 600 words, 2+ H2s, no bullet points
[ ] <div class="post-cta"> — relevant book CTA with links to book page + Amazon
[ ] "Also on the blog" — 2–4 internal links to related live posts
[ ] Giscus comments block (copy exactly, do not change config values)
[ ] </div></main>
[ ] <section class="mailing-section"> — MailerLite form (copy exactly, form ID geMJhx)
[ ] <footer> — copy exactly
[ ] <script src="js/main.js">
[ ] Footer year script
```

---

## When to Update This File

Update `POST-STYLE.md` when:
- A new book is published (add it to the CTA options)
- The MailerLite form ID changes
- The Giscus repo ID changes (if repo is renamed)
- The voice evolves in a way that should be documented (note it in the Voice section)
- The internal link map grows significantly (update `POST-LINKS.md` or add a section here)

---

## File Locations

| File | Purpose |
|---|---|
| `POST-STYLE.md` | This file — voice, SEO, AI, virality settings |
| `BLOG-PIPELINE.md` | Automation ops — schedules, workflow commands, MailerLite setup |
| `blog-who-was-penthesilea.html` | Canonical HTML template — copy structure from this file |
| `scheduled-posts/` | Pre-written weekly posts (do not edit without updating publish-post.yml) |
