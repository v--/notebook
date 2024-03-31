# Notebook

<!-- __Note__: The corresponding PDF, kept up-to-date, can be found [here](https://ivasilev.net/files/Notebook.pdf). -->

## Introduction

This ever-expanding document started as a set of study notes and exercises and gradually outgrew itself to become more encyclopedic. Having all these notes in one place is quite helpful for both expressing my own thoughts clearly and for later reference. It is also helpful for tracking connections between seemingly unrelated concepts --- the entire monograph is hyperlinked. Even though I aim at understanding every concept in the way it is meant to be used, most concepts are presented insomuch as they are relevant to my previous experience.

Since these are study notes, they will naturally have a lot of errors, so read them with caution. The document claims no referential nor pedagogical value. Everything is written at the level of abstraction I am comfortable with. Furthermore, some sections in the monograph are much more polished than others. Feel free to [contact me](https://ivasilev.net) if something in this monograph happens to distress you.

I tried putting citations on as many things as possible. The citations themselves are usually put in the left margin. If there is no citation on a definition or theorem, that means that I have either recalled it from memory or discovered it on my own. I try to mark my own definitions to distinguish them from one taken from other sources. Many of the unoriginal definitions and theorems are restated. The simple proofs are mostly original, and the difficult ones are, often loosely, based on proofs from the places cited. Some proofs simply state "Trivial." in order to distinguish themselves from the proofs that are omitted for other reasons.

Last but not least, some auxiliary programs are provided in the [code/](https://github.com/v--/notebook/tree/master/code) subdirectory within the monograph's source.

See the remarks in the introduction of the sections on mathematical logic and set theory for clarification regarding seemingly arbitrary conventions.

## License

This is a [public domain](https://en.wikipedia.org/wiki/Public_domain) project: it uses [CC0](https://spdx.org/licenses/CC0-1.0.html) for the text itself and the [Unlicense](https://spdx.org/licenses/Unlicense.html) for the Python code.

## Project structure

While I have put in a lot of effort into the project structure itself, I believe that, because of the nature of the project, it makes little sense to document it extensively. There is a GNU Make file specifying how to build the document. There are also several custom tools that can be found in the `code/commands` subdirectory - they are most easily activated via [poe](https://poethepoet.natn.io) (`poe --root code <command>`).

If you happen to be interested in any aspect of the setup, feel free to [contact me](https://ivasilev.net).
