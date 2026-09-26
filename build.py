#!/usr/bin/env python3
"""Build the site into dist/, in English at / and Chinese at /zh/.

    python3 build.py          # writes dist/
    python3 -m http.server -d dist 8000

Notes (the long-form write-ups) are Markdown files in content/notes/ and are English-only; the
Chinese pages link out to them with an "(EN)" label. A line containing only [[figure:name]] in a
note is replaced by a chart from figures.py. Bilingual UI copy and translated project rows live in
content/i18n.py. Hobby photos are static/img/hobby-*.webp (free-license stock, see static/img/CREDITS.md).
"""
import json
import re
import shutil
import sys
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

import figures
from content.i18n import ABOUT, EXPERIENCE, FOOTER, HOME, NAV, NOT_FOUND, NOTES_ZH, WORK_ZH

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
SITE = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
WORK = json.loads((ROOT / "content" / "work.json").read_text(encoding="utf-8"))

env = Environment(
    loader=FileSystemLoader(ROOT / "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def split_front(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, m.group(2)


def render_markdown(body):
    md = markdown.Markdown(extensions=["fenced_code", "tables", "smarty", "toc", "footnotes"])
    out = md.convert(body)
    out = re.sub(r"<p>\[\[figure:([a-z0-9-]+)\]\]</p>", lambda m: figures.render(m.group(1)), out)
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return out


def load_notes():
    notes = []
    for path in sorted((ROOT / "content" / "notes").glob("*.md")):
        meta, body = split_front(path.read_text(encoding="utf-8"))
        notes.append(
            {
                "slug": meta["slug"],
                "title": meta["title"],
                "summary": meta["summary"],
                "order": int(meta["order"]),
                "html": render_markdown(body),
                "url": f"/notes/{meta['slug']}/",
            }
        )
    notes.sort(key=lambda n: n["order"])
    return notes


def work_for(lang, by_slug):
    """Project rows for one language: English as authored in work.json, Chinese overlaid from WORK_ZH."""
    note_label = "Note" if lang == "en" else "笔记（英文）"
    rows = []
    for row in WORK:
        row = dict(row)
        if lang == "zh":
            row.update(WORK_ZH.get(row["name"], {}))
            row["links"] = [{"label": WORK_ZH[row["name"]]["repo_label"], "href": l["href"]} for l in row["links"]]
        else:
            row["links"] = list(row["links"])
        if row.get("note") and row["note"] in by_slug:
            row["links"].append({"label": note_label, "href": by_slug[row["note"]]["url"]})
        rows.append(row)
    return rows


def note_cards_for(lang, notes):
    """Cards for the home page: Chinese title and summary on /zh/ (the notes themselves stay English)."""
    if lang == "en":
        return notes
    return [dict(n, **NOTES_ZH[n["slug"]]) if n["slug"] in NOTES_ZH else n for n in notes]


def write(rel, content):
    target = DIST / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def page(template, rel, lang, **ctx):
    ctx.setdefault("site", SITE)
    ctx["lang"] = lang
    ctx["nav"] = NAV[lang]
    ctx["footer_note"] = FOOTER[lang]["note"]
    write(rel, env.get_template(template).render(**ctx))


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ROOT / "static", DIST / "static")

    notes = load_notes()
    by_slug = {n["slug"]: n for n in notes}
    hero_note = by_slug.get("simulation-cannot-see-a-cache")

    for lang, prefix in (("en", ""), ("zh", "/zh")):
        page(
            "home.html", f"{prefix}/index.html".lstrip("/"), lang,
            t=HOME[lang], work=work_for(lang, by_slug), notes=notes, note_cards=note_cards_for(lang, notes),
            experience=EXPERIENCE[lang],
            hero_chart=figures.render("hit-rate-compact", lang=lang), hero_note=hero_note,
            path=f"{prefix}/", alt_path=("/" if lang == "zh" else "/zh/"),
            page_title=None, description=SITE["description"] if lang == "en" else SITE["description_zh"],
        )
        page(
            "about.html", f"{prefix}/about/index.html".lstrip("/"), lang,
            t=ABOUT[lang], notes=notes,
            path=f"{prefix}/about/", alt_path=("/about/" if lang == "zh" else "/zh/about/"),
            page_title=ABOUT[lang]["eyebrow"], description=f'{ABOUT[lang]["h1"]} {ABOUT[lang]["f_looking_v"]}',
        )

    # Notes stay English-only: substantial technical write-ups, not yet translated.
    if notes:
        page("notes.html", "notes/index.html", "en", notes=notes, path="/notes/", alt_path="/zh/",
             page_title="Notes", description="Short notes on what a measurement taught me.")
    for i, note in enumerate(notes):
        page(
            "note.html", f"notes/{note['slug']}/index.html", "en", note=note,
            newer=notes[i - 1] if i > 0 else None, older=notes[i + 1] if i + 1 < len(notes) else None,
            notes=notes, path=note["url"], alt_path="/zh/", page_title=note["title"], description=note["summary"],
        )
    page("404.html", "404.html", "en", t=NOT_FOUND["en"], notes=notes, path="/404.html", alt_path="/zh/",
         page_title="Not found", description="This page does not exist.")

    urls = ["/", "/zh/", "/about/", "/zh/about/"] + (["/notes/"] if notes else []) + [n["url"] for n in notes]
    write(
        "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{SITE['url']}{u}</loc></url>" for u in urls)
        + "</urlset>",
    )
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    print(f"built {len(notes)} notes into {DIST}, in English and Chinese")


if __name__ == "__main__":
    sys.exit(main())
