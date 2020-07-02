COMPILER := latexmk -cd -interaction=nonstopmode -bibtex

.PHONY: clean

index.pdf: index.tex references.bib packages/*.sty src/*.tex
	$(COMPILER) index.tex -pdf

clean:
	$(COMPILER) index.tex -C
	rm -fv *.run.xml # biber
