"""Add The Burning Sea (B0HJGL8P7Q) to the site + backfill The Gorgon's Reflection on the
homepage (its launch commit only touched books.html/blog). 17 Sep 2026."""
import glob, re

BS_ASIN = 'B0HJGL8P7Q'
BS_URL = f'https://www.amazon.com/dp/{BS_ASIN}?tag=georgevela-20'
GR_URL = 'https://www.amazon.com/dp/B0HK3LZM1S?tag=georgevela-20'


def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8', newline='').write(s)
def sub1(s, a, b, label):
    assert s.count(a) == 1, f'{label}: expected 1 match, got {s.count(a)}'
    return s.replace(a, b)

# ---------------- books.html ----------------
p = 'books.html'; s = rd(p)
s = s.replace('Eleven standalone Greek myth retellings', 'Twelve standalone Greek myth retellings')
s = s.replace('Eleven Greek mythology retellings', 'Twelve Greek mythology retellings')
s = s.replace('"numberOfItems": 11,', '"numberOfItems": 12,')
s = s.replace('An eleven-book Greek mythology literary fiction series', 'A twelve-book Greek mythology literary fiction series')
s = sub1(s, 'Eleven books. Eleven myths reclaimed', 'Twelve books. Twelve myths reclaimed', 'intro')
s = sub1(s,
    '"url": "https://georgealexandervela.com/books.html#gorgons-reflection", "position": 11 }',
    '"url": "https://georgealexandervela.com/books.html#gorgons-reflection", "position": 11 },\n'
    '          { "@type": "Book", "name": "The Burning Sea: Aeneas and the Escape from Troy", "isbn": "B0HJGL8P7Q", "url": "https://georgealexandervela.com/books.html#burning-sea", "position": 12 }',
    'hasPart')
s = sub1(s, '<span class="arc-count">Five books</span>', '<span class="arc-count">Six books</span>', 'arc count')
entry = f'''    <!-- THE BURNING SEA -->
    <article class="book-entry featured fade-in" id="burning-sea">
      <div class="book-cover-wrap">
        <div class="book-badge badge-new">New — out now</div>
        <div class="book-cover">
          <a href="{BS_URL}" target="_blank" rel="noopener" aria-label="Buy The Burning Sea on Amazon">
            <img src="img/burning-sea.jpg"
                 alt="The Burning Sea: Aeneas and the Escape from Troy — Greek mythology literary fiction by George Alexander Vela"
                 width="500" height="795"
                 loading="eager">
          </a>
        </div>
      </div>
      <div class="book-info">
        <div class="book-meta">
          <span class="book-number">Trojan War Cycle</span>
          <span class="book-separator" aria-hidden="true"></span>
          <span class="book-genre">Literary Mythology</span>
        </div>
        <h2 class="book-title">The Burning Sea</h2>
        <p class="book-subtitle">Aeneas and the Escape from Troy</p>
        <div class="book-divider" aria-hidden="true"></div>
        <div class="book-description">
          <p>The Greeks came out of the horse at midnight. By dawn Troy was a fire, and one man was walking out of it with his father on his back and his small son by the hand.</p>
          <p>Aeneas is not the greatest of the Trojan princes, only the one the gods decided should survive. He loses his wife in the burning streets and meets her ghost before he reaches the gate. He builds a fleet from a dead city, is chased off one shore by harpies and wrecked on another by a storm, and washes up at Carthage — where a queen who has already buried one husband decides she will not bury her heart with him.</p>
          <p><em>The Burning Sea</em> follows Virgil's story from the belly of the horse to the coast of Italy: Dido's cave and Dido's pyre, the funeral games in Sicily, the descent to the underworld where his father shows him the city he will never live to see. It is the rare epic whose hero is defined not by what he wins but by what he is made to leave behind — and by carrying the seed of one city out of the ruins of another.</p>
        </div>
        <div class="book-actions">
          <a href="{BS_URL}" class="btn btn-primary" target="_blank" rel="noopener">Buy on Amazon</a>
          <a href="blog-trojan-horse.html" class="btn btn-outline">Read: Is the Trojan Horse in the Iliad?</a>
        </div>
      </div>
    </article>

    <!-- THE BROTHER'S BOW -->
    <article class="book-entry fade-in" id="brothers-bow">'''
s = sub1(s, '''    <!-- THE BROTHER'S BOW -->
    <article class="book-entry featured fade-in" id="brothers-bow">''', entry, 'insert entry')
wr(p, s)

# ---------------- index.html ----------------
p = 'index.html'; s = rd(p)
s = s.replace('eleven novels retelling ancient myth', 'twelve novels retelling ancient myth')
s = s.replace('Eleven Novels, Faithful to the Sources', 'Twelve Novels, Faithful to the Sources')
s = s.replace("across all eleven books.", "across all twelve books.")
s = sub1(s, '"numberOfItems": 10,', '"numberOfItems": 12,', 'index numberOfItems')
s = sub1(s, '''        "isPartOf": { "@id": "https://georgealexandervela.com/#series" },
        "position": 10
      }
    ]''', '''        "isPartOf": { "@id": "https://georgealexandervela.com/#series" },
        "position": 10,
        "offers": { "@type": "Offer", "url": "https://www.amazon.com/dp/B0HJC8QMD6", "availability": "https://schema.org/InStock" }
      },
      {
        "@type": "Book",
        "@id": "https://georgealexandervela.com/#book-gorgons-reflection",
        "name": "The Gorgon's Reflection: Perseus and the Rescue of Andromeda",
        "isbn": "B0HK3LZM1S",
        "author": { "@id": "https://georgealexandervela.com/#author" },
        "url": "https://georgealexandervela.com/books.html#gorgons-reflection",
        "image": "https://georgealexandervela.com/img/gorgons-reflection.jpg",
        "description": "Perseus, the boy from the chest, promises a king the head of Medusa — and brings it back. The Gorgon, Andromeda's rock, the wedding that becomes a war. Heroes & Journeys.",
        "genre": ["Greek mythology", "Literary fiction", "Perseus myth", "Greek mythology retelling"],
        "isPartOf": { "@id": "https://georgealexandervela.com/#series" },
        "position": 11,
        "offers": { "@type": "Offer", "url": "https://www.amazon.com/dp/B0HK3LZM1S", "availability": "https://schema.org/InStock" }
      },
      {
        "@type": "Book",
        "@id": "https://georgealexandervela.com/#book-burning-sea",
        "name": "The Burning Sea: Aeneas and the Escape from Troy",
        "isbn": "B0HJGL8P7Q",
        "author": { "@id": "https://georgealexandervela.com/#author" },
        "url": "https://georgealexandervela.com/books.html#burning-sea",
        "image": "https://georgealexandervela.com/img/burning-sea.jpg",
        "description": "Aeneas carries his father out of burning Troy and sails for a city that does not exist yet: the ghost of Creusa, the harpies, the storm, Dido at Carthage, the underworld, the Italian coast. Trojan War Cycle.",
        "genre": ["Greek mythology", "Literary fiction", "Aeneid retelling", "Roman mythology", "Greek mythology retelling"],
        "isPartOf": { "@id": "https://georgealexandervela.com/#series" },
        "position": 12,
        "offers": { "@type": "Offer", "url": "https://www.amazon.com/dp/B0HJGL8P7Q", "availability": "https://schema.org/InStock" }
      }
    ]''', 'index schema')
s = sub1(s, '<span class="strip-book-number">Book X · New</span>', '<span class="strip-book-number">Book X</span>', 'strip X')
s = sub1(s, '''        <span class="strip-book-title">The Blind Exile</span>
      </div>
''', f'''        <span class="strip-book-title">The Blind Exile</span>
      </div>

      <div class="strip-book fade-in" style="transition-delay:0.4s">
        <a href="books.html#gorgons-reflection" class="strip-book-cover" aria-label="The Gorgon's Reflection — Book Eleven">
          <img src="img/gorgons-reflection.jpg"
               alt="The Gorgon's Reflection: Perseus and the Rescue of Andromeda — Greek mythology literary fiction by George Alexander Vela"
               width="300" height="480"
               loading="lazy">
        </a>
        <span class="strip-book-number">Book XI · New</span>
        <span class="strip-book-title">The Gorgon's Reflection</span>
      </div>

      <div class="strip-book fade-in" style="transition-delay:0.42s">
        <a href="books.html#burning-sea" class="strip-book-cover" aria-label="The Burning Sea — Book Twelve">
          <img src="img/burning-sea.jpg"
               alt="The Burning Sea: Aeneas and the Escape from Troy — Greek mythology literary fiction by George Alexander Vela"
               width="300" height="480"
               loading="lazy">
        </a>
        <span class="strip-book-number">Book XII · New</span>
        <span class="strip-book-title">The Burning Sea</span>
      </div>
''', 'strip insert')
wr(p, s)

# ---------------- contact.html ----------------
p = 'contact.html'; s = rd(p)
s = sub1(s, '<option value="brothers-bow">The Brother\'s Bow</option>',
         '<option value="burning-sea">The Burning Sea</option>\n                    <option value="brothers-bow">The Brother\'s Bow</option>', 'contact option')
s = s.replace('Eleven novels on Amazon in ebook', 'Twelve novels on Amazon in ebook')
s = s.replace('All eleven novels are on Amazon', 'All twelve novels are on Amazon')
wr(p, s)

# ---------------- blog-trojan-horse.html: mid-article card -> The Burning Sea (its Ch.1 is inside the horse) ----------------
p = 'blog-trojan-horse.html'; s = rd(p)
old_card = re.search(r'<aside class="post-cta-card">.*?</aside>', s, flags=re.S).group(0)
assert 'hound-of-troy' in old_card
new_card = f'''<aside class="post-cta-card">
      <a class="post-cta-card__coverlink" href="books.html#burning-sea"><img class="post-cta-card__cover" src="img/burning-sea.jpg" alt="The Burning Sea - cover" width="92" height="138" loading="lazy"></a>
      <div class="post-cta-card__body">
        <span class="post-cta-card__kicker">From the novels</span>
        <p class="post-cta-card__title"><a href="books.html#burning-sea">The Burning Sea</a></p>
        <p class="post-cta-card__line">Chapter one opens inside the horse. Aeneas&rsquo;s night of the fall, and the voyage that came after it.</p>
        <a class="btn btn-primary" href="{BS_URL}" target="_blank" rel="noopener">Read it on Amazon</a>
      </div>
    </aside>'''
s = s.replace(old_card, new_card)
wr(p, s)

# ---------------- sitewide count ----------------
n = 0
for f in glob.glob('*.html'):
    t = rd(f); o = t
    t = t.replace('Eleven novels and counting.', 'Twelve novels and counting.')
    t = t.replace('Literary fiction rooted in Greek mythology. Eleven books. One unbroken', 'Literary fiction rooted in Greek mythology. Twelve novels and counting. One unbroken')
    if t != o: wr(f, t); n += 1
print('sitewide files touched', n)
