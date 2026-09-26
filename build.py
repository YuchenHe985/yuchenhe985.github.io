#!/usr/bin/env python3
"""Build the site into dist/, in English at / and Chinese at /zh/.

    python3 build.py          # writes dist/
    python3 -m http.server -d dist 8000

Notes are Markdown files: English in content/notes/, Chinese in content/notes_zh/ (same slugs and order).
A line containing only [[figure:name]] in a note is replaced by a chart from figures.py, in the note's language. Bilingual UI copy and translated project rows live in
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
from content.i18n import ABOUT, EXPERIENCE, FOOTER, HOME, NAV, NOT_FOUND, NOTES_PAGE, WORK_ZH

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


def render_markdown(body, lang="en"):
    md = markdown.Markdown(extensions=["fenced_code", "tables", "smarty", "toc", "footnotes"])
    out = md.convert(body)
    out = re.sub(
        r"<p>\[\[figure:([a-z0-9-]+)\]\]</p>", lambda m: figures.render(m.group(1), lang=lang, strict=True), out
    )
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return out


def load_notes(lang):
    folder = ROOT / "content" / ("notes" if lang == "en" else "notes_zh")
    prefix = "/zh" if lang == "zh" else ""
    notes = []
    for path in sorted(folder.glob("*.md")):
        meta, body = split_front(path.read_text(encoding="utf-8"))
        notes.append(
            {
                "slug": meta["slug"],
                "title": meta["title"],
                "summary": meta["summary"],
                "order": int(meta["order"]),
                "html": render_markdown(body, lang),
                "url": f"{prefix}/notes/{meta['slug']}/",
            }
        )
    notes.sort(key=lambda n: n["order"])
    return notes


def work_for(lang, by_slug):
    """Project rows for one language: English as authored in work.json, Chinese overlaid from WORK_ZH."""
    note_label = "Note" if lang == "en" else "笔记"
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

    notes = {lang: load_notes(lang) for lang in ("en", "zh")}
    assert [n["slug"] for n in notes["en"]] == [n["slug"] for n in notes["zh"]], "English and Chinese notes must match"
    by_slug = {lang: {n["slug"]: n for n in notes[lang]} for lang in notes}

    for lang, prefix in (("en", ""), ("zh", "/zh")):
        other = "en" if lang == "zh" else "zh"
        other_prefix = "/zh" if other == "zh" else ""
        tn = NOTES_PAGE[lang]
        page(
            "home.html", f"{prefix}/index.html".lstrip("/"), lang,
            t=HOME[lang], work=work_for(lang, by_slug[lang]), notes=notes[lang],
            experience=EXPERIENCE[lang],
            hero_chart=figures.render("hit-rate-compact", lang=lang), hero_note=by_slug[lang].get("simulation-cannot-see-a-cache"),
            path=f"{prefix}/", alt_path=f"{other_prefix}/",
            page_title=None, description=SITE["description"] if lang == "en" else SITE["description_zh"],
        )
        page(
            "about.html", f"{prefix}/about/index.html".lstrip("/"), lang,
            t=ABOUT[lang], notes=notes[lang],
            path=f"{prefix}/about/", alt_path=f"{other_prefix}/about/",
            page_title=ABOUT[lang]["eyebrow"], description=f'{ABOUT[lang]["h1"]} {ABOUT[lang]["f_looking_v"]}',
        )
        page(
            "notes.html", f"{prefix}/notes/index.html".lstrip("/"), lang,
            notes=notes[lang], tn=tn, path=f"{prefix}/notes/", alt_path=f"{other_prefix}/notes/",
            page_title=tn["eyebrow"], description=tn["description"],
        )
        for i, note in enumerate(notes[lang]):
            page(
                "note.html", f"{prefix}/notes/{note['slug']}/index.html".lstrip("/"), lang,
                note=note, tn=tn,
                newer=notes[lang][i - 1] if i > 0 else None,
                older=notes[lang][i + 1] if i + 1 < len(notes[lang]) else None,
                notes=notes[lang], path=note["url"], alt_path=by_slug[other][note["slug"]]["url"],
                page_title=note["title"], description=note["summary"],
            )
    page("404.html", "404.html", "en", t=NOT_FOUND["en"], notes=notes["en"], path="/404.html", alt_path="/zh/",
         page_title="Not found", description="This page does not exist.")

    urls = ["/", "/zh/", "/about/", "/zh/about/", "/notes/", "/zh/notes/"] + [n["url"] for lang in notes for n in notes[lang]]
    write(
        "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{SITE['url']}{u}</loc></url>" for u in urls)
        + "</urlset>",
    )
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    print(f"built {len(notes['en'])} notes into {DIST}, in English and Chinese")


if __name__ == "__main__":
    sys.exit(main())
