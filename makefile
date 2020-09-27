COMPILER := latexmk -cd -interaction=nonstopmode -bibtex -time -e '$$biber="biber --isbn-normalise %O %S"'

.PHONY: clean

notebook.pdf: notebook.tex bib/*.bib packages/*.sty src/*.tex
	$(COMPILER) notebook.tex -pdf

clean:
	$(COMPILER) notebook.tex -C
	rm -fv src/*.aux
	rm -fv *.run.xml *.tex.bbl *.tex.blg # biber
	rm -fv *.{aoc,lem,usc} # tocloft
