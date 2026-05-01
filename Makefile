DOC_COMPILER := lualatex -interaction=batchmode
FIGURE_COMPILER := pdflatex -interaction=batchmode
FIGURES_TEX_PDF := $(patsubst figures/%.tex,output/%.pdf,$(wildcard figures/*.tex))
FIGURES_ASY_PDF := $(patsubst figures/%.asy,output/%.pdf,$(wildcard figures/*.asy))
FIGURES_PY_PDF := $(patsubst src/notebook/figures/%.py,output/%.pdf,$(filter-out src/notebook/figures/__init__.py, $(wildcard src/notebook/figures/*.py)))
PYTHON_SOURCE := $(wildcard src/*.py)
TEXT_SOURCE := notebook.tex classes/notebook.cls bibliography/*.bib asymptote/*.asy asymptote/geom/*.asy asymptote/graphs/*.asy asymptote/square_grid_automaton/*.asy packages/*.sty text/*.tex aux/corderef.aux $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF) $(FIGURES_PY_PDF)

.PHONY: figures clean clean-text clean-figures touch-figures checkcites
.DEFAULT_GOAL := output/notebook.pdf

aux:
	mkdir --parents aux

aux/text:
	mkdir --parents aux/text

output:
	mkdir --parents output

# LaTeX compilation is complicated, so we avoid using Make for intermediate files in aux/
# In the end, we use dd to copy the result (cp messes up reloading of PDF files in viewers)
output/notebook.pdf: $(TEXT_SOURCE) images/*.png $(wildcard includeonly metadata) | aux aux/text output
	$(DOC_COMPILER) -output-directory=aux -draftmode notebook.tex
	biber --quiet aux/notebook.bcf
	$(DOC_COMPILER) -output-directory=aux -draftmode notebook.tex
	$(DOC_COMPILER) -output-directory=aux notebook.tex
	dd status=none if=aux/notebook.pdf of=output/notebook.pdf

output/%.pdf: figures/%.tex classes/*.cls packages/*.sty | aux output
	$(FIGURE_COMPILER) -output-directory=aux figures/$*.tex
	dd status=none if=aux/$*.pdf of=output/$*.pdf

# Asymptote may fail silently, so we remove the aux file prior to making a new one
output/%.pdf: figures/%.asy asymptote/*.asy asymptote/geom/*.asy asymptote/graphs/*.asy asymptote/square_grid_automaton/*.asy | aux output
	rm --force aux/$*.pdf
	asy -outname=aux/$* figures/$*.asy
	dd status=none if=aux/$*.pdf of=output/$*.pdf

output/%.pdf: src/notebook/figures/%.py | aux output
	uv run python -m src.notebook.figures.$*
	dd status=none if=aux/$*.pdf of=output/$*.pdf

figures: $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF) $(FIGURES_PY_PDF)

# This is occasionally useful in those cases when some TeX/asymptote module is updated,
# but the update does not require rebuilding all figures
touch-figures:
	touch $(FIGURES_TEX_PDF)

aux/metadata: .git/refs/heads/master | aux
	LC_ALL=en_US.UTF-8 git log --max-count 1 --format=format:'commit={%h},date={%cd}' --date='format:%d %B %Y' HEAD > aux/metadata
	LC_ALL=en_US.UTF-8 git log --max-count 1 --format=format:',pdfdate={%cd}' --date='format:D:%Y%m%d%H%M%S' HEAD >> aux/metadata

aux/corderef.aux: $(PYTHON_SOURCE) | aux
	uv run coderefs collect

clean-text:
	rm --recursive --force aux/text aux/notebook.* output/notebook.pdf

clean-figures:
	rm --recursive --force aux output

clean: clean-text clean-figures

checkcites:
	checkcites --backend biber --crossrefs --all aux/notebook.bcf
