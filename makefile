COMPILER := latexmk -cd -interaction=nonstopmode -bibtex

.PHONY: clean

index.pdf: index.tex bib/*.bib packages/*.sty src/*.tex
	$(COMPILER) index.tex -pdf

clean:
	$(COMPILER) index.tex -C
	rm -fv src/*.aux
	rm -fv *.run.xml # biber
	rm -fv *.{aoc,lem,usc} # tocloft
