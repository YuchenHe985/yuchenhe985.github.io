# yuchenhe985.github.io

Source of [yuchenhe985.github.io](https://yuchenhe985.github.io): a short front door to my projects, plus notes on what a measurement taught me. The detail lives in the project repositories.

It is plain HTML and CSS produced by a short Python script, with no JavaScript framework. The only script on the page is a three-state
(system, light, dark) theme switch.

```
content/notes/*.md   short notes: Markdown with a small front-matter block
content/work.json    the project rows on the home page
figures.py           charts, drawn as HTML and CSS bars on one scale per chart; every number is taken from a published result
templates/           Jinja2 templates
static/              stylesheet, script, favicon and self-hosted fonts (Archivo, Source Serif 4, JetBrains Mono)
build.py             writes dist/, plus sitemap.xml and robots.txt
check_links.py       fails on any broken internal link or asset
```

## Build

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python build.py && .venv/bin/python check_links.py
python3 -m http.server -d dist 8000
```

A line containing only `[[figure:name]]` in a note is replaced by the chart of that name from `figures.py`.

## Deploy

Pushing to `main` runs `.github/workflows/pages.yml`, which builds the site, checks the links and publishes `dist/` with GitHub Pages.

## Licence

Code: MIT. Writing and figure data: all rights reserved. Fonts: SIL Open Font License 1.1. See [LICENSE](LICENSE).
