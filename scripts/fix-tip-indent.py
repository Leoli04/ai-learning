#!/usr/bin/env python3
"""Fix VitePress custom container leading-whitespace bug.

Bug: container opener lines have 2 leading spaces; content / closer lines
do not. markdown-it sees the opener as an indented paragraph and emits a
box with empty body.

Fix: strip exactly the 2 leading spaces from any line that opens with
'  ::: ' (VitePress tip/warning/info/danger/note/details containers),
where the container is top-level (not nested inside a list item). All 19
hits in this repo are top-level per audit; no nested usages exist.
"""
from pathlib import Path
import re

ROOT = Path(r"F:\lixiaofei\WorkBuddy\技术\ai-learning\docs")
# VitePress container keywords (case-insensitive prefix)
KEYWORDS = ("tip", "warning", "info", "danger", "note", "details")

# Match: line that starts with EXACTLY two spaces, then ":::" then space
PATTERN = re.compile(r"^( {2}):::(?= )", re.MULTILINE)


def fix_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    new_text, n = PATTERN.subn(":::", text)
    if n:
        path.write_text(new_text, encoding="utf-8")
    return n


total = 0
hits = []
for md in sorted(ROOT.rglob("*.md")):
    n = fix_file(md)
    if n:
        hits.append((md, n))
        total += n

print(f"Fixed {total} container openers in {len(hits)} files:")
for p, n in hits:
    print(f"  +{n}  {p.relative_to(ROOT)}")