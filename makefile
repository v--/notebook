COMPILER := pdflatex -interaction=batchmode
FIGURES_TEX_PDF := $(patsubst figures/%.tex,output/%.pdf,$(wildcard figures/*.tex))
FIGURES_ASY_PDF := $(patsubst figures/%.asy,output/%.pdf,$(wildcard figures/*.asy))
DOC_SOURCE := notebook.cls notebook.tex bib/*.bib packages/*.sty src/*.tex $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF)

.PHONY: full format-figures figures watch clean

output/notebook.pdf: $(DOC_SOURCE)
	$(COMPILER) -output-directory=aux -draftmode notebook.tex
	biber aux/notebook.bcf
	$(COMPILER) -output-directory=aux -draftmode notebook.tex
	$(COMPILER) -output-directory=aux notebook.tex
	cat aux/notebook.pdf > output/notebook.pdf

output/%.pdf: tikzcd.cls packages/*.sty figures/%.tex
	$(COMPILER) -output-directory=aux figures/$*.tex
	cat aux/$*.pdf > output/$*.pdf

output/%.pdf: figures/%.asy
	asy -outname=aux/$*.asy figures/$*.asy
	cat aux/$*.pdf > output/$*.pdf

figures: $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF)

format-figures:
	@poetry run python format-tex-matrices.py figures/*.tex

# I have implemented a very useful build system for LaTeX with log processing and debouncing
watch:
	@poetry run python watcher.py

git-commit-info: .git/refs/heads/master
	LC_ALL=en_US.UTF-8 git log --max-count 1 --format=format:'hash={%h},date={%cd}' --date='format:%d %B %Y' HEAD > git-commit-info
