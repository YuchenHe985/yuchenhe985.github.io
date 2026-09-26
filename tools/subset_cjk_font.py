#!/usr/bin/env python3
"""Regenerate the Chinese webfont subsets in static/fonts/ from the characters the built Chinese pages use.

    python3 build.py && python3 tools/subset_cjk_font.py && python3 build.py

Run it after adding or changing Chinese text; `--check` only reports characters the current subset lacks.
Needs fontTools with brotli (pip install fonttools brotli) and the Source Han Sans CN OTF files
(Regular and Bold), which are not in the repository:
https://github.com/adobe-fonts/source-han-sans/releases (SIL Open Font License, see static/fonts/licenses/).
"""
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "static" / "fonts"
SOURCES = {"Regular": Path.home() / "Library/Fonts/SourceHanSansCN-Regular.otf", "Bold": Path.home() / "Library/Fonts/SourceHanSansCN-Bold.otf"}
EXTRA = "“”‘’…—–·•→←×÷²³°±≈≤≥µμ"


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chunks, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        self.skip += tag in ("script", "style")

    def handle_endtag(self, tag):
        self.skip -= tag in ("script", "style")

    def handle_data(self, data):
        if not self.skip:
            self.chunks.append(data)


def used_characters():
    chars = set(chr(c) for c in range(0x20, 0x7F)) | set(EXTRA)
    for path in (ROOT / "dist" / "zh").rglob("*.html"):
        parser = Text()
        parser.feed(path.read_text(encoding="utf-8"))
        chars |= set("".join(parser.chunks))
    chars.discard("\n")
    return "".join(sorted(chars))


def covered(woff2):
    """Characters a .woff2 file can draw. Reading WOFF2 needs brotli, so use the interpreter pyftsubset runs under."""
    python = Path(shutil.which("pyftsubset")).read_text().splitlines()[0][2:].strip()
    code = "import sys; from fontTools.ttLib import TTFont; print(''.join(map(chr, TTFont(sys.argv[1]).getBestCmap())))"
    out = subprocess.run([python, "-c", code, str(woff2)], check=True, capture_output=True, text=True).stdout
    return set(out.rstrip("\n"))


def main():
    chars = used_characters()
    if "--check" in sys.argv:
        have = covered(FONTS / "SourceHanSansCN-Regular.subset.woff2")
        missing = [c for c in chars if c not in have and not c.isspace()]
        print(f"{len(chars)} characters used, {len(missing)} missing from the subset: {''.join(missing)}")
        return 1 if missing else 0
    text_file = ROOT / "dist" / "_cjk_chars.txt"
    text_file.write_text(chars, encoding="utf-8")
    for weight, source in SOURCES.items():
        out = FONTS / f"SourceHanSansCN-{weight}.subset.woff2"
        subprocess.run(
            ["pyftsubset", str(source), f"--text-file={text_file}", "--flavor=woff2", "--layout-features=*", f"--output-file={out}"],
            check=True,
        )
        print(f"{out.name}: {out.stat().st_size // 1024} KB")
    text_file.unlink()
    print(f"{len(chars)} characters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
