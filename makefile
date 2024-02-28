COMPILER := pdflatex -interaction=batchmode
FIGURES_TEX_PDF := $(patsubst figures/%.tex,output/%.pdf,$(wildcard figures/*.tex))
FIGURES_ASY_PDF := $(patsubst figures/%.asy,output/%.eps,$(wildcard figures/*.asy))
TEXT_SOURCE := notebook.tex classes/notebook.cls bibliography/*.bib packages/*.sty text/*.tex $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF)

.PHONY: notebook figures watch watch-figures format-figures find-obsolete-figures tidy-bib-files clean checkcites

notebook: output/notebook.pdf

aux:
	mkdir --parents aux

output:
	mkdir --parents output

output/notebook.pdf: $(TEXT_SOURCE) | aux output
	$(COMPILER) -output-directory=aux -draftmode notebook.tex
	biber --quiet aux/notebook.bcf
	$(COMPILER) -output-directory=aux -draftmode notebook.tex
	$(COMPILER) -output-directory=aux notebook.tex
	cat aux/notebook.pdf > output/notebook.pdf

output/%.pdf: classes/tikzcd.cls packages/*.sty figures/%.tex | aux output
	$(COMPILER) -output-directory=aux figures/$*.tex
	cat aux/$*.pdf > output/$*.pdf

output/%.eps: figures/%.asy | aux output
	asy -quiet -render=5 -outname=aux/$* figures/$*.asy
	cat aux/$*.eps > output/$*.eps

figures: $(FIGURES_TEX_PDF) $(FIGURES_ASY_PDF)

format-figures:
	@poetry --directory code run python -m code.commands.format_matrices figures/*.tex

find-obsolete-figures:
	@poetry --directory code run python -m code.commands.find_obsolete_figures

tidy-bib-files:
	@poetry --directory code run python -m code.commands.tidy_bib_files

checkcites:
	@checkcites --backend biber --all aux/notebook.bcf

# I have implemented a very useful build system for LaTeX with log processing and debouncing
watch: | aux output
	@poetry --directory code run python -m code.commands.watcher all

watch-figures: | aux output
	@poetry --directory code run python -m code.commands.watcher figures

git-commit-info: .git/refs/heads/master
	LC_ALL=en_US.UTF-8 git log --max-count 1 --format=format:'hash={%h},date={%cd}' --date='format:%d %B %Y' HEAD > git-commit-info

clean:
	rm --recursive --force aux output
