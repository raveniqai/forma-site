# Forma 360 website

Source for https://forma.raveniq.ai (privacy policy, terms and support pages for the Forma 360 iOS app).

- `site.config.json`: publisher line, support email, effective date, App Store URL.
- `content/`, `templates/`, `static/`, `assets/`: sources. `build.py` (Python 3 standard library only) renders them into `docs/`, which GitHub Pages serves.
- Rebuild after any change: `python3 build.py`, then commit `docs/` together with the source.
- Preview locally: `python3 -m http.server 8000 --bind 127.0.0.1 --directory docs`

No scripts, trackers, cookies or third-party fonts are used.
