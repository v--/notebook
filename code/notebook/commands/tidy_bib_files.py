import pathlib

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from titlecase import titlecase


BIB_PATH = pathlib.Path('bibliography').resolve()


# Simplified transliteration based on
# https://www.mid.ru/ru/activity/legislation_documents/reglaments/1441771/
CYR_TO_LAT_TABLE = str.maketrans({
    'a': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': 'a',  # This is supposed to be "ie", but "a" is more appropriate for Bulgarian and "ъ" is rarely used in Russian names
    'ы': 'y',
    'ь': None,
    'э': 'e',
    'ю': 'iu',
    'я': 'ya',  # This is supposed to be "ia", but "ya" is more widely accepted
    # Custom
    'і': 'i'
})


def refine_bib_files():
    for bib_file_path in BIB_PATH.iterdir():
        parser = BibTexParser(ignore_nonstandard_types=False)

        with open(bib_file_path, 'r') as file:
            bibtex_db = bibtexparser.load(file, parser)

        bibtex_db.entries = sorted(
            bibtex_db.entries,
            key=lambda entry: entry['ID']
        )

        for entry in bibtex_db.entries:
            if entry['ENTRYTYPE'] != 'online':
                for field in ['title', 'subtitle']:
                    if field not in entry:
                        continue

                    title_cased = titlecase(entry[field], callback=lambda string, **kwargs: string if not string.isascii() else None)

                    if title_cased:
                        entry[field] = title_cased

            if 'shortauthor' in entry:
                continue

            if entry['language'] == 'russian' or entry['language'] == 'bulgarian':
                entry['shortauthor'] = ' and '.join(
                    author
                        .lower()
                        .replace('ий', 'iy')
                        .replace('ей', 'еy')
                        .translate(CYR_TO_LAT_TABLE)
                        .title()

                    for author in entry['author'].split(' and ')
                )

        writer = BibTexWriter()
        writer.indent = '  '

        with open(bib_file_path, 'w') as file:
            file.write(writer.write(bibtex_db))



if __name__ == '__main__':
    refine_bib_files()
