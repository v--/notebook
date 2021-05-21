COMPILER := pdflatex -interaction=batchmode
SOURCE := notebook.cls notebook.tex bib/*.bib packages/*.sty src/*.tex revision

.PHONY: watch clean output-revision

notebook.pdf: $(SOURCE)
	$(COMPILER) -draftmode notebook.tex
	biber notebook.bcf
	makeindex notebook.idx -o notebook.ind
	$(COMPILER) -draftmode notebook.tex
	$(COMPILER) notebook.tex

watch:
	@$(COMPILER) notebook.tex; \

	@while inotifywait --event modify $(SOURCE); do \
		echo; \
		$(COMPILER) notebook.tex; \
		echo; \
	done

clean:
	rm -fv notebook.pdf
	rm -fv {,src/}*.log # tex
	rm -fv {,src/}*.{aux,out,fls,toc} # latex
	rm -fv {,src/}*.{bbl,bcf,blg,run.xml} # biber
	rm -fv {,src/}*.{idx,ilg,ind} # makeindex

output-revision:
	git --no-pager log -1 --date=short --decorate=short --pretty=format:'%h (%cd)' HEAD > revision
