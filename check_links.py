#!/usr/bin/env python3
"""Fail if any internal link or asset in dist/ points at a file that does not exist."""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

DIST = Path(__file__).parent / "dist"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.found.append(value)


def target(url, page):
    parsed = urlparse(url)
    if parsed.scheme or parsed.netloc or url.startswith(("mailto:", "#")):
        return None
    path = parsed.path
    file = DIST / path.lstrip("/") if path.startswith("/") else page.parent / path
    return file / "index.html" if file.is_dir() or not file.suffix else file


def main():
    bad = []
    for page in DIST.rglob("*.html"):
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8"))
        for url in parser.found:
            file = target(url, page)
            if file is not None and not file.exists():
                bad.append(f"{page.relative_to(DIST)}: {url}")
    if bad:
        print("broken internal links:\n  " + "\n  ".join(sorted(set(bad))))
        return 1
    print(f"links ok in {len(list(DIST.rglob('*.html')))} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
