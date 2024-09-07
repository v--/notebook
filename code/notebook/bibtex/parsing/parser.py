from collections import deque
from collections.abc import Iterable, Sequence
from typing import NamedTuple, cast, get_args

from ...parsing.mixins.whitespace import WhitespaceParserMixin
from ...parsing.parser import Parser
from ...parsing.whitespace import Whitespace
from ...support.iteration import list_accumulator
from ..entry import BibAuthor, BibEntry, BibEntryType, BibLanguage
from .tokenizer import tokenize_bibtex
from .tokens import BibToken, CommentToken, MiscToken, NumberToken, WordToken


AUTHOR_KEYS = {key_name for _, key_name in BibEntry.get_author_fields()} | {'shortauthor'}


class PropertyValue(NamedTuple):
    segments: Sequence[str]

    def __str__(self) -> str:
        return ''.join(self.segments)


class PropertyValueBuilder:
    segments: list[str]
    buffer: str

    def __init__(self) -> None:
        self.segments = []
        self.buffer = ''

    def append(self, string: str) -> None:
        self.buffer += string

    def flush(self) -> None:
        if len(self.buffer) > 0:
            self.segments.append(self.buffer)
            self.buffer = ''

    def get_value(self) -> PropertyValue:
        return PropertyValue(self.segments)


class BibParser(WhitespaceParserMixin[BibToken], Parser[BibToken]):
    def skip_whitespace_and_comments(self) -> None:
        self.gobble_and_skip(lambda token: isinstance(token, Whitespace | CommentToken))

    def parse_entry_type(self) -> BibEntryType:
        start_i = self.index
        entry_type = self.gobble_string(lambda token: isinstance(token, WordToken))

        if len(entry_type) == 0:
            raise self.error('Expected an entry type')

        if entry_type not in get_args(BibEntryType):
            raise self.error('Unrecognized entry type', i_first_token=start_i, i_last_token=self.index - 1)

        return cast(BibEntryType, entry_type)

    def parse_entry_name(self, existing: set[str]) -> str:
        start_i = self.index

        # Entry names may even contain %, which is otherwise used for comments
        entry_name = self.gobble_string(lambda token: token != MiscToken.closing_brace and token != MiscToken.comma and token != Whitespace.line_break)

        if len(entry_name) == 0:
            raise self.error('Expected an entry name', i_last_token=self.index - 1)

        if entry_name in existing:
            raise self.error('Duplicate entry name', i_first_token=start_i, i_last_token=self.index - 1)

        return entry_name

    def parse_property_key(self) -> str:
        key = self.gobble_string(lambda token: isinstance(token, WordToken | NumberToken) or token == MiscToken.underscore)

        if len(key) == 0:
            raise self.error('Expected an entry key')

        return key

    def parse_braced_value(self, entry_start_i: int, value_start_i: int) -> PropertyValue:  # noqa: PLR0912
        assert self.peek() == MiscToken.opening_brace
        self.advance()

        builder = PropertyValueBuilder()
        verbatim = False

        while not self.is_at_end():
            match head := self.peek():
                case CommentToken():
                    raise self.error('Unexpected comment')

                case MiscToken.closing_brace:
                    if verbatim:
                        builder.append('}')
                        builder.flush()
                        verbatim = False
                        self.advance()
                    else:
                        builder.flush()
                        self.advance()
                        return builder.get_value()

                case MiscToken.opening_brace:
                    builder.flush()
                    builder.append('{')
                    verbatim = True
                    self.advance()

                case MiscToken.backslash:
                    lookahead = self.peek_multiple(2)

                    match lookahead:
                        case [MiscToken.backslash]:
                            raise self.error('Invalid escaped symbol')

                        case [MiscToken.backslash, MiscToken.opening_brace]:
                            builder.append('{')
                            self.advance(2)

                        case [MiscToken.backslash, MiscToken.closing_brace]:
                            builder.append('}')
                            self.advance(2)

                        case _:
                            builder.append(str(head))
                            self.advance()

                case WordToken('and') | WordToken('AND'):
                    if verbatim:
                        builder.append(str(head))
                    else:
                        builder.flush()
                        builder.append(str(head))
                        builder.flush()

                    self.advance()

                case _:
                    builder.append(str(head))
                    self.advance()

        raise self.error('Unclosed brace', i_first_token=value_start_i, i_first_visible_token=entry_start_i)

    def parse_quoted_value(self, entry_start_i: int, value_start_i: int) -> PropertyValue:  # noqa: PLR0912
        assert self.peek() == MiscToken.quotes
        self.advance()

        builder = PropertyValueBuilder()
        verbatim = False

        while not self.is_at_end():
            match head := self.peek():
                case CommentToken():
                    raise self.error('Unexpected comment')

                case MiscToken.quotes:
                    builder.flush()
                    self.advance()
                    return builder.get_value()

                case MiscToken.closing_brace:
                    builder.append('}')

                    if verbatim:
                        builder.flush()
                        verbatim = False
                    else:
                        builder.append('}')
                        self.advance()

                    self.advance()

                case MiscToken.opening_brace:
                    lookahead = self.peek_multiple(3)

                    if lookahead == [MiscToken.opening_brace, MiscToken.quotes, MiscToken.closing_brace]:
                        builder.append('"')
                        self.advance(3)
                    else:
                        verbatim = True
                        builder.flush()
                        builder.append(str(head))
                        self.advance()

                case WordToken('and') | WordToken('AND'):
                    if verbatim:
                        builder.append(str(head))
                    else:
                        builder.flush()
                        builder.append(str(head))
                        builder.flush()

                    self.advance()

                case _:
                    builder.append(str(head))
                    self.advance()

        raise self.error('Unclosed brace', i_first_token=value_start_i, i_first_visible_token=entry_start_i)

    def parse_author_string(self, string: str, entry_start_i: int, value_start_i: int) -> BibAuthor:
        if string.startswith('{') and string.endswith('}'):
            return BibAuthor(main_name=string)

        parts = [part.strip() for part in string.split(',')]

        error_kwargs = dict(
            i_first_token=value_start_i,
            i_last_token=self.index - 1,
            i_first_visible_token=entry_start_i
        )

        for part in parts:
            if len(part) == 0:
                raise self.error('Cannot parse author string', **error_kwargs)

        match parts:
            case [main_name]:
                return BibAuthor(main_name=main_name)
            case [main_name, other_names]:
                return BibAuthor(main_name=main_name, other_names=other_names)
            case [main_name, title, other_names]:
                return BibAuthor(main_name=main_name, other_names=other_names, title=title)
            case _:
                raise self.error('Cannot parse author string', **error_kwargs)

    def parse_authors(self, value: PropertyValue, entry_start_i: int, value_start_i: int) -> Iterable[BibAuthor]:
        expecting_and = False

        error_kwargs = dict(
            i_first_token=value_start_i,
            i_last_token=self.index - 1,
            i_first_visible_token=entry_start_i
        )

        for segment in value.segments:
            if segment == 'and' or segment == 'AND':
                if expecting_and:
                    expecting_and = False
                    continue
                else:
                    raise self.error('Cannot parse author string', **error_kwargs)

            if segment.isspace():
                continue

            if expecting_and:
                raise self.error('Cannot parse author string', **error_kwargs)

            yield self.parse_author_string(
                segment,
                entry_start_i=entry_start_i,
                value_start_i=value_start_i
            )

            expecting_and = True

    def perform_inline_validation(self, key: str, value: PropertyValue, entry_start_i: int, value_start_i: int) -> None:
        error_kwargs = dict(
            i_first_token=value_start_i,
            i_last_token=self.index - 1,
            i_first_visible_token=entry_start_i
        )

        value_str = str(value)

        if len(value_str) == 0 or value_str.isspace():
            raise self.error('Empty value', **error_kwargs)

        if key in AUTHOR_KEYS:
            for _ in self.parse_authors(value, entry_start_i, value_start_i):
                pass

        if key == 'language' and value_str not in get_args(BibLanguage):
            raise self.error('Unrecognized language', **error_kwargs)

        if key == 'isbn':
            no_dashes = value_str.replace('-', '')

            if (len(no_dashes) == 10 or len(no_dashes) == 13) and no_dashes[:-1].isdigit() and (no_dashes[-1].isdigit() or no_dashes[-1] == 'X'):
                return

            raise self.error('Invalid ISBN', **error_kwargs)

        if key == 'issn':
            no_dashes = value_str.replace('-', '')

            if len(no_dashes) == 8 and no_dashes[:-1].isdigit() and (no_dashes[-1].isdigit() or no_dashes[-1] == 'X'):
                return

            raise self.error('Invalid ISSN', **error_kwargs)

    def parse_entry_properties(self, entry_start_i: int) -> Iterable[tuple[str, PropertyValue]]:
        keys = set[str]()

        while not self.is_at_end() and self.peek() != MiscToken.closing_brace:
            key_start_i = self.index
            key = self.parse_property_key()

            if key in keys:
                raise self.error('Duplicate key', i_first_token=key_start_i, i_first_visible_token=entry_start_i, i_last_token=self.index - 1)

            if key != 'shortauthor' and not BibEntry.is_known_key(key):
                raise self.error('Unrecognized key', i_first_token=key_start_i, i_first_visible_token=entry_start_i, i_last_token=self.index - 1)

            keys.add(key)

            self.skip_spaces()

            if self.peek() != MiscToken.equals:
                raise self.error('Expected an equality sign', i_first_visible_token=entry_start_i)

            self.advance()
            self.skip_spaces()

            value_start_i = self.index
            value: PropertyValue

            match head := self.peek():
                case NumberToken():
                    value = PropertyValue([str(head)])
                    self.advance()

                case MiscToken.opening_brace:
                    value = self.parse_braced_value(entry_start_i, value_start_i)

                case MiscToken.quotes:
                    value = self.parse_quoted_value(entry_start_i, value_start_i)

                case _:
                    raise self.error('Invalid entry value', i_first_visible_token=entry_start_i)

            self.perform_inline_validation(key, value, entry_start_i, value_start_i)
            yield key, value
            self.skip_whitespace_and_comments()

            match head := self.peek():
                case MiscToken.comma:
                    self.advance()

                case MiscToken.closing_brace:
                    self.advance()
                    return

                case _:
                    raise self.error('Entry values must end with a comma or closing brace', i_first_visible_token=entry_start_i)

            self.skip_whitespace_and_comments()

    def perform_global_validation(self, properties: dict[str, PropertyValue], entry_start_i: int) -> None:
        if 'title' not in properties:
            raise self.error('Entry without title', i_first_token=entry_start_i, i_last_token=self.index - 1)

        if 'author' not in properties:
            raise self.error('Entry without authors', i_first_token=entry_start_i, i_last_token=self.index - 1)

        if 'language' not in properties:
            raise self.error('Entry without language', i_first_token=entry_start_i, i_last_token=self.index - 1)

    @list_accumulator
    def process_authors(self, properties: dict[str, PropertyValue], key: str, entry_start_i: int, display_names_key: str | None = None) -> Iterable[BibAuthor]:
        value = properties.pop(key, None)

        if value is None:
            return

        error_message = f'Property {display_names_key!r} does not match the structure of {key!r}'
        error_kwargs = dict(
            i_first_token=entry_start_i,
            i_last_token=self.index - 1
        )

        display_segments: deque[str] | None = None

        if display_names_key is not None and display_names_key in properties:
            display_segments = deque()

            for author in self.parse_authors(properties.pop(display_names_key), entry_start_i, entry_start_i):
                display_segments.append(str(author))

        for author in self.parse_authors(value, entry_start_i, entry_start_i):
            if display_segments is None:
                yield author
                continue

            if len(display_segments) == 0:
                raise self.error(error_message, **error_kwargs)

            yield author._replace(display_name=display_segments.popleft().strip())

        if display_segments and len(display_segments) > 0:
            raise self.error(error_message, **error_kwargs)


    def parse(self) -> Iterable[BibEntry]:
        entry_names = set[str]()
        self.skip_whitespace_and_comments()

        while not self.is_at_end():
            if self.peek() != MiscToken.at:
                raise self.error('A bibtex entry must start with @')

            entry_start_i = self.index
            self.advance()
            entry_type = self.parse_entry_type()

            if self.is_at_end() or self.peek() != MiscToken.opening_brace:
                raise self.error('An opening brace must follow a bibtex entry type', i_first_visible_token=entry_start_i)

            self.advance()
            entry_name = self.parse_entry_name(entry_names)
            entry_names.add(entry_name)

            if self.peek() == MiscToken.closing_brace:
                raise self.error('Entry without properties', i_first_token=entry_start_i)

            if self.peek() != MiscToken.comma:
                raise self.error('An opening brace must follow a bibtex entry type')

            self.advance()
            self.skip_whitespace_and_comments()

            properties = dict(self.parse_entry_properties(entry_start_i))
            self.perform_global_validation(properties, entry_start_i)

            yield BibEntry(
                entry_type=entry_type,
                entry_name=entry_name,
                title=str(properties.pop('title')),
                authors=self.process_authors(properties, 'author', entry_start_i, display_names_key='shortauthor'),
                translators=self.process_authors(properties, 'translator', entry_start_i),
                advisors=self.process_authors(properties, 'advisor', entry_start_i),
                editors=self.process_authors(properties, 'editor', entry_start_i),
                language=cast(BibLanguage, str(properties.pop('language'))),
                **{key: str(value) for key, value in properties.items()}
            )

            self.skip_whitespace_and_comments()


def parse_bibtex(string: str) -> Sequence[BibEntry]:
    tokens = tokenize_bibtex(string)

    with BibParser(tokens) as parser:
        return list(parser.parse())
