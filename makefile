COMPILER := pdflatex -interaction=batchmode
FIGURES_TEX := $(patsubst figures/%.tex,figures/%.pdf,$(wildcard figures/*.tex))
FIGURES_ASY := $(patsubst figures/%.asy,figures/%.pdf,$(wildcard figures/*.asy))
SOURCE := notebook.cls notebook.tex bib/*.bib packages/*.sty src/*.tex revision $(FIGURES_TEX) $(FIGURES_ASY)

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

watch:
	@$(COMPILER) notebook.tex || true; \

	@while inotifywait --event modify $(SOURCE); do \
		echo; \
		$(COMPILER) notebook.tex; \
		echo; \
	done

clean:
	rm -fv {,figures/}*.pdf
	rm -fv {,src/,figures/}*.log # tex
	rm -fv {,src/,figures/}*.{aux,out,fls,toc} # latex
	rm -fv {,src/}*.{bbl,bcf,blg,run.xml} # biber
	rm -fv {,src/}*.{idx,ilg,ind} # makeindex

output-revision:
	git --no-pager log -1 --date=short --decorate=short --pretty=format:'%h (%cd)' HEAD > revision
