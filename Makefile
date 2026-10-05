# Rebuild everything generated from the CV sources: run `make` after editing
# cv/cv.tex, cv/publications.tex or cv/other_writings.tex.

all: publications/index.html other-writings/index.html cv/cv.pdf

publications/index.html other-writings/index.html &: cv/publications.tex cv/other_writings.tex scripts/build_publications.py
	python3 scripts/build_publications.py

cv/cv.pdf: cv/cv.tex cv/publications.tex cv/other_writings.tex cv/paperlist.sty
	cd cv && latexmk -pdf -interaction=nonstopmode -halt-on-error cv.tex

.PHONY: all
