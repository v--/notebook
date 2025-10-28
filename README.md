# Notebook

<!-- __Note__: The corresponding PDF, kept up-to-date, can be found [here](https://ivasilev.net/files/Notebook.pdf). -->

## Introduction

This ever-expanding monograph started as a set of study notes and exercises and gradually outgrew itself to become more encyclopedic. Having all these notes in one place is quite helpful for both expressing my own thoughts clearly and for later reference. It is also helpful for tracking connections between seemingly unrelated concepts --- the entire monograph is hyperlinked. Even though I aim at understanding every concept in the way it is meant to be used, most concepts are presented insomuch as they are relevant to my previous experience.

Most of the document contains concepts that are new to me at the time of writing, and thus it is naturally rough around the edges. There are a lot of errors, both insignificant and substantial, so read with caution. The document claims no referential nor pedagogical value. Everything is written at the level of abstraction I am comfortable with. Furthermore, some sections in the monograph are much more polished than others. Feel free to [contact me](https://ivasilev.net) if something in this monograph happens to distress you.

I tried putting citations on as many things as possible. The citations themselves are usually put in the left margin. If there is no citation on a definition or theorem, that means that I have either recalled it from memory or discovered it on my own. I try to mark my own definitions to distinguish them from one taken from other sources. Many of the unoriginal definitions and theorems are restated. The simple proofs are mostly original, and the difficult ones are, often loosely, based on proofs from the places cited.

Last but not least, some auxiliary programs are provided in the [`src`](https://github.com/v--/notebook/tree/master/src) subdirectory within the monograph's source. Staying close to the monograph exposition is a priority over performance or code quality considerations.

Even though the document starts by building the familiar number systems, from a formalist perspective, it should start at the chapter for mathematical logic.

## License

This is a [public domain](https://en.wikipedia.org/wiki/Public_domain) project: it uses [CC0](https://spdx.org/licenses/CC0-1.0.html) for the text itself and the [Unlicense](https://spdx.org/licenses/Unlicense.html) for the Python code.

## Project structure

While I have put in a lot of effort into the project structure itself, I believe that, because of the nature of the project, it makes little sense to document it extensively. There is a GNU Make file specifying how to build the document. There are also several custom tools that can be found in the [`src/notebook/commands`](./src/notebook/commands) subdirectory - they are most easily activated via [poe](https://poethepoet.natn.io) (`poe <command>`).

See the README at [`src/notebook`](./src/notebook) for an overview of how the code is structured.

If you happen to be interested in any aspect of the setup, feel free to [contact me](https://ivasilev.net).

### Build system

There are two build systems --- the [`Makefile`](./Makefile) and the [`notebook.commands.watcher`](./src/notebook/commands/watcher) (Usage: `poe watcher [--no-aux]`) command. The first one is aimed at full builds, i.e. for continuous integration, while the second one is aimed at incremental builds, i.e. for development.

There are externalized figures in the [`figures`](./figures) directory of the following kinds:
* [Asymptote](https://github.com/vectorgraphics/asymptote) (`.asy`) files for 2D and 3D sketches and plots, as well as (graph-theoretic) graphs. `xvfb` is used by default for 3D rendering (freeglut doesn't work on headless environments nor on Wayland).
* [tikz-cd](https://ctan.org/pkg/tikz-cd) (`.tex` with document class `classes/tikzcd`) files for commutative and Hasse diagrams and automata.
* [forest](https://ctan.org/pkg/forest) (`.tex` with document class `classes/forest`) files for trees.

### Parsers

A lot of the monograph-related code, as well as some of the tools are based on a recursive descent [parser framework](./src/notebook/parsing) created specifically for various (micro)languages in the monograph:
* [Formal grammar schemas](./src/notebook/math/grammars/parsing)
* [First-order logic terms and formulas and schemas](./src/notebook/math/logic/parsing)
* [Lambda calculus terms and schemas](./src/notebook/math/lambda/parsing)
* [Plain text](./src/notebook/math/nlp/parsing)

Two additional parsers are included:
* (Limited) [LaTeX](./src/notebook/latex/parsing)
* (Opinionated) [BibTeX](./src/notebook/bibtex/parsing)

### LaTeX tools

There is a tool, [`notebook.commands.format_matrices`](./src/notebook/commands/format_matrices) (Usage: `poe format-matrices figures/*.tex`), made specifically for formatting LaTeX arrays and similar environments.

### Bib(La)TeX tools

There is a set of tools, [`notebook.commands.bibtools`](./src/notebook/commands/bibtools) (Usage: `poe bibtools`), consisting of:
* A "formatter" (`... format bibliography bibliography/*.bib`) that handles name and ISBN/ISSN normalization, reference translation (e.g. DOI, mathnet, zbMATH and other URLs to fields) and other mundane tasks. It also emits warnings when it detects mistakes, e.g. an `@article` entry without a `journal` or an `@inbook` entry without a `booktitle`.

* Several BibLaTeX entry fetch tools:
  * `... fetch doi <id>`
  * `... fetch isbn <id>`
  * `... fetch arxiv <id>`.
  * `... fetch mathnet <id>`.

Some comments should be made about the parser. It was created specifically for maintaining my personal (digital) library and this monograph's sources in particular.
* The rules for entry fields are based on those of BibLaTeX with some additions (e.g. mathnet, zbMATH, jstor).
* The parser only allows the fields from the [`BibEntry`](./src/notebook/bibtex/entry.py) class. Because this tool was built upon years of maintaining references with other improvised tools, however, a lot of (standard and nonstandard) entry properties accumulated.
* The parser auxiliary logic for handling author names via the [`BibAuthor`](./src/notebook/bibtex/author.py) class. This involves parsing and handling each author separately (with `and` acting as a separator). For Cyrillic languages, Latin transliteration is enforced via the `BibAuthor.short` field that gets read and written to the `shortauthor` BibTeX field.
* The parser tries to unescape certain characters like `&` and `@`, while `BibEntry` tries to escape them when serializing. Exceptions for this are the fields marked as "verbatim" such as `url`.
* The parser also supports verbatim fields, i.e. fields with values enclosed in an additional pair of curly braces like `{{value}}` or `"{value}"`. The value inside does not get processed by the author processing mechanism, thus we can treat "corporate names" like `{{Springer Science and Business Media}}` as one.
