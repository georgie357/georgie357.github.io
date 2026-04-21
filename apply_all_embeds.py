r"""
apply_all_embeds.py - One-shot script to embed all posted YouTube videos
into the correct book pages on georgealexandervela.com.

Run from: C:\Users\User\Documents\georgie357.github.io\
  python apply_all_embeds.py

Commits and pushes both changed files at the end.
"""

import subprocess
from pathlib import Path

REPO = Path(r"C:\Users\User\Documents\georgie357.github.io")
HERC = REPO / "hercules.html"
DT   = REPO / "dragons-teeth.html"

# ---------------------------------------------------------------------------
# Portrait iframe figure (for both pages)
# ---------------------------------------------------------------------------
def figure(video_id, title, caption):
    return f"""
      <figure style="margin:0">
        <div style="position:relative;width:100%;padding-bottom:177.78%;height:0;overflow:hidden;border:1px solid var(--border-light);border-radius:4px;background:#000">
          <iframe
            src="https://www.youtube-nocookie.com/embed/{video_id}?rel=0"
            title="{title}"
            loading="lazy"
            allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerpolicy="strict-origin-when-cross-origin"
            allowfullscreen
            style="position:absolute;top:0;left:0;width:100%;height:100%;border:0"></iframe>
        </div>
        <figcaption style="margin-top:0.75rem;text-align:center;font-size:0.85rem;color:var(--text-muted);font-style:italic">
          {caption}
        </figcaption>
      </figure>"""


# ===========================================================================
# 1. HERCULES.HTML — add 5 missing chapter shorts to existing grid
# ===========================================================================
NEW_HERC_FIGURES = [
    figure("PUYwjnS8ZOA",
           "The Coward on the Throne | Ch04 | Hercules and the Cradle of Thunder",
           "Chapter 4 — The Coward on the Throne"),
    figure("pkxNA2Uzh3s",
           "The Wound That Would Not Close | Ch05 | Hercules and the Cradle of Thunder",
           "Chapter 5 — The Wound That Would Not Close"),
    figure("IxmWg6WD2xI",
           "The Year of Running | Ch06 | Hercules and the Cradle of Thunder",
           "Chapter 6 — The Year of Running"),
    figure("dhxiOmYZF00",
           "Thirty years of dung | Chapter 8 | Hercules and the Cradle of Thunder",
           "Chapter 8 — The River and the Filth"),
    figure("9DeMGwjlVhA",
           "Ten thousand metal birds | Chapter 9 | Hercules and the Cradle of Thunder",
           "Chapter 9 — The Rain of Bronze"),
]

# The grid closes just before the "More passages on YouTube" paragraph
HERC_GRID_ANCHOR = '    </div>\n\n    <p style="text-align:center;margin-top:2rem'

herc_content = HERC.read_text(encoding="utf-8")

added_herc = 0
for fig in NEW_HERC_FIGURES:
    # Extract video id from the figure HTML to check if already present
    vid_id = fig.split('/embed/')[1].split('?')[0]
    if vid_id in herc_content:
        print(f"  [skip] {vid_id} already in hercules.html")
        continue
    # Insert figure just before the grid's closing </div>
    herc_content = herc_content.replace(
        HERC_GRID_ANCHOR,
        fig + "\n\n    </div>\n\n    <p style=\"text-align:center;margin-top:2rem",
        1
    )
    print(f"  [added] {vid_id} to hercules.html")
    added_herc += 1

if added_herc:
    HERC.write_text(herc_content, encoding="utf-8")
    print(f"hercules.html — {added_herc} figures added")
else:
    print("hercules.html — nothing to add")


# ===========================================================================
# 2. DRAGONS-TEETH.HTML — new "Passages from the Book" section with all 7 DT shorts
# ===========================================================================
DT_SHORTS = [
    # (video_id, iframe title, figcaption)
    ("YthFMrFaydM",
     "The Dragon's Teeth — Chapter 1: The White Bull | Myths of the Ancient World",
     "Chapter 1 — The White Bull"),
    ("cfNvHtTPQGM",
     "The Dragon Did Not Roar | Ch01 | The Dragon's Teeth | Greek Mythology",
     "Chapter 1 — The Dragon Did Not Roar"),
    ("6C1nuGmZuTo",
     "She Opened Her Eyes and Whispered | Ch02 | The Dragon's Teeth | Greek Mythology",
     "Chapter 2 — Europa"),
    ("aSYyZa_75Zc",
     "He Came to Delphi for an Answer | Ch03 | The Dragon's Teeth | Greek Mythology",
     "Chapter 3 — The Oracle"),
    ("zksqKJ5zQRY",
     "The Dragon's Teeth — Chapter 4 | Myths of the Ancient World",
     "Chapter 4 — The Dragon's Teeth"),
    ("-glMomRrTEw",
     "He Drove His Sword Through the Dragon's Throat | Ch04 | The Dragon's Teeth | Greek Mythology",
     "Chapter 4 — The Dragon's Throat"),
    ("QW4YoXlCUhI",
     "They Rose From the Earth Fully Armed | Ch05 | The Dragon's Teeth | Greek Mythology",
     "Chapter 5 — The Spartoi"),
]

DT_FIGURES = "".join(figure(vid, title, cap) for vid, title, cap in DT_SHORTS)

DT_SECTION = f"""
  <!-- PASSAGES FROM THE BOOK — SHORT CLIPS -->
  <section class="fade-in" style="max-width:1000px;margin:3rem auto 5rem;padding:0 1rem" aria-labelledby="dt-passages-heading">
    <header style="text-align:center;margin-bottom:2.5rem">
      <span class="section-label" style="justify-content:center;display:flex">Short Passages</span>
      <h2 id="dt-passages-heading" class="section-title" style="font-size:1.9rem;text-align:center">Passages from the Book</h2>
      <p style="color:var(--text-muted);font-size:1rem;line-height:1.6;max-width:560px;margin:1rem auto 0">
        60-second cinematic readings from <em>The Dragon's Teeth</em>, narrated by Daniel, with AI-generated ancient Greek artwork.
      </p>
    </header>

    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.5rem">
{DT_FIGURES}
    </div>

    <p style="text-align:center;margin-top:2rem;font-size:0.9rem;color:var(--text-muted)">
      More passages on <a href="https://www.youtube.com/@GeorgeAlexanderVela" target="_blank" rel="noopener" style="color:var(--gold)">YouTube \u2192</a> &nbsp;&middot;&nbsp; <a href="https://www.amazon.com/dp/B0D7K5J71W" target="_blank" rel="noopener" style="color:var(--gold)">Full book on Amazon \u2192</a>
    </p>
  </section>"""

dt_content = DT.read_text(encoding="utf-8")

# Check which DT videos are already present
already_present = [vid for vid, _, _ in DT_SHORTS if vid in dt_content]
new_ids = [vid for vid, _, _ in DT_SHORTS if vid not in dt_content]

if "dt-passages-heading" in dt_content:
    print("dragons-teeth.html — passages section already exists")
elif not new_ids:
    print("dragons-teeth.html — all videos already embedded")
else:
    # Insert new section just before </main>
    dt_content = dt_content.replace("</main>", DT_SECTION + "\n</main>", 1)
    DT.write_text(dt_content, encoding="utf-8")
    print(f"dragons-teeth.html — passages section added ({len(DT_SHORTS)} shorts)")

# Verify no DT videos were skipped (some may have been in the section already)
for vid in already_present:
    print(f"  [note] {vid} was already in dragons-teeth.html before this run")


# ===========================================================================
# 3. Git commit + push
# ===========================================================================
changed = []
if added_herc:
    changed.append("hercules.html")
if "dt-passages-heading" not in Path(DT).read_text(encoding="utf-8").replace(DT_SECTION, ""):
    # only add to changed if we actually wrote it
    pass

# Re-read to confirm what changed
for fname in ["hercules.html", "dragons-teeth.html"]:
    result = subprocess.run(
        ["git", "diff", "--name-only", fname],
        cwd=str(REPO), capture_output=True, text=True
    )
    if result.stdout.strip():
        changed.append(fname)

changed = list(set(changed))

if changed:
    print(f"\nCommitting: {changed}")
    for f in changed:
        subprocess.run(["git", "add", f], cwd=str(REPO), check=True)
    subprocess.run(
        ["git", "commit", "-m",
         f"embed: add all posted YouTube Shorts to book pages ({', '.join(changed)})"],
        cwd=str(REPO), check=True
    )
    push = subprocess.run(["git", "push"], cwd=str(REPO), capture_output=True, text=True)
    if push.returncode == 0:
        print("git push succeeded — live in ~30 seconds")
    else:
        print(f"git push failed: {push.stderr[:300]}")
else:
    print("\nNo changes to commit.")
