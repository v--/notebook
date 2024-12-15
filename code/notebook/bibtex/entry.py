from collections.abc import Iterable, Sequence
from typing import Annotated, Literal, NamedTuple, get_args, get_type_hints

from ..support.iteration import list_accumulator, string_accumulator
from .author import BibAuthor
from .escaping import escape
from .string import BibString


TAB_SIZE = 2


BibEntryType = Literal[
    'article',
    'book',
    'booklet',
    'collection',
    'conference',
    'inbook',
    'incollection',
    'inproceedings',
    'manual',
    'mastersthesis',
    'misc',
    'online',
    'phdthesis',
    'proceedings',
    'report',
    'techreport',
    'thesis',
    'unpublished',
]


class BibFieldAnnotation(NamedTuple):
    meta: bool = False
    author: bool = False
    verbatim: bool = False
    list: bool = False
    key_name: str | None = None


class BibEntry(NamedTuple):
    """Customized biblatex entry specific for the citations in this monograph.
    Includes almost all fields from https://www.bibtex.com/format/fields/ (except type, annote and organization), but also a lot of other fields.
    """
    entry_type:    Annotated[BibEntryType, BibFieldAnnotation(meta=True)]
    entry_name:    Annotated[str, BibFieldAnnotation(meta=True)]
    # Base fields
    title:         Annotated[BibString, BibFieldAnnotation()]
    # Optional
    authors:       Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='author')] = []
    editors:       Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='editor')] = []
    translators:   Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='translator')] = []
    languages:     Annotated[Sequence[BibString], BibFieldAnnotation(list=True, key_name='language')] = []
    origlanguages: Annotated[Sequence[BibString], BibFieldAnnotation(list=True, key_name='origlanguage')] = []
    options:       Annotated[BibString | None, BibFieldAnnotation()] = None
    related:       Annotated[BibString | None, BibFieldAnnotation()] = None
    relatedtype:   Annotated[BibString | None, BibFieldAnnotation()] = None
    publisher:     Annotated[BibString | None, BibFieldAnnotation()] = None
    pubstate:      Annotated[BibString | None, BibFieldAnnotation()] = None
    titleaddon:    Annotated[BibString | None, BibFieldAnnotation()] = None
    subtitle:      Annotated[BibString | None, BibFieldAnnotation()] = None
    subtitleaddon: Annotated[BibString | None, BibFieldAnnotation()] = None
    date:          Annotated[BibString | None, BibFieldAnnotation()] = None
    url:           Annotated[BibString | None, BibFieldAnnotation(verbatim=True)] = None
    note:          Annotated[BibString | None, BibFieldAnnotation()] = None
    year:          Annotated[BibString | None, BibFieldAnnotation()] = None
    month:         Annotated[BibString | None, BibFieldAnnotation()] = None
    day:           Annotated[BibString | None, BibFieldAnnotation()] = None
    edition:       Annotated[BibString | None, BibFieldAnnotation()] = None
    volume:        Annotated[BibString | None, BibFieldAnnotation()] = None
    version:       Annotated[BibString | None, BibFieldAnnotation()] = None
    institution:   Annotated[BibString | None, BibFieldAnnotation()] = None
    # Theses
    advisors:      Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='advisor')] = []
    # Books
    chapter:       Annotated[BibString | None, BibFieldAnnotation()] = None
    series:        Annotated[BibString | None, BibFieldAnnotation()] = None
    isbn:          Annotated[BibString | None, BibFieldAnnotation()] = None
    part:          Annotated[BibString | None, BibFieldAnnotation()] = None
    # Book (and proceeding) chapters
    booktitle:     Annotated[BibString | None, BibFieldAnnotation()] = None
    booksubtitle:  Annotated[BibString | None, BibFieldAnnotation()] = None
    # Articles
    issue:         Annotated[BibString | None, BibFieldAnnotation()] = None
    issuetitle:    Annotated[BibString | None, BibFieldAnnotation()] = None
    journal:       Annotated[BibString | None, BibFieldAnnotation()] = None
    number:        Annotated[BibString | None, BibFieldAnnotation()] = None
    pages:         Annotated[BibString | None, BibFieldAnnotation()] = None
    issn:          Annotated[BibString | None, BibFieldAnnotation()] = None
    # Reports and manuals
    type:          Annotated[BibString | None, BibFieldAnnotation()] = None
    # References
    doi:           Annotated[BibString | None, BibFieldAnnotation()] = None
    eudml:         Annotated[BibString | None, BibFieldAnnotation()] = None
    gutenberg:     Annotated[BibString | None, BibFieldAnnotation()] = None
    jstor:         Annotated[BibString | None, BibFieldAnnotation()] = None
    handle:        Annotated[BibString | None, BibFieldAnnotation()] = None
    mathnet:       Annotated[BibString | None, BibFieldAnnotation()] = None
    mathscinet:    Annotated[BibString | None, BibFieldAnnotation()] = None
    numdam:        Annotated[BibString | None, BibFieldAnnotation()] = None
    scopus:        Annotated[BibString | None, BibFieldAnnotation()] = None
    zbmath:        Annotated[BibString | None, BibFieldAnnotation()] = None
    # eprints
    eprinttype:    Annotated[BibString | None, BibFieldAnnotation()] = None
    eprintclass:   Annotated[BibString | None, BibFieldAnnotation()] = None
    eprint:        Annotated[BibString | None, BibFieldAnnotation()] = None
    # Online
    howpublished:  Annotated[BibString | None, BibFieldAnnotation()] = None
    urldate:       Annotated[BibString | None, BibFieldAnnotation()] = None

    @classmethod
    @list_accumulator
    def get_meta_fields(cls) -> Iterable[str]:
        for field_name, field_annotation in get_type_hints(cls, include_extras=True).items():
            _, annotation = get_args(field_annotation)

            if annotation.meta:
                yield field_name

    @classmethod
    @list_accumulator
    def get_list_fields(cls) -> Iterable[tuple[str, str]]:
        for field_name, field_annotation in get_type_hints(cls, include_extras=True).items():
            _, annotation = get_args(field_annotation)

            if annotation.list or annotation.author:
                yield field_name, annotation.key_name or field_name

    @classmethod
    @list_accumulator
    def get_author_fields(cls) -> Iterable[tuple[str, str, str]]:
        for field_name, field_annotation in get_type_hints(cls, include_extras=True).items():
            _, annotation = get_args(field_annotation)

            if annotation.author:
                yield field_name, annotation.key_name or field_name, f'short{annotation.key_name or field_name}'

    @classmethod
    def is_known_key(cls, key: str) -> bool:
        for field_name, field_annotation in get_type_hints(cls, include_extras=True).items():
            _, annotation = get_args(field_annotation)

            if not annotation.meta:
                field_key = annotation.key_name or field_name

                if key == field_key or (annotation.author and key == f'short{field_key}'):
                    return True

        return False

    @classmethod
    def is_key_value_verbatim(cls, key: str) -> bool:
        for field_name, field_annotation in get_type_hints(cls, include_extras=True).items():
            _, annotation = get_args(field_annotation)

            if key == (annotation.key_name or field_name):
                return annotation.verbatim

        return False

    def _string_properties(self) -> dict[str, BibString]:
        properties = self._asdict()

        for field_name in self.get_meta_fields():
            properties.pop(field_name)

        for key, value in list(properties.items()):
            if value is None or value is False:
                properties.pop(key)

        for field_name, key_name, short_key_name in self.get_author_fields():
            authors = properties.pop(field_name)

            if len(authors) == 0:
                continue

            properties[key_name] = ' and '.join(str(author.full_name) for author in authors)

            if all(author.short_name for author in authors):
                properties[short_key_name] = ' and '.join(str(author.short_name) for author in authors)

        for field_name, key_name in self.get_list_fields():
            list_field = properties.pop(field_name, [])

            if len(list_field) == 0:
                continue

            properties[key_name] = ' and '.join(map(str, list_field))

        return properties

    @string_accumulator('')
    def __str__(self) -> Iterable[str]:  # noqa: PLE0307
        properties = self._string_properties()
        total = len(properties)

        yield f'@{self.entry_type}{{{self.entry_name},\n'

        for i, (key, value) in enumerate(sorted(properties.items(), key=lambda x: x[0])):
            yield ' ' * TAB_SIZE
            yield key
            yield ' = '

            if self.is_key_value_verbatim(key):
                yield '{' + str(value) + '}'
            else:
                yield '{' + escape(value) + '}'

            if i + 1 < total:
                yield ','

            yield '\n'

        yield '}\n'
