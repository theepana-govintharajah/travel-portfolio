"""Generate index.html and the individual trip pages. Requires Python 3 only."""
import argparse
from calendar import month_name
from html import escape
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent

ARROW = '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
UP_RIGHT = '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 18 18 6M8 6h10v10"/></svg>'
PIN = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/></svg>'
LOGO = '<svg width="25" height="25" viewBox="0 0 28 28" fill="none" aria-hidden="true"><circle cx="14" cy="14" r="12" stroke="currentColor" stroke-width="1.25"/><path d="m18.7 9.3-2.5 6.9-6.9 2.5 2.5-6.9 6.9-2.5Z" fill="currentColor"/><circle cx="14" cy="14" r="1.25" fill="#132d36"/></svg>'

def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

def href(value):
    return quote(str(value), safe="/-._~")

def validate_path(value, label):
    if not value or "\\" in value or value.startswith("/") or ".." in PurePosixPath(value).parts:
        raise ValueError(f"Invalid {label}: {value!r}")

def stamp(number):
    return str(number).zfill(2)

def format_date(date):
    y, m = date.split("-")
    return f"{month_name[int(m)]} {y}"

def photo_path(trip, photo):
    return f"photos/{trip['folder']}/{photo['file']}"

def trip_url(trip):
    return f"trips/{trip['slug']}.html"

def header(site, prefix="", trip=False):
    return f"""
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header" id="top"><div class="shell header-inner">
  <a class="brand" href="{prefix}index.html">{LOGO}<span>{escape(site["name"])}<small>TRAVEL JOURNAL</small></span></a>
  <nav aria-label="Main navigation">
    <a class="header-link" href="{prefix}{'index.html' if trip else ''}#trips">{'All trips' if trip else 'Trip index'} <span aria-hidden="true">↗</span></a>
  </nav>
</div></header>"""

def footer(site, prefix=""):
    return f"""
<footer class="site-footer"><div class="shell footer-inner">
  <a class="brand" href="{prefix}index.html">{LOGO}<span>{escape(site["name"])}<small>TRAVEL JOURNAL</small></span></a>
  <a class="header-link" href="#top">Back to top <span aria-hidden="true">↑</span></a>
</div></footer>"""

def page(site, title, summary, content, prefix="", trip=False):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#132d36">
  <meta name="description" content="{escape(summary)}">
  <title>{escape(title)}</title>
  <link rel="icon" href="{prefix}assets/compass.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}assets/styles.css">
  <script src="{prefix}assets/site.js" defer></script>
</head>
<body>
{header(site, prefix, trip)}
{content}
{footer(site, prefix)}
</body>
</html>
"""

def home_card(trip, ordinal):
    photo = next(iter(trip["photos"]), None)
    media = f'<img src="{href(photo_path(trip, photo))}" alt="" loading="lazy" decoding="async">' if photo else ""
    note = f'<p>{escape(trip["note"])}</p>' if trip["note"] else ""
    return f"""
<li class="trip-card" data-year="{trip["date"][:4]}">
  <a href="{trip_url(trip)}" class="card-link">
    <div class="card-photo">{media}<span class="card-stamp">NO. {stamp(ordinal)}</span></div>
    <div class="card-body">
      <time class="eyebrow" datetime="{trip["date"]}">{format_date(trip["date"])}</time>
      <h3>{escape(trip["title"])}</h3>
      {note}
      <span class="card-arrow">{UP_RIGHT}<span class="sr-only">Open gallery</span></span>
    </div>
  </a>
</li>"""

def landing(site, trips):
    first_year, last_year = (trips[0]["date"][:4], trips[-1]["date"][:4]) if trips else ("", "")
    dates = first_year if first_year == last_year else f"{first_year}–{last_year}"
    country_count = len({t["country"] for t in trips})
    year_buttons = "".join(f'<button type="button" data-filter="{y}" aria-pressed="false">{y}</button>' for y in sorted({t["date"][:4] for t in trips}))
    cards = "\n".join(home_card(t, i) for i, t in enumerate(trips, 1))
    cap = f'<p class="hero-caption">{PIN}{escape(site["hero_caption"])}</p>' if site.get("hero_caption") else ""
    hero_image = f'<img class="hero-img" src="{href(site["hero_image"])}" alt="" fetchpriority="high">' if site.get("hero_image") else ""
    return page(site, site["title"], "A personal collection of international journeys, with a photo gallery for each trip.", f"""
<main id="main">
  <section class="hero shell" aria-labelledby="hero-title">
    <div class="hero-frame">
      {hero_image}
      <div class="hero-content">
        <p class="eyebrow hero-kicker"><span></span> A PERSONAL TRAVEL JOURNAL</p>
        <h1 id="hero-title">The places<br>I’ve <em>been.</em></h1>
        <p class="hero-description">International trips, in the order they happened, with a photo album for each chapter.</p>
        <a class="hero-button" href="#trips">Explore the trips <span aria-hidden="true">↓</span></a>
      </div>
      {cap}
    </div>
    <div class="stats" aria-label="Journal at a glance">
      <div><strong>{stamp(len(trips))}</strong><span>{'Trip' if len(trips) == 1 else 'Trips'}</span></div>
      <div><strong>{stamp(country_count)}</strong><span>{'Country' if country_count == 1 else 'Countries'}</span></div>
      <div><strong>{dates or '—'}</strong><span>Travel years</span></div>
    </div>
  </section>
  <section class="shell index-section" id="trips" aria-labelledby="index-title">
    <p class="eyebrow section-kicker"><span></span> THE TRIP INDEX</p>
    <div class="index-heading">
      <div><h2 id="index-title">Journeys</h2><p>Pick a trip to open its photo album.</p></div>
      <div class="filters" role="group" aria-label="Filter trips by year" hidden><button type="button" data-filter="all" aria-pressed="true">All years</button>{year_buttons}</div>
    </div>
    <p class="sr-only" id="filter-status" aria-live="polite"></p>
    <ul class="trip-grid">{cards}</ul>
    {'<p class="sample-note">The current photos are samples, ready to be replaced with my own.</p>' if site.get("sample_photos") else ''}
  </section>
</main>""")

def figure(trip, photo, ordinal):
    src = "../" + href(photo_path(trip, photo))
    place = escape(photo["place"])
    alt = escape(photo.get("alt", photo["place"]))
    return f"""
<figure>
  <a class="gallery-image" href="{src}" data-gallery aria-label="Enlarge photo: {place}">
    <img src="{src}" alt="{alt}" {'fetchpriority="high"' if ordinal == 1 else 'loading="lazy"'} decoding="async">
    <span class="image-expand" aria-hidden="true">{UP_RIGHT}</span>
  </a>
  <figcaption><span class="plate-number" aria-hidden="true">{stamp(ordinal)}</span>{place}</figcaption>
</figure>"""

def move_link(trip, label, cls):
    if not trip:
        return ""
    return f'<a class="trip-step {cls}" href="{trip["slug"]}.html"><span class="step-arrow">{ARROW}</span><span><small>{label}</small><strong>{escape(trip["title"])}<span class="step-date"> · {format_date(trip["date"])}</span></strong></span></a>'

def trip_page(site, trips, idx):
    trip = trips[idx]
    photo_count = len(trip["photos"])
    images = "\n".join(figure(trip, p, i) for i, p in enumerate(trip["photos"], 1))
    label = 'Sample gallery' if site.get("sample_photos") else 'Photo gallery'
    note = f'<p class="trip-note">{escape(trip["note"])}</p>' if trip["note"] else ""
    return page(site, f'{trip["title"]} | {format_date(trip["date"])} | {site["title"]}', f'{trip["title"]} photo gallery, {format_date(trip["date"])}.', f"""
<main id="main" class="shell detail">
  <a class="back-link" href="../index.html#trips">{ARROW} All trips</a>
  <div class="detail-heading">
    <div>
      <p class="eyebrow section-kicker"><span></span> TRIP {stamp(idx + 1)} <span class="dot-separator">·</span> <time datetime="{trip["date"]}">{format_date(trip["date"])}</time></p>
      <h1>{escape(trip["title"])}</h1>
      {note}
    </div>
    <p class="detail-country">{PIN}{escape(trip["country"])}</p>
  </div>
  <section aria-labelledby="gallery-title">
    <div class="gallery-heading"><h2 id="gallery-title">{label}</h2><p>{photo_count} {'photo' if photo_count == 1 else 'photos'}</p></div>
    {'<p class="gallery-note">Illustrative photos and place names, not a record of the sites visited.</p>' if site.get("sample_photos") and photo_count else ''}
    {f'<div class="gallery" id="photos">{images}</div>' if images else '<p class="gallery-note">No photos have been added to this trip yet.</p>'}
  </section>
  <nav class="trip-nav" aria-label="Browse trips">
    {move_link(trips[idx - 1] if idx else None, 'Previous trip', 'previous')}
    {move_link(trips[idx + 1] if idx + 1 < len(trips) else None, 'Next trip', 'next')}
  </nav>
  <dialog class="lightbox" id="lightbox" aria-labelledby="lightbox-caption">
    <div class="lightbox-inner">
      <button type="button" class="lightbox-close" aria-label="Close photo" autofocus>×</button>
      <button type="button" class="lightbox-prev" aria-label="Previous photo">←</button>
      <figure><img alt=""><figcaption id="lightbox-caption"></figcaption></figure>
      <button type="button" class="lightbox-next" aria-label="Next photo">→</button>
    </div>
  </dialog>
</main>""", prefix="../", trip=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="also check that all configured photos exist on disk")
    args = parser.parse_args()
    site = read("site.json")
    trips = sorted(read("trips.json"), key=lambda t: t["date"])
    slugs = set()
    paths = []
    if site.get("hero_image"):
        validate_path(site["hero_image"], "hero image")
        paths.append(site["hero_image"])
    for trip in trips:
        slug = trip["slug"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in slugs:
            raise ValueError(f"Each slug must be unique and contain only lowercase letters, numbers and hyphens: {slug!r}")
        if not re.fullmatch(r"\d{4}-(?:0[1-9]|1[0-2])", trip["date"]):
            raise ValueError(f"Use YYYY-MM dates for {slug}")
        slugs.add(slug)
        validate_path(trip["folder"], "photo folder")
        for photo in trip["photos"]:
            validate_path(photo["file"], "photo filename")
            paths.append(photo_path(trip, photo))
    if args.check:
        missing = sorted({p for p in paths if not (ROOT / p).is_file()})
        if missing:
            parser.exit(1, "Missing images:\n  " + "\n  ".join(missing) + "\n")
    (ROOT / "trips").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(landing(site, trips), encoding="utf-8")
    for i, trip in enumerate(trips):
        (ROOT / trip_url(trip)).write_text(trip_page(site, trips, i), encoding="utf-8")
    print(f"Built the home page and {len(trips)} trip pages.")

if __name__ == "__main__":
    main()
