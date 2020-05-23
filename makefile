.PHONY: all

src/index.pdf: src/index.tex src/references.bib src/*/*/*.tex
	cd src && arara --verbose index.tex

clean:
	rm --force src/{index,*/*/*}.{aux,log,out,pdf,bbl,bcf,blg,nav,run.xml,snm,toc,vrb}
