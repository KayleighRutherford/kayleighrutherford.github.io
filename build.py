#!/usr/bin/env python3
"""
Builds index.html from src/template.html by inlining fonts and the headshot
photo as base64 data URIs, so the result is a single self-contained file
(no external requests — works offline, and is what gets published/deployed).

Usage:
    python3 build.py

Edit src/template.html for copy/layout/style changes, then re-run this.
To swap the photo, replace assets/headshot.jpg (keep the filename, or update
the path below) and re-run.
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).parent
TEMPLATE = ROOT / "src" / "template.html"
OUTPUT = ROOT / "index.html"

FONTS = {
    "__SERIF_SEMIBOLD__": ROOT / "assets/fonts/serif-semibold.woff2",
    "__SANS_REGULAR__": ROOT / "assets/fonts/sans-regular.woff2",
    "__SANS_SEMIBOLD__": ROOT / "assets/fonts/sans-semibold.woff2",
    "__MONO_REGULAR__": ROOT / "assets/fonts/mono-regular.woff2",
    "__MONO_MEDIUM__": ROOT / "assets/fonts/mono-medium.woff2",
}
PHOTO = {"__HEADSHOT__": ROOT / "assets/headshot.jpg"}


def b64(path: pathlib.Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def main() -> None:
    html = TEMPLATE.read_text()

    for placeholder, path in {**FONTS, **PHOTO}.items():
        if placeholder not in html:
            raise SystemExit(f"placeholder {placeholder} not found in template")
        html = html.replace(placeholder, b64(path))

    OUTPUT.write_text(html)
    print(f"Built {OUTPUT} ({len(html):,} chars)")


if __name__ == "__main__":
    main()
