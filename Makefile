COMPILER := pdflatex -interaction=batchmode
FIGURES_TEX_PDF := $(patsubst figures/%.tex,output/%.pdf,$(wildcard figures/*.tex))
FIGURES_ASY_PDF := $(patsubst figures/%.asy,output/%.pdf,$(wildcard figures/*.asy))
FIGURES_PY_PDF := $(patsubst src/notebook/figures/%.py,output/%.pdf,$(filter-out src/notebook/figures/__init__.py, $(wildcard src/notebook/figures/*.py)))
TEXT_SOURCE := notebook.tex classes/notebook.cls bibliography/*.bib asymptote/*.asy asymptote/geom/*.asy asymptote/graphs/*.asy asymptote/square_grid_automaton/*.asy packages/*.sty text/*.tex $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF) $(FIGURES_PY_PDF)

.PHONY: figures clean clean-text clean-figures
.DEFAULT_GOAL := output/notebook.pdf

aux:
	mkdir --parents aux

aux/text:
	mkdir --parents aux/text

output:
	mkdir --parents output

output/notebook.pdf: $(TEXT_SOURCE) images/*.png $(wildcard includeonly metadata) | aux aux/text output
	$(COMPILER) -output-directory=aux -draftmode notebook.tex
	biber --quiet aux/notebook.bcf
	$(COMPILER) -output-directory=aux -draftmode notebook.tex
	$(COMPILER) -output-directory=aux notebook.tex
	cat aux/notebook.pdf > output/notebook.pdf

output/%.pdf: figures/%.tex classes/*.cls packages/*.sty | aux output
	$(COMPILER) -output-directory=aux figures/$*.tex
	cat aux/$*.pdf > output/$*.pdf

output/%.pdf: figures/%.asy asymptote/*.asy asymptote/geom/*.asy asymptote/graphs/*.asy asymptote/square_grid_automaton/*.asy | aux output
	$(if $(shell grep 'import three' figures/$*.asy),xvfb-run --auto-servernum,) asy -outname=aux/$* figures/$*.asy
	cat aux/$*.pdf > output/$*.pdf

output/%.pdf: src/notebook/figures/%.py | aux output
	poetry run python -m src.notebook.figures.$*
	cat aux/$*.pdf > output/$*.pdf

figures: $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF) $(FIGURES_PY_PDF)

metadata: .git/refs/heads/master
	LC_ALL=en_US.UTF-8 git log --max-count 1 --format=format:'commit={%h},date={%cd}' --date='format:%d %B %Y' HEAD > metadata
	LC_ALL=en_US.UTF-8 git log --max-count 1 --format=format:',pdfdate={%cd}' --date='format:D:%Y%m%d%H%M%S' HEAD >> metadata

clean-text:
	rm --recursive --force aux/text aux/notebook.* output/notebook.pdf

clean-figures:
	rm --recursive --force aux output

clean: clean-text clean-figures
