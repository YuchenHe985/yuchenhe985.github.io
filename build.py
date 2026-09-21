#!/usr/bin/env python3
"""Build the site into dist/.

    python3 build.py          # writes dist/
    python3 -m http.server -d dist 8000

Notes are Markdown files in content/notes/ with a small front-matter block and are listed in the order given by
`order`. A line containing only [[figure:name]] is replaced by a chart from figures.py.
"""
import json
import re
import shutil
import sys
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

import figures

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


def write(rel, content):
    target = DIST / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def page(template, rel, **ctx):
    ctx.setdefault("site", SITE)
    write(rel, env.get_template(template).render(**ctx))


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ROOT / "static", DIST / "static")

    notes = load_notes()
    by_slug = {n["slug"]: n for n in notes}
    # A project row links to its note when there is one.
    work = []
    for row in WORK:
        links = [l for l in row["links"] if "href" in l]
        if row.get("note") and row["note"] in by_slug:
            links.append({"label": "Note", "href": by_slug[row["note"]]["url"]})
        work.append({**row, "links": links})
    hero_note = by_slug.get("simulation-cannot-see-a-cache")

    page("home.html", "index.html", notes=notes, work=work, hero_chart=figures.render("hit-rate-compact"),
         hero_note=hero_note, path="/", page_title=None, description=SITE["description"])
    page("about.html", "about/index.html", notes=notes, path="/about/", page_title="About",
         description="Master's student in Electrical Engineering at Penn. How I approach a project, and how to reach me.")
    if notes:
        page("notes.html", "notes/index.html", notes=notes, path="/notes/", page_title="Notes",
             description="Short notes on what a measurement taught me.")
    for i, note in enumerate(notes):
        page("note.html", f"notes/{note['slug']}/index.html", note=note, newer=notes[i - 1] if i > 0 else None,
             older=notes[i + 1] if i + 1 < len(notes) else None, notes=notes, path=note["url"],
             page_title=note["title"], description=note["summary"])
    page("404.html", "404.html", notes=notes, path="/404.html", page_title="Not found", description="This page does not exist.")

    urls = ["/", "/about/"] + (["/notes/"] if notes else []) + [n["url"] for n in notes]
    write(
        "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{SITE['url']}{u}</loc></url>" for u in urls)
        + "</urlset>",
    )
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    print(f"built {len(notes)} notes into {DIST}")


if __name__ == "__main__":
    sys.exit(main())
