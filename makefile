COMPILER := pdflatex -interaction=batchmode
FIGURES_TEX := $(patsubst figures/%.tex,figures/%.pdf,$(wildcard figures/*.tex))
FIGURES_ASY := $(patsubst figures/%.asy,figures/%.pdf,$(wildcard figures/*.asy))
SOURCE := notebook.cls notebook.tex bib/*.bib packages/*.sty src/*.tex $(FIGURES_TEX) $(FIGURES_ASY)

.PHONY: figures watch clean output-revision

notebook.pdf: $(SOURCE)
	$(COMPILER) -draftmode notebook.tex
	biber notebook.bcf
	makeindex notebook.idx -o notebook.ind
	$(COMPILER) -draftmode notebook.tex
	$(COMPILER) notebook.tex

figures/%.pdf: figures/%.tex
	cd figures && $(COMPILER) $*.tex

figures/%.pdf: figures/%.asy
	cd figures && asy $*.asy

figures: $(FIGURES_TEX) $(FIGURES_ASY)

watch: figures
	@find $(SOURCE) | entr $(COMPILER) notebook.tex;

clean:
	rm -fv {,figures/}*.pdf
	rm -fv {,src/,figures/}*.log # tex
	rm -fv {,src/,figures/}*.{aux,out,fls,toc} # latex
	rm -fv {,src/}*.{bbl,bcf,blg,run.xml} # biber
	rm -fv {,src/}*.{idx,ilg,ind} # makeindex
	rm -fv git-commit-info

git-commit-info: .git/refs/heads/master
	LC_ALL=en_BG.UTF-8 git log --max-count 1 --format=format:'hash={%h},date={%cd}' --date='format:%d %B %Y' HEAD > git-commit-info
