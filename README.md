# Theepana’s Travel Journal

## Open the website

1. On Windows, right-click the ZIP and choose **Extract All**. On macOS, double-click the ZIP.
2. Open the extracted `travel-portfolio` folder and double-click `index.html`.
3. Select a trip to open its own page. Click a photo to enlarge it.

You can browse the included website offline without installing anything. Keep `index.html`, `trips/`, `photos/`, and `assets/` in their original locations relative to one another.

## Replace or add photos

All photos live in `photos/<country>/<trip-folder>/`, beside the home page. For example, the two UAE trips use `photos/uae/feb-2024/` and `photos/uae/nov-2024/`.

- To swap a sample for your own JPEG without changing any code, give your photo the **same filename** and put it in the **same folder**. The old caption stays until you change it in `trips.json`.
- To change captions, use new filenames, or add photos, edit that trip’s `photos` list in `trips.json`. Each photo needs a `file` name and a `place` caption. You can also add an optional `alt` description.
- The first photo in each list is also the trip’s cover on the home page. The home-page hero uses the image specified in `site.json`; change its path and caption there.
- The bundled images are generated samples, not personal photos or evidence of visits to the pictured places. After replacing them, set `sample_photos` to `false` in `site.json` to hide the sample notices.

## Add a future trip

Open `trips.json` in a text editor and copy one complete trip entry. Put a comma between entries, but not after the last entry. For example:

```json
{
  "slug": "japan-april-2027",
  "title": "Japan",
  "country": "Japan",
  "date": "2027-04",
  "note": "",
  "folder": "japan/apr-2027",
  "photos": [
    { "file": "park.jpg", "place": "Ueno Park, Tokyo" },
    { "file": "waterfront.jpg", "place": "Sumida River, Tokyo" }
  ]
}
```

- `slug` is the unique page name: use lowercase letters, numbers and hyphens.
- `date` uses year and month, such as `2027-04`. The home page orders trips by date and keeps their listed order when two have the same month.
- Add your files to `photos/` followed by the `folder` you chose. In the example, that is `photos/japan/apr-2027/`.
- There is no fixed number of trips or photos. Use `"photos": []` to add a trip before adding pictures.

## Rebuild after changing trip details

Rebuild when you edit `trips.json` or `site.json`. You’ll need Python 3 for this step only. Open a terminal in the portfolio folder and run:

- **Windows:** `py build.py --check`
- **macOS/Linux:** `python3 build.py --check`

The command will report any missing photo files. It updates `index.html` and the separate HTML pages in `trips/` from your data. Reopen or refresh `index.html` to see your changes. If you remove a trip or change its slug, you can delete its old HTML file from `trips/`.

To host it yourself, publish `index.html` plus the `assets/`, `photos/`, and `trips/` folders with any static-site host. There’s no server app or database to configure.
