COMPILER := pdflatex -interaction=batchmode
FIGURES_TEX_PDF := $(patsubst figures/%.tex,figures/%.pdf,$(wildcard figures/*.tex))
FIGURES_ASY_PDF := $(patsubst figures/%.asy,figures/%.pdf,$(wildcard figures/*.asy))
DOC_SOURCE := notebook.cls notebook.tex bib/*.bib packages/*.sty src/*.tex $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF)

.PHONY: full figures watch clean

full:
	$(COMPILER) -draftmode notebook.tex
	biber notebook.bcf
	$(COMPILER) -draftmode notebook.tex
	$(COMPILER) notebook.tex

notebook.pdf: $(DOC_SOURCE)
	$(COMPILER) notebook.tex

figures/%.pdf: tikzcd.cls packages/*.sty figures/%.tex
	cd figures && $(COMPILER) $*.tex

figures/%.pdf: figures/%.asy
	cd figures && asy $*.asy

figures: $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF)

# I have implemented a very useful build system for LaTeX with log processing and debouncing
watch:
	@poetry run python watcher.py

clean:
	rm -fv {,figures/}*.pdf
	rm -fv {,src/,figures/}*.log # tex
	rm -fv {,src/,figures/}*.{aux,out,fls,toc} # latex
	rm -fv {,src/}*.{bbl,bcf,blg,run.xml} # biber
	rm -fv git-commit-info

git-commit-info: .git/refs/heads/master
	LC_ALL=en_BG.UTF-8 git log --max-count 1 --format=format:'hash={%h},date={%cd}' --date='format:%d %B %Y' HEAD > git-commit-info
