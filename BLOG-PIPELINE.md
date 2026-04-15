# Blog Pipeline — georgealexandervela.com

## Schedule

| Week | Date (Tuesday) | Post | Status |
|------|--------------|------|--------|
| 1  | 6 Apr 2026   | Who Was Penthesilea? | ✅ Live |
| 2  | 13 Apr 2026  | The Real Myth of Bellerophon | ✅ Live |
| 3  | 21 Apr 2026  | Hecuba of Troy: The Queen Behind the War | ⏳ Scheduled |
| 4  | 28 Apr 2026  | Achilles and Penthesilea: The Love Story History Ignored | ⏳ Scheduled |
| 5  | 5 May 2026   | What Is the Iliad Actually About? | ⏳ Scheduled |
| 6  | 12 May 2026  | The Women the Trojan War Forgot | ⏳ Scheduled |
| 7  | 19 May 2026  | Hercules and Guilt: What the Myths Never Say Directly | ⏳ Scheduled |
| 8  | 26 May 2026  | Greek Mythology Books for Fans of Madeline Miller | ⏳ Scheduled |
| 9  | 2 Jun 2026   | Pegasus: The Horse That Was Never Just a Horse | ⏳ Scheduled |
| 10 | 9 Jun 2026   | Why Hecuba Matters: Grief, Power, and Vengeance in Troy | ⏳ Scheduled |
| 11 | 16 Jun 2026  | The Amazons: What Greek Mythology Got Wrong | ⏳ Scheduled |
| 12 | 23 Jun 2026  | Where to Start With Greek Mythology Retellings | ⏳ Scheduled |

---

## How It Works

```
Every Tuesday 8 AM Pacific (15:00 UTC)
       │
       ▼
publish-post.yml (GitHub Actions)
       │
       ├── 1. Calculate week number from date
       ├── 2. Copy scheduled-posts/week-XX.html → root
       ├── 3. Insert article card into blog.html
       ├── 4. Update sitemap.xml
       ├── 5. Update feed.xml (Brevo RSS picks this up → emails subscribers)
       ├── 6. Commit + push
       └── 7. Verify post is live (HTTP check)

Every Tuesday 10 AM Pacific (17:00 UTC)
       │
       ▼
verify-blog-publish.yml (GitHub Actions)
       │
       ├── HTTP check on expected post URL
       └── If not live → opens GitHub Issue with fix instructions
```

---

## Workflows

| File | Trigger | Purpose |
|------|---------|---------|
| `.github/workflows/publish-post.yml` | Tuesday 8 AM Pacific (15:00 UTC) + manual | Publishes the week's post |
| `.github/workflows/verify-blog-publish.yml` | Tuesday 10 AM Pacific (17:00 UTC) + manual | Checks post went live, opens issue if not |

---

## If a Post Didn't Publish

### 1. Check what went wrong
```bash
gh run list --repo georgie357/georgie357.github.io --workflow publish-post.yml --limit 5
```

### 2. Read the logs
```bash
gh run view <RUN_ID> --repo georgie357/georgie357.github.io --log | grep -E "ERROR|error|Traceback|Published|Updated"
```

### 3. Re-trigger manually
```bash
gh workflow run publish-post.yml \
  --repo georgie357/georgie357.github.io \
  --field week_override=<WEEK_NUMBER>
```

Or from the GitHub web UI:
**Actions → Publish Scheduled Blog Post → Run workflow → set week_override**

---

## Brevo Email — RSS Automation (fully automatic)

The publish workflow updates `feed.xml` with each new post.
Brevo's RSS Automation watches the feed and emails subscribers automatically.

### Setup (one-time, via Brevo App Store)

1. Log into [Brevo](https://app.brevo.com)
2. Go to **App Store → RSS campaign** integration
3. Set feed URL: `https://georgealexandervela.com/feed.xml`
4. Select template and configure recipients
5. Activate the automation

**After that: fully automatic.** Each Monday when the post publishes, `feed.xml` gets a new item, Brevo detects it and sends the email. No manual work.

### Signup form

Form: **Blog Newsletter Signup** (created in Brevo dashboard)
- Builder: Marketing → Forms → Sign-up
- Form ID: `69ded9fe24cbc036c65565ff`
- Embed: iframe from `https://978199fb.sibforms.com/serve/MUIFAHSyDkZj9Lr_3K9fn5PlYXCtMW7mAzf3VMl5-RY3YD74omgeYXMC2DkdA5LOKd75i1WhClw-TUIx2o16qhM8Fi_Q_xEDHIo-iCo7HH5-MCYb0nLNQVV339TSKsUeGWf3_E6waXxWkbuhQrwBjr9OzEgZRKkr66XUKT4rh-uRrc35IyZriKQXc0ZQO32nNu-XDpj5YFeieygtBg==`
  - NOTE: URL contains capital `I` characters that look like lowercase `l` in many fonts — do not retype, always copy from Brevo dashboard
- Saves to: **Your first list**

### Feed URL
```
https://georgealexandervela.com/feed.xml
```

---

## Adding a New Post

1. Write the post in `scheduled-posts/week-XX-slug.html`
   - Use `../` relative paths (the publish script fixes them on deploy)
2. Add an entry to the `posts` dict in `publish-post.yml`
3. Add the title to the `titles` dict in `publish-post.yml`
4. Add the excerpt to the `excerpts` dict in `publish-post.yml`
5. Add to the schedule table in this file
   - Email is fully automatic via Brevo RSS — no extra step needed

---

## Source Files

| Location | Purpose |
|----------|---------|
| `scheduled-posts/week-XX-*.html` | Pre-written posts, not yet live |
| `blog-*.html` | Live published posts (root) |
| `blog.html` | Blog index — article cards inserted here on publish |
| `sitemap.xml` | Updated automatically on publish |
| `.github/workflows/publish-post.yml` | Main publish automation |
| `.github/workflows/verify-blog-publish.yml` | Tuesday post-publish check |

---

## Known Limitations

| Issue | Status |
|-------|--------|
| GitHub Actions cron can be delayed up to ~1 hr on free accounts | Acceptable — Tuesday verifier catches any misses |
| No SMS/email alert on failure | Handled — GitHub Issue opened automatically by verifier |
