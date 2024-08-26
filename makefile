COMPILER := pdflatex -interaction=batchmode
FIGURES_TEX_PDF := $(patsubst figures/%.tex,output/%.pdf,$(wildcard figures/*.tex))
FIGURES_ASY_PDF := $(patsubst figures/%.asy,output/%.eps,$(wildcard figures/*.asy))
TEXT_SOURCE := notebook.tex classes/notebook.cls bibliography/*.bib packages/*.sty text/*.tex $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF)

.PHONY: figures clean
.DEFAULT_GOAL := output/notebook.pdf

aux:
	mkdir --parents aux

output:
	mkdir --parents output

output/notebook.pdf: $(TEXT_SOURCE) images/*.png | aux output
	$(COMPILER) -output-directory=aux -draftmode notebook.tex
	biber --quiet aux/notebook.bcf
	$(COMPILER) -output-directory=aux -draftmode notebook.tex
	$(COMPILER) -output-directory=aux notebook.tex
	cat aux/notebook.pdf > output/notebook.pdf

output/%.pdf: classes/*.cls packages/*.sty figures/%.tex | aux output
	$(COMPILER) -output-directory=aux figures/$*.tex
	cat aux/$*.pdf > output/$*.pdf

output/%.eps: figures/%.asy | aux output
	asy -quiet -render=5 -outname=aux/$* figures/$*.asy
	cat aux/$*.eps > output/$*.eps

figures: $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF)

git-commit-info: .git/refs/heads/master
	LC_ALL=en_US.UTF-8 git log --max-count 1 --format=format:'hash={%h},date={%cd}' --date='format:%d %B %Y' HEAD > git-commit-info

clean:
	rm --recursive --force aux output
