COMPILER := latexmk -cd -interaction=nonstopmode -bibtex

.PHONY: clean

src/index.pdf: src/*.tex src/references.bib src/common/*.sty
	${COMPILER} src/index.tex -pdf

clean:
	${COMPILER} src/index.tex -C
	rm -fv src/*.run.xml # biber
