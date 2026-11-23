# Theepana’s Travel Journal

## Copy the Sri Lanka update into your Git repository

1. Extract the ZIP into a temporary folder.
2. Open your Git repo folder, the one that already contains `index.html`, `assets/`, `trips/`, and `photos/`.
3. Copy the extracted contents into that folder. Merge the `assets/` folders; keep your existing `photos/` and `.git/` in place. The supplied international `trips/` pages are included unchanged. If you have newer local copies, keep them rather than copying the included `trips/` folder.
4. Open `index.html` to preview. Click **Sri Lanka** and then any district. No build command is required to open or publish this ZIP.

The homepage’s existing hero, all international covers, and seven international trip pages are unchanged in content. Sri Lanka is a separate feature and does not change the international trip totals. This ZIP does not contain your existing photos or Git history.

## Update the Sri Lanka photos

- **District galleries:** Edit `sri-lanka/districts.json`, then run `py sri-lanka/build.py` from the repository root on Windows (or `python3 sri-lanka/build.py` on macOS/Linux). This rebuilds only the Sri Lanka pages, not the homepage or international gallery files.
- **Photo folders:** Put your real images into `photos/sri-lanka/<district-slug>/`. Use exact filenames, including the extension and letter case. The lists in `sri-lanka/districts.json` control how many photos appear and in what order. Add or remove one entry per photo. Keep the JSON commas between entries, but not after the last one.
- **Sri Lanka homepage image:** In `site.json`, change `birth_country_cover` to the new image path relative to the repository root. Set `birth_country_cover_is_sample` to `false` when switching to your own photo, then run `py build.py` (or `python3 build.py`).
- **A photo entry:** For example, add `{"file": "photos/sri-lanka/jaffna/Nallur Temple.jpg", "place": "Nallur Kandaswamy Temple, Jaffna"}` under Jaffna’s `photos` array. The first entry is its card cover unless you also set a separate `cover` entry, with the same format. An empty photo list shows an empty gallery.
- **Sri Lanka landing photo:** Edit the top-level `hero` entry in `sri-lanka/districts.json`, then rebuild the Sri Lanka pages. Run `py sri-lanka/build.py --check` to check the Sri Lanka photo paths before writing.
- **Samples:** The Sri Lanka placeholders are AI-generated illustrations of scenery, not photos of your trips or verified views of a district. They are kept separately in `assets/sri-lanka-samples/`. Leave those files in place for galleries that still use them.

## Maintain the international section

- To edit an existing international gallery, edit the corresponding HTML file in `trips/`. Add photos to its existing photo folder. The filters, captions, and display order live in the gallery HTML.
- To edit the international homepage covers or add a trip, use `trips.json` and then run `py build.py` (or `python3 build.py`). The first section of the homepage is controlled by `site.json`. For a new trip, add a unique lowercase hyphenated `slug`, `title`, `country`, `date` (`YYYY-MM`), `note`, and a photo `folder` relative to `photos/`. The optional `cover` is relative to that trip’s folder. An optional `photos` list can seed its new page.
- The main build updates the homepage and creates missing international trip pages; it never overwrites existing ones. Once your original `photos/` folder is in place, `py build.py --check` checks home and international gallery photo paths before writing. The separate Sri Lanka build uses its own data file and command.
- GitHub Pages serves these static pages without Python. Keep `index.html`, `assets/`, `sri-lanka/`, `trips/` and `photos/` together. Only push photos you want visitors to be able to access.
