"""Build only the Sri Lanka district hub and galleries (Python 3, no packages)."""
from argparse import ArgumentParser
from html import escape
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
SAMPLE_DIR = "assets/sri-lanka-samples/"
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
ARROW = '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
UP_RIGHT = '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 18 18 6M8 6h10v10"/></svg>'
PIN = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/></svg>'

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def upper(text):
    return escape(text.upper())

def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def path_url(path):
    return "../" + quote(path, safe="/-._~")

def photo_fallback(photo):
    if not photo.get("detect_extension"):
        return ""
    filename = PurePosixPath(photo["file"])
    suffixes = (".jpeg", ".jpg", ".JPEG", ".JPG", ".Jpeg", ".Jpg")
    attrs = " ".join(path_url(filename.with_suffix(ext).as_posix()) for ext in suffixes
                     if ext != filename.suffix)
    handler = ("const list=this.dataset.fallback.split(' ');const next=list.shift();"
               "if(!next){this.onerror=null;return;}this.dataset.fallback=list.join(' ');"
               "const a=this.closest('a[data-gallery]');if(a)a.href=next;this.src=next;")
    return f' data-fallback="{escape(attrs)}" onerror="{escape(handler)}"'

def sample(photo):
    return bool(photo and photo["file"].startswith(SAMPLE_DIR))

def cover(district):
    return district.get("cover") or next(iter(district["photos"]), None)

def ordinal(idx):
    return str(idx).zfill(2)

def site_brand(site):
    return f'<a class="brand" href="../index.html"><img class="sl-compass" src="../assets/compass.svg" alt=""><span>{escape(site["name"])}<small>TRAVEL JOURNAL</small></span></a>'

def layout(site, title, description, body, district=False):
    brand = site_brand(site)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#132d36">
  <meta name="description" content="{escape(description)}">
  <title>{escape(title)} | {escape(site["title"])}</title>
  <link rel="icon" href="../assets/compass.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../assets/styles.css">
  <link rel="stylesheet" href="../assets/sri-lanka.css">
  <script src="{('../assets/site.js' if district else 'district-filter.js')}" defer></script>
</head>
<body id="top" class="sl-section">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="shell header-inner">
  {brand}
  <nav class="sl-header-nav" aria-label="Main navigation">
    <a class="header-link" href="../index.html">Travel journal <span aria-hidden="true">↗</span></a>
    <a class="header-link" href="{('index.html#districts' if district else '#districts')}">All districts <span aria-hidden="true">{('↗' if district else '↓')}</span></a>
  </nav>
</div></header>
{body}
<footer class="site-footer"><div class="shell footer-inner">
  {brand}
  <a class="header-link" href="#top">Back to top <span aria-hidden="true">↑</span></a>
</div></footer>
</body>
</html>
"""

def district_card(district, i):
    thumbnail = cover(district)
    image = f'<img src="{path_url(thumbnail["file"])}" alt="" loading="lazy" decoding="async"{photo_fallback(thumbnail)}>' if thumbnail else ""
    return f'''<li class="trip-card sl-district-card" data-province="{slugify(district["province"])}">
  <a class="card-link" href="{district["slug"]}.html">
    <div class="card-photo">{image}<span class="card-stamp">DISTRICT {ordinal(i)}</span></div>
    <div class="card-body">
      <p class="eyebrow sl-card-province">{upper(district["province"])} PROVINCE</p>
      <h3>{escape(district["name"])}</h3>
      <span class="card-arrow">{UP_RIGHT}<span class="sr-only">Open gallery</span></span>
    </div>
  </a>
</li>'''

def hub(site, data, districts):
    hero = data["hero"]
    provinces = data["provinces"]
    illustrative = " • illustrative sample" if sample(hero) and hero.get("show_sample_label", True) else ""
    intro = data.get("intro", "Explore the island, one district at a time.")
    hero_intro = f"        <p>{escape(intro)}</p>\n" if intro else ""
    cards = "\n".join(district_card(d, i) for i, d in enumerate(districts, 1))
    controls = "\n".join(f'<button type="button" data-province-filter="{slugify(p["name"])}" aria-pressed="false" aria-controls="sl-district-grid">{escape(p["name"])}</button>' for p in provinces)
    note = '<p class="sample-note sl-covers-note">Illustrative sample covers are used where personal photos haven’t been added.</p>' if data.get("show_cover_note", True) and any(sample(cover(d)) for d in districts) else ""
    body = f"""
<main id="main">
  <div class="shell">
    <a class="back-link sl-hub-back" href="../index.html">{ARROW} Back to the travel journal</a>
    <section class="sl-hero" aria-labelledby="sl-title">
      <div class="sl-hero-copy">
        <p class="eyebrow hero-kicker"><span></span> BORN COUNTRY</p>
        <h1 id="sl-title">Sri Lanka</h1>
{hero_intro}        <a class="hero-button" href="#districts">Explore the districts <span aria-hidden="true">↓</span></a>
      </div>
      <figure class="sl-hero-photo">
        <img src="{path_url(hero["file"])}" alt="{escape(hero.get("alt", hero["place"]))}" fetchpriority="high" decoding="async">
        <figcaption>{PIN}{escape(hero["place"] + illustrative)}</figcaption>
      </figure>
    </section>
    <div class="sl-stats">
      <span><b>{len(districts)}</b> districts</span><span><b>{len(provinces)}</b> provinces</span><span>My birthplace</span>
    </div>
  </div>
  <section class="shell index-section sl-index" id="districts" aria-labelledby="sl-index-title">
    <p class="eyebrow section-kicker"><span></span> THE ISLAND INDEX</p>
    <div class="index-heading sl-index-heading">
      <div><h2 id="sl-index-title">Districts</h2><p>Open any district to see its photo gallery.</p></div>
      <p class="sl-results" id="sl-district-count" aria-live="polite">{len(districts)} districts</p>
    </div>
    <div class="filters sl-filters" id="sl-province-filters" role="group" aria-label="Filter districts by province" hidden>
      <button type="button" data-province-filter="all" aria-pressed="true" aria-controls="sl-district-grid">All provinces</button>
      {controls}
    </div>
    <ul class="trip-grid" id="sl-district-grid">
      {cards}
    </ul>
    {note}
  </section>
</main>"""
    return layout(site, "Sri Lanka", "Explore Sri Lanka’s district photo galleries by province.", body)

def figure(photo, index):
    src = path_url(photo["file"])
    place = escape(photo["place"])
    alt = escape(photo.get("alt", photo["place"]))
    note = '<span class="sl-sample-badge">Illustrative sample</span>' if sample(photo) else ""
    return f"""<figure>
  <a class="gallery-image" href="{src}" data-gallery aria-label="Enlarge photo: {place}">
    <img src="{src}" alt="{alt}" {'fetchpriority="high"' if index == 1 else 'loading="lazy"'} decoding="async"{photo_fallback(photo)}>
    {note}<span class="image-expand" aria-hidden="true">{UP_RIGHT}</span>
  </a>
  <figcaption><span class="plate-number" aria-hidden="true">{ordinal(index)}</span>{place}</figcaption>
</figure>"""

def district_link(target, label, cls):
    return f'<a class="trip-step {cls}" href="{target["slug"]}.html"><span class="step-arrow">{ARROW}</span><span><small>{label}</small><strong>{escape(target["name"])}</strong></span></a>' if target else ""

def district_page(site, districts, i):
    d = districts[i]
    name = escape(d["name"])
    photos = d["photos"]
    note = '<p class="gallery-note">Illustrative samples are placeholders, not photos taken in this district.</p>' if any(sample(p) for p in photos) else ""
    rendered_photos = "\n".join(figure(p, j) for j, p in enumerate(photos, 1))
    rendered_photos = f'<div class="gallery">{rendered_photos}</div>' if photos else '<p class="gallery-note">No photos have been added to this gallery yet.</p>'
    body = f"""
<main id="main" class="shell detail sl-detail">
  <a class="back-link" href="index.html#districts">{ARROW} All Sri Lanka districts</a>
  <div class="detail-heading sl-detail-heading">
    <div>
      <p class="eyebrow section-kicker"><span></span> SRI LANKA <span class="dot-separator">·</span> DISTRICT {ordinal(i + 1)}</p>
      <h1>{name}</h1>
    </div>
    <p class="detail-country">{PIN}{escape(d["province"])} Province</p>
  </div>
  <section aria-labelledby="gallery-title">
    <div class="gallery-heading"><h2 id="gallery-title">Photo gallery</h2><p>{len(photos)} {'photo' if len(photos) == 1 else 'photos'}</p></div>
    {note}
    {rendered_photos}
  </section>
  <nav class="trip-nav" aria-label="Browse districts">
    {district_link(districts[i-1] if i else None, 'Previous district', 'previous')}
    {district_link(districts[i+1] if i+1 < len(districts) else None, 'Next district', 'next')}
  </nav>
  <dialog class="lightbox" id="lightbox" aria-label="Photo viewer">
    <div class="lightbox-inner">
      <button type="button" class="lightbox-close" aria-label="Close photo" autofocus>×</button>
      <button type="button" class="lightbox-prev" aria-label="Previous photo">←</button>
      <figure><img alt=""><figcaption aria-live="polite"></figcaption></figure>
      <button type="button" class="lightbox-next" aria-label="Next photo">→</button>
    </div>
  </dialog>
</main>"""
    return layout(site, f'{d["name"]} | Sri Lanka', f'{d["name"]} district photo gallery, Sri Lanka.', body, True)

def validate_photo(photo, missing):
    path = photo["file"]
    raw = PurePosixPath(path)
    if not path or "\\" in path or raw.is_absolute() or ".." in raw.parts or ":" in path:
        raise ValueError(f"Photo paths must be relative to the site root: {path!r}")
    local = SITE / raw
    if photo.get("detect_extension") and local.parent.is_dir():
        # Windows Explorer can hide extensions. Preserve the actual filename for GitHub Pages.
        supported = {".jpg", ".jpeg", ".png", ".webp", ".avif"}
        matches = sorted(p for p in local.parent.iterdir()
                         if p.is_file() and p.stem == local.stem and p.suffix.lower() in supported)
        if any(p.name == local.name for p in matches):
            return photo
        if len(matches) == 1:
            return {**photo, "file": matches[0].relative_to(SITE).as_posix()}
    if not local.is_file():
        missing.add(path)
    return photo

def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail without writing if any listed photo file is missing")
    options = parser.parse_args()
    site = read(SITE / "site.json")
    data = read(HERE / "districts.json")
    slugs = set()
    province_ids = set()
    districts = []
    missing = set()
    validate_photo(data["hero"], missing)
    for province in data["provinces"]:
        province_id = slugify(province["name"])
        if not province_id or province_id == "all" or province_id in province_ids:
            raise ValueError(f'Invalid or duplicate province name: {province["name"]!r}')
        province_ids.add(province_id)
        for district in province["districts"]:
            slug = district["slug"]
            if not NAME_RE.fullmatch(slug) or slug in slugs or slug == "index":
                raise ValueError(f"Invalid or duplicate district slug: {slug!r}")
            slugs.add(slug)
            entry = {**district, "province": province["name"]}
            if district.get("cover"):
                entry["cover"] = validate_photo(district["cover"], missing)
            entry["photos"] = [validate_photo(photo, missing) for photo in district["photos"]]
            districts.append(entry)
    if options.check and missing:
        parser.exit(1, "Missing images:\n  " + "\n  ".join(sorted(missing)) + "\n")
    outputs = {"index.html": hub(site, data, districts)}
    outputs.update({f'{d["slug"]}.html': district_page(site, districts, i) for i, d in enumerate(districts)})
    for filename, source in outputs.items():
        (HERE / filename).write_text(source, encoding="utf-8")
    print(f"Built the Sri Lanka hub and {len(districts)} district pages.")

if __name__ == "__main__":
    main()
