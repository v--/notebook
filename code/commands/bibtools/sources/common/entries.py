from notebook.bibtex.author import BibAuthor
from notebook.support.unicode import remove_accents, remove_symbols, remove_whitespace

from .keywords import extract_keyphrase


def mangle_string_for_entry_name(string: str) -> str:
    return remove_whitespace(remove_symbols(remove_accents(string).title()))


def generate_entry_name(author: BibAuthor, year: str, title: str, language: str, *aux_texts: str | None) -> str:
    keyphrase = extract_keyphrase(title, language, *(aux for aux in aux_texts if aux))
    mangled_keyphrase = mangle_string_for_entry_name(keyphrase)
    mangled_name = mangle_string_for_entry_name(author.main_name)
    return f'{mangled_name}{year}{mangled_keyphrase}'
