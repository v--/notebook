COMPILER := pdflatex -interaction=batchmode
FIGURES_TEX_PDF := $(patsubst figures/%.tex,output/%.pdf,$(wildcard figures/*.tex))
FIGURES_ASY_PDF := $(patsubst figures/%.asy,output/%.pdf,$(wildcard figures/*.asy))
TEXT_SOURCE := notebook.tex classes/notebook.cls bibliography/*.bib packages/*.sty text/*.tex $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF)

.PHONY: notebook figures watch watch-figures format-figures clean

notebook: output/notebook.pdf

aux:
	mkdir --parents aux

output:
	mkdir --parents output

output/notebook.pdf: $(TEXT_SOURCE) | aux output
	$(COMPILER) -output-directory=aux -draftmode notebook.tex
	biber --quiet aux/notebook.bcf
	$(COMPILER) -output-directory=aux -draftmode notebook.tex
	$(COMPILER) -output-directory=aux notebook.tex
	cat aux/notebook.pdf > output/notebook.pdf

output/%.pdf: classes/tikzcd.cls packages/*.sty figures/%.tex | aux output
	$(COMPILER) -output-directory=aux figures/$*.tex
	cat aux/$*.pdf > output/$*.pdf

output/%.pdf: figures/%.asy | aux output
	asy -quiet -outname=aux/$*.pdf figures/$*.asy
	cat aux/$*.pdf > output/$*.pdf

figures: $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF)

format-figures:
	@$(MAKE) --no-print-directory --directory code format-figures

# I have implemented a very useful build system for LaTeX with log processing and debouncing
watch: | aux output
	@$(MAKE) --no-print-directory --directory code watch

watch-figures: | aux output
	@$(MAKE) --no-print-directory --directory code watch-figures

git-commit-info: .git/refs/heads/master
	LC_ALL=en_US.UTF-8 git log --max-count 1 --format=format:'hash={%h},date={%cd}' --date='format:%d %B %Y' HEAD > git-commit-info

clean:
	rm --recursive --force aux output
