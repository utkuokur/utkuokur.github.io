#!/usr/bin/env python3
"""Regenerate the lists on the website from the CV sources.

cv/publications.tex   -> publications/index.html
cv/other_writings.tex -> other-writings/index.html

Every \\paper{authors}{title}{venue}{arXiv id}{DOI} entry in a source file
becomes one list item, in the order it appears there. Only the part of each
page between its BEGIN and END markers is rewritten.

Usage (from the repository root):  python3 scripts/build_publications.py
"""

import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
# (source, page, name used in the page's BEGIN/END markers)
LISTS = [
    ("cv/publications.tex", "publications/index.html", "papers"),
    ("cv/other_writings.tex", "other-writings/index.html", "other writings"),
]

INLINE_MACROS = {"emph": "em", "textit": "i", "textbf": "strong"}


def strip_comments(tex):
    # As in LaTeX, a comment also swallows the line break and the next line's indentation.
    return re.sub(r"(?<!\\)%[^\n]*(\n[ \t]*)?", "", tex)


def read_group(tex, i):
    """Return the contents of the {...} group starting at tex[i] and the index after it."""
    if tex[i] != "{":
        raise ValueError(f"expected '{{' near: {tex[i:i + 40]!r}")
    depth = 0
    j = i
    while j < len(tex):
        c = tex[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return tex[i + 1:j], j + 1
        j += 1
    raise ValueError(f"unbalanced braces near: {tex[i:i + 40]!r}")


def papers(tex):
    tex = strip_comments(tex)
    entries = []
    for m in re.finditer(r"\\paper\s*(?=\{)", tex):
        i, args = m.end(), []
        for _ in range(5):
            while tex[i].isspace():
                i += 1
            arg, i = read_group(tex, i)
            args.append(" ".join(arg.split()))
        entries.append(args)
    return entries


def to_html(s):
    """Convert the small LaTeX subset allowed in \\paper entries to HTML."""
    # \webonly{...} is dropped from the PDF but kept here.
    while m := re.search(r"\\webonly\s*(?=\{)", s):
        inner, end = read_group(s, m.end())
        s = s[:m.start()] + inner + s[end:]
    out = html.escape(s, quote=False).replace("\\&amp;", "&amp;")
    # Set \href links aside so the replacements below leave their URLs alone.
    urls = []

    def stash(m):
        urls.append(m.group(1).replace('"', "&quot;"))
        return f"\x00{len(urls) - 1}\x01{m.group(2)}\x02"

    out = re.sub(r"\\href\{([^{}]*)\}\{([^{}]*)\}", stash, out)
    out = re.sub(r"\$([^$]*)\$", r"<i>\1</i>", out)
    out = out.replace("</i>-", "</i>&#8209;")  # keep "E-cospectral" on one line
    changed = True
    while changed:
        changed = False
        for macro, tag in INLINE_MACROS.items():
            new = re.sub(r"\\%s\{([^{}]*)\}" % macro, r"<%s>\1</%s>" % (tag, tag), out)
            changed |= new != out
            out = new
    out = out.replace("---", "&mdash;").replace("--", "&ndash;")
    out = out.replace("~", "&nbsp;").replace("\\,", "&thinsp;").replace("\\ ", " ")
    out = out.replace("{", "").replace("}", "")
    if "\\" in out:
        raise ValueError(f"unsupported LaTeX in {s!r}; use UTF-8 accents and plain text")
    return re.sub(r"\x00(\d+)\x01(.*?)\x02",
                  lambda m: f'<a href="{urls[int(m.group(1))]}">{m.group(2)}</a>', out)


def item(authors, title, venue, arxiv, doi):
    links = []
    if arxiv:
        links.append(f'<a href="https://arxiv.org/abs/{html.escape(arxiv)}">arXiv</a>')
    if doi:
        links.append(f'<a href="https://doi.org/{html.escape(doi)}">DOI</a>')
    lines = [
        "      <li>",
        f'        <div class="entry-title">{to_html(title)}</div>',
        f'        <div class="entry-meta">{to_html(authors)}<br>{to_html(venue)}</div>',
    ]
    if links:
        lines.append(f'        <div class="entry-links">{" ".join(links)}</div>')
    lines.append("      </li>")
    return "\n".join(lines)


def build(source, page_path, name):
    begin = (f"<!-- BEGIN {name}: generated from {source} by "
             f"scripts/build_publications.py; edit that file, not this list -->")
    end_marker = f"<!-- END {name} -->"
    entries = papers((ROOT / source).read_text(encoding="utf-8"))
    if not entries:
        sys.exit(f"no \\paper entries found in {source}")
    page = (ROOT / page_path).read_text(encoding="utf-8")
    start, end = page.find(begin), page.find(end_marker)
    if start < 0 or end < start:
        sys.exit(f"markers not found in {page_path}")
    items = "\n".join(item(*e) for e in entries)
    page = page[:start + len(begin)] + "\n" + items + "\n      " + page[end:]
    (ROOT / page_path).write_text(page, encoding="utf-8")
    print(f"wrote {len(entries)} entries to {page_path}")


def main():
    for source, page_path, name in LISTS:
        build(source, page_path, name)


if __name__ == "__main__":
    main()
