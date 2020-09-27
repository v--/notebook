COMPILER := latexmk -cd -interaction=nonstopmode -bibtex -time

.PHONY: clean

notebook.pdf: notebook.tex bib/*.bib packages/*.sty src/*.tex
	$(COMPILER) notebook.tex -pdf

clean:
	$(COMPILER) notebook.tex -C
	rm -fv src/*.aux
	rm -fv *.run.xml # biber
	rm -fv *.{aoc,lem,usc} # tocloft
