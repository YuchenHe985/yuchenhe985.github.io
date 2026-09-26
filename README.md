# yuchenhe985.github.io

Source of [yuchenhe985.github.io](https://yuchenhe985.github.io): a short front door to my projects, in English and Chinese, plus notes on what a measurement taught me. The detail lives in the project repositories.

It is plain HTML and CSS produced by a short Python script, with no JavaScript framework. Two small scripts run on the page: a three-state
(system, light, dark) theme switch, and a restrained motion script (sections rise in once, chart bars grow in, the nav follows the
section on screen). The motion script does nothing when JavaScript is off or reduced motion is requested.

```
content/notes/*.md      short notes in English: Markdown with a small front-matter block
content/notes_zh/*.md   the same notes in Chinese (same slugs and order)
content/i18n.py         page copy in both languages and the Chinese project rows
content/work.json       the project rows on the home page (numbers and links, language-neutral)
figures.py           charts, drawn as HTML and CSS bars on one scale per chart; every number is taken from a published result
templates/           Jinja2 templates
static/              stylesheet, scripts, favicon, share cards, photos (credits in static/img/CREDITS.md) and self-hosted
                     fonts (Archivo, Source Serif 4, JetBrains Mono, and a subset of Source Han Sans CN for the Chinese pages)
tools/               subset_cjk_font.py rebuilds the Chinese font subset from the characters the pages use
build.py             writes dist/, plus sitemap.xml and robots.txt
check_links.py       fails on any broken internal link or asset
```

## Build

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python build.py && .venv/bin/python check_links.py
python3 -m http.server -d dist 8000
```

A line containing only `[[figure:name]]` in a note is replaced by the chart of that name from `figures.py`, in the note's language.

After adding or changing Chinese text, rebuild the font subset so every character has a glyph (it needs the Source Han Sans CN OTF
files, which are not in the repository):

```bash
.venv/bin/python build.py && python3 tools/subset_cjk_font.py && .venv/bin/python build.py
```

## Deploy

Pushing to `main` runs `.github/workflows/pages.yml`, which builds the site, checks the links and publishes `dist/` with GitHub Pages.

## License

Code: MIT. Writing and figure data: all rights reserved. Fonts: SIL Open Font License 1.1. See [LICENSE](LICENSE).
