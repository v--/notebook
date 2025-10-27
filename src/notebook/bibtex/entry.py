from collections.abc import Collection, Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from typing import Annotated, Literal, get_args, get_type_hints

from ..support.iteration import string_accumulator
from .author import BibAuthor
from .escaping import escape
from .string import BibString


TAB_SIZE = 2


BibEntryType = Literal[
    'article',
    'book',
    'bookinbook',
    'booklet',
    'collection',
    'conference',
    'inbook',
    'incollection',
    'inproceedings',
    'manual',
    'mastersthesis',
    'misc',
    'mvbook',
    'mvcollection',
    'online',
    'phdthesis',
    'proceedings',
    'report',
    'techreport',
    'thesis',
    'unpublished'
]


ENTRY_TYPE_LIST: Sequence[BibEntryType] = get_args(BibEntryType)


@dataclass(frozen=True)
class BibFieldAnnotation:
    meta: bool = False
    author: bool = False
    verbatim: bool = False
    list: bool = False
    key_name: str | None = None


@dataclass()
class BibEntry:
    """Customized biblatex entry specific for the citations in this monograph.
    Includes almost all fields from https://www.bibtex.com/format/fields/ (except type, annote and organization), but also a lot of other fields.
    """
    entry_type:    Annotated[BibEntryType, BibFieldAnnotation(meta=True)]
    entry_name:    Annotated[str, BibFieldAnnotation(meta=True)]
    # Base fields
    title:         Annotated[BibString, BibFieldAnnotation()]
    # Optional
    authors:       Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='author')] = field(default_factory=list)
    editors:       Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='editor')] = field(default_factory=list)
    compilers:     Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='compiler')] = field(default_factory=list)
    translators:   Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='translator')] = field(default_factory=list)
    annotators:    Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='annotator')] = field(default_factory=list)
    foreword:      Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True)] = field(default_factory=list)
    languages:     Annotated[Sequence[BibString], BibFieldAnnotation(list=True, key_name='language')] = field(default_factory=list)
    origlanguages: Annotated[Sequence[BibString], BibFieldAnnotation(list=True, key_name='origlanguage')] = field(default_factory=list)
    options:       Annotated[BibString | None, BibFieldAnnotation()] = None
    related:       Annotated[BibString | None, BibFieldAnnotation()] = None
    relatedtype:   Annotated[BibString | None, BibFieldAnnotation()] = None
    crossref:      Annotated[BibString | None, BibFieldAnnotation()] = None
    publisher:     Annotated[BibString | None, BibFieldAnnotation()] = None
    pubstate:      Annotated[BibString | None, BibFieldAnnotation()] = None
    titleaddon:    Annotated[BibString | None, BibFieldAnnotation()] = None
    subtitle:      Annotated[BibString | None, BibFieldAnnotation()] = None
    subtitleaddon: Annotated[BibString | None, BibFieldAnnotation()] = None
    origdate:      Annotated[BibString | None, BibFieldAnnotation()] = None
    origpublisher: Annotated[BibString | None, BibFieldAnnotation()] = None
    origtitle:     Annotated[BibString | None, BibFieldAnnotation()] = None
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
    addendum:      Annotated[BibString | None, BibFieldAnnotation()] = None
    # Theses
    advisors:      Annotated[Sequence[BibAuthor], BibFieldAnnotation(author=True, key_name='advisor')] = field(default_factory=list)
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
    jstor:         Annotated[BibString | None, BibFieldAnnotation()] = None
    handle:        Annotated[BibString | None, BibFieldAnnotation()] = None
    mathnet:       Annotated[BibString | None, BibFieldAnnotation()] = None
    mathscinet:    Annotated[BibString | None, BibFieldAnnotation()] = None
    numdam:        Annotated[BibString | None, BibFieldAnnotation()] = None
    scopus:        Annotated[BibString | None, BibFieldAnnotation()] = None
    ssrn  :        Annotated[BibString | None, BibFieldAnnotation()] = None
    zbmath:        Annotated[BibString | None, BibFieldAnnotation()] = None
    # eprints
    eprinttype:    Annotated[BibString | None, BibFieldAnnotation()] = None
    eprintclass:   Annotated[BibString | None, BibFieldAnnotation()] = None
    eprint:        Annotated[BibString | None, BibFieldAnnotation()] = None
    # Online
    howpublished:  Annotated[BibString | None, BibFieldAnnotation()] = None
    urldate:       Annotated[BibString | None, BibFieldAnnotation()] = None

    # Based on https://stackoverflow.com/a/77690186/2756776
    def __or__(self, other: 'BibEntry') -> 'BibEntry':
        return BibEntry(**asdict(self) | asdict(other))

    def _string_properties(self) -> Iterable[tuple[str, BibString]]:
        for key in sorted(ENTRY_KEYS.known):
            if key in ENTRY_KEYS.meta:
                continue

            value = getattr(self, ENTRY_KEYS.field_name_map[key])

            if key in ENTRY_KEYS.author:
                if key.startswith('short'):
                    author_string = ' and '.join(str(author.short_name) for author in value if author.short_name)

                    if author_string:
                        yield key, author_string
                elif len(value) > 0:
                    yield key, ' and '.join(str(author.full_name) for author in value)
            elif isinstance(value, list):
                if len(value) > 0:
                    yield key, ' and '.join(value)
            elif value is not None:
                yield key, value

    @string_accumulator('')
    def __str__(self) -> Iterable[str]:  # noqa: PLE0307
        properties = dict(self._string_properties())
        total = len(properties)

        yield f'@{self.entry_type}{{{self.entry_name},\n'

        for i, (key, value) in enumerate(properties.items()):
            yield ' ' * TAB_SIZE
            yield key
            yield ' = '

            if key in ENTRY_KEYS.verbatim:
                yield '{' + str(value) + '}'
            else:
                yield '{' + escape(value) + '}'

            if i + 1 < total:
                yield ','

            yield '\n'

        yield '}\n'



@dataclass(frozen=True)
class KeyConfiguration:
    field_name_map: Mapping[str, str]
    known: Collection[str]
    meta: Collection[str]
    list: Collection[str]
    author: Collection[str]
    verbatim: Collection[str]


def infer_key_configuration(cls: type) -> KeyConfiguration:
    field_name_map = dict[str, str]()
    known_keys = set[str]()
    meta_keys = set[str]()
    list_keys = set[str]()
    author_keys = set[str]()
    verbatim_keys = set[str]()

    for field_key, field_annotation in get_type_hints(cls, include_extras=True).items():
        _, annotation = get_args(field_annotation)

        if not isinstance(annotation, BibFieldAnnotation):
            continue

        bib_key = annotation.key_name or field_key
        known_keys.add(bib_key)
        field_name_map[bib_key] = field_key

        if annotation.author:
            author_keys.add(bib_key)
            list_keys.add(bib_key)

            short_key = f'short{bib_key}'
            field_name_map[short_key] = field_key
            known_keys.add(short_key)
            author_keys.add(short_key)
            list_keys.add(short_key)

        if annotation.meta:
            meta_keys.add(bib_key)

        if annotation.list:
            list_keys.add(bib_key)

        if annotation.verbatim:
            verbatim_keys.add(bib_key)

    return KeyConfiguration(field_name_map, known_keys, meta_keys, list_keys, author_keys, verbatim_keys)


ENTRY_KEYS = infer_key_configuration(BibEntry)
