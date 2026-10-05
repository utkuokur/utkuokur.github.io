# personal-webpage

Personal website of Utku Okur, served by GitHub Pages at
<https://utkuokur.github.io/personal-webpage/>. Plain HTML and CSS, no build
step (`.nojekyll` keeps GitHub from running Jekyll). All links between pages
are relative, so the site works under any URL prefix.

| Path | Content |
| --- | --- |
| `index.html` | Home: short bio and research topics |
| `publications/` | Journal articles, preprints, theses |
| `code/` | Selected repositories and formalization projects |
| `contact/` | Address and profile links |
| `cv/cv.tex` | CV source (skeleton, to be filled in) |
| `assets/` | Stylesheet, light/dark toggle, favicon |
| `lean-challenges/` | Redirect to the Ten Challenges website (from when this repo was `utkuokur.github.io`) |

The sidebar is repeated in each page, so a new nav entry has to be added to
all four `index.html` files.

## CV

Build with `latexmk -pdf cv/cv.tex` (run inside `cv/`), commit `cv/cv.pdf`,
and change the `CV` links (sidebar of every page, and the link row on the
home page) from the Google Drive URL to `cv/cv.pdf` on the home page and
`../cv/cv.pdf` on the other pages.

## Preview locally

```sh
python3 -m http.server 8000 --directory /home/uokur/the_workspace/personal-webpage
```

then open <http://localhost:8000/>.
