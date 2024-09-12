from collections.abc import Iterable, Sequence
from typing import Annotated, Literal, NamedTuple, cast, get_args, get_type_hints

from ..support.iteration import list_accumulator, string_accumulator
from .author import BibAuthor
from .escaping import escape


TAB_SIZE = 2


BibEntryType = Literal[
    'article',
    'book',
    'booklet',
    'conference',
    'inbook',
    'incollection',
    'inproceedings',
    'manual',
    'mastersthesis',
    'misc',
    'phdthesis',
    'proceedings',
    'techreport',
    'unpublished',
    'online'
]


class BibFieldAnnotation(NamedTuple):
    meta: bool = False
    author: bool = False
    verbatim: bool = False
    key_name: str | None = None


class BibEntry(NamedTuple):
    """Customized biblatex entry specific for the citations in this monograph.
    Includes almost all fields from https://www.bibtex.com/format/fields/ (except type, annote and organization), but also a lot of other fields.
    """
    entry_type:    Annotated[BibEntryType, BibFieldAnnotation(meta=True)]
    entry_name:    Annotated[str, BibFieldAnnotation(meta=True)]
    # Base fields
    title:         Annotated[str, BibFieldAnnotation()]
    language:      Annotated[str, BibFieldAnnotation()]
    authors:       Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='author')]
    # Optional
    translators:   Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='translator')] = []
    editors:       Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='editor')] = []
    doi:           Annotated[str | None, BibFieldAnnotation()] = None
    publisher:     Annotated[str | None, BibFieldAnnotation()] = None
    subtitle:      Annotated[str | None, BibFieldAnnotation()] = None
    date:          Annotated[str | None, BibFieldAnnotation()] = None
    url:           Annotated[str | None, BibFieldAnnotation(verbatim=True)] = None
    note:          Annotated[str | None, BibFieldAnnotation()] = None
    year:          Annotated[str | None, BibFieldAnnotation()] = None
    month:         Annotated[str | None, BibFieldAnnotation()] = None
    day:           Annotated[str | None, BibFieldAnnotation()] = None
    edition:       Annotated[str | None, BibFieldAnnotation()] = None
    volume:        Annotated[str | None, BibFieldAnnotation()] = None
    institution:   Annotated[str | None, BibFieldAnnotation()] = None
    # Theses
    advisors:      Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='advisor')] = []
    # Books
    series:        Annotated[str | None, BibFieldAnnotation()] = None
    isbn:          Annotated[str | None, BibFieldAnnotation()] = None
    # Russian books
    udc:           Annotated[str | None, BibFieldAnnotation()] = None
    bbc:           Annotated[str | None, BibFieldAnnotation()] = None
    # Articles
    booktitle:     Annotated[str | None, BibFieldAnnotation()] = None
    issue:         Annotated[str | None, BibFieldAnnotation()] = None
    journal:       Annotated[str | None, BibFieldAnnotation()] = None
    mathnet:       Annotated[str | None, BibFieldAnnotation()] = None
    mathscinet:    Annotated[str | None, BibFieldAnnotation()] = None
    zmath:         Annotated[str | None, BibFieldAnnotation()] = None
    zbl:           Annotated[str | None, BibFieldAnnotation()] = None
    number:        Annotated[str | None, BibFieldAnnotation()] = None
    pages:         Annotated[str | None, BibFieldAnnotation()] = None
    issn:          Annotated[str | None, BibFieldAnnotation()] = None
    mrnumber:      Annotated[str | None, BibFieldAnnotation()] = None
    # HAL
    hal_id:        Annotated[str | None, BibFieldAnnotation()] = None
    hal_version:   Annotated[str | None, BibFieldAnnotation()] = None
    # arXiv
    archiveprefix: Annotated[str | None, BibFieldAnnotation()] = None
    primaryclass:  Annotated[str | None, BibFieldAnnotation()] = None
    eprint:        Annotated[str | None, BibFieldAnnotation()] = None
    # Online
    howpublished:  Annotated[str | None, BibFieldAnnotation()] = None
    urldate:       Annotated[str | None, BibFieldAnnotation()] = None

    @classmethod
    @list_accumulator
    def get_meta_fields(cls) -> Iterable[str]:
        for field_name, field_annotation in get_type_hints(cls, include_extras=True).items():
            _, annotation = get_args(field_annotation)

            if annotation.meta:
                yield field_name

    @classmethod
    @list_accumulator
    def get_author_fields(cls) -> Iterable[tuple[str, str]]:
        for field_name, field_annotation in get_type_hints(cls, include_extras=True).items():
            _, annotation = get_args(field_annotation)

            if annotation.author:
                yield field_name, annotation.key_name or field_name

    @classmethod
    def is_known_key(cls, key: str) -> bool:
        if key == 'shortauthor':
            return True

        for field_name, field_annotation in get_type_hints(cls, include_extras=True).items():
            _, annotation = get_args(field_annotation)

            if not annotation.meta and key == (annotation.key_name or field_name):
                return True

        return False

    @classmethod
    def is_key_value_verbatim(cls, key: str) -> bool:
        for field_name, field_annotation in get_type_hints(cls, include_extras=True).items():
            _, annotation = get_args(field_annotation)

            if key == (annotation.key_name or field_name):
                return annotation.verbatim

        return False

    def _string_properties(self) -> dict[str, str]:
        properties = self._asdict()

        for field_name in self.get_meta_fields():
            properties.pop(field_name)

        for key, value in list(properties.items()):
            if value is None:
                properties.pop(key)

        for field_name, key_name in self.get_author_fields():
            authors = properties.pop(field_name)

            if len(authors) > 0:
                properties[key_name] = ' and '.join(map(str, authors))

        if all(author.display_name for author in self.authors):
            properties['shortauthor'] = ' and '.join(cast(str, author.display_name) for author in self.authors)

        return properties

    @string_accumulator('')
    def __str__(self) -> Iterable[str]:  # noqa: PLE0307
        properties = self._string_properties()
        total = len(properties)

        yield f'@{self.entry_type}{{{self.entry_name},\n'

        for i, (key, value) in enumerate(sorted(properties.items(), key=lambda x: x[0])):
            yield ' ' * TAB_SIZE
            yield key
            yield ' = {'

            if self.is_key_value_verbatim(key):
                yield value
            else:
                yield escape(value)

            yield '}'

            if i + 1 < total:
                yield ','

            yield '\n'

        yield '}\n'
