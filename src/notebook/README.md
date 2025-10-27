# Notebook code

The code is split into several packages as follows:

* The "core" part, aimed at conceptual code and having no external dependencies:

  * The [`math`](./math) package contains the code that verifies the algorithms and constructions of the monograph.

  * The [`parsing`](./parsing) package contains generic tools for creating a recursive descent parser. It is used extensively by the `math` package, as well as the following:
    * The [`bibtex`](./bibtex) package contains a Bib(La)TeX parser that is used by the `bibtools` subcommands.
    * The [`latex`](./latex) package contains a (La)TeX parser that is used by the `format-matrices` command.

  * The [`support`](./support) package contains helpers such as collections, strings, iteration. It is used by all other packages.

* The "auxiliary" part, aimed at various tools and thus being closer to "normal" code (in particular, having no restrictions on external dependencies).

  * The [`commands`](./commands) package contains several useful tools of various complexity.

  * The [`figures`](./figures) package contains figures that could not be reasonably drawn using LaTeX and/or Asymptote.
