COMPILER := latexmk -cd -interaction=batchmode -time -bibtex -e '$$biber="biber --isbn-normalise %O %S"'

.PHONY: clean

notebook.pdf: notebook.tex bib/*.bib packages/*.sty src/*.tex
ifdef only
	$(COMPILER) notebook.tex -pdflua -usepretex="\includeonly{$(only)}" $(args)
else
	$(COMPILER) notebook.tex -pdflua $(args)
endif

clean:
	rm -fv notebook.pdf
	rm -fv {,src/}*.log # luatex
	rm -fv {,src/}*.{aux,log,out,fls,toc} # latex
	rm -fv {,src/}*.fdb_latexmk # latexmk
	rm -fv {,src/}*.{bbl,bcf,blg,run.xml} # biber
	rm -fv {,src/}*.{idx,ilg,ind} # makeindex
