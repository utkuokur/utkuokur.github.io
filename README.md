# utkuokur.github.io

Personal website of Utku Okur, served by GitHub Pages at
<https://utkuokur.github.io/>. Plain HTML and CSS (`.nojekyll` keeps GitHub
from running Jekyll). All links between pages are relative.

| Path | Content |
| --- | --- |
| `index.html` | Home: short bio |
| `publications/` | Papers (generated from `cv/publications.tex`) and theses |
| `other-writings/` | Work outside journals (generated from `cv/other_writings.tex`) |
| `contact/` | Address |
| `cv/cv.tex` | CV source |
| `cv/publications.tex` | The list of papers, newest first |
| `cv/other_writings.tex` | Workshop abstracts, formalisations, unpublished preprints, newest first |
| `cv/paperlist.sty` | Formatting and countdown numbering for both lists |
| `scripts/build_publications.py` | Copies both lists into their website pages |
| `slides/` | Talk slides (PDF), linked from the website only |
| `assets/` | Stylesheet, favicon, link icons (arXiv, Google Scholar, ORCID, GitHub from Simple Icons, CC0) |
| `cv/icons/` | Logos used in the CV (PDF, converted from `assets/icons/`) |
| `lean-challenges/` | Redirect to the Ten Challenges website (keep: older links point here) |

The sidebar is repeated in each page, so a new nav entry has to be added to
all four `index.html` files.

## Papers and CV

The papers are listed once, as `\paper{authors}{title}{venue}{arXiv id}{DOI}`
entries in `cv/publications.tex`, newest first. Work that is not in a journal
(workshop abstracts, formalisations, preprints that will not be published) goes
in `cv/other_writings.tex` in the same format; it is listed without numbers
and does not count towards the paper total. Anything inside `\webonly{...}`
in an entry (such as a link to talk slides in `slides/`) appears on the website
but not in the CV. After editing either file or the CV, run

```sh
make
```

in the repository root. It rewrites the lists on the Publications and Other
writings pages (same order as in the files) and compiles `cv/cv.pdf`. Then
commit and push.

To use the list in another LaTeX document (a grant application, say), put
`\usepackage{paperlist}` in its preamble and `\input{publications}` (and/or
`\input{other_writings}`) where the list should go, with `cv/` on the TeX
search path or the files copied next to the document.

The `CV` link in the sidebar opens `cv/cv.pdf`.

## Preview locally

```sh
python3 -m http.server 8000 --directory /home/uokur/the_workspace/utkuokur.github.io
```

then open <http://localhost:8000/>.
