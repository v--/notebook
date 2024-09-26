from collections import deque
from collections.abc import Iterable, Sequence
from typing import NamedTuple, cast, get_args

from ...parsing.mixins.whitespace import WhitespaceParserMixin
from ...parsing.parser import Parser
from ...parsing.whitespace import Whitespace
from ...support.iteration import list_accumulator
from ..entry import BibAuthor, BibEntry, BibEntryType
from .tokenizer import tokenize_bibtex
from .tokens import BibToken, MiscToken, NumberToken, WordToken


AUTHOR_KEYS = {key_name for _, key_name, _ in BibEntry.get_author_fields()} | {short_key_name for _, _, short_key_name in BibEntry.get_author_fields()}


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
        while not self.is_at_end():
            head = self.peek()

            if isinstance(head, Whitespace):
                self.advance()
            elif head == MiscToken.percent:
                self.gobble_and_skip(lambda token: token != '\n')
            else:
                break

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
        key = self.gobble_string(lambda token: isinstance(token, WordToken))

        if len(key) == 0:
            raise self.error('Expected an entry key')

        return key

    def parse_value(self, entry_start_i: int, value_start_i: int, *, quotes: bool) -> PropertyValue:  # noqa: PLR0912, PLR0915, C901
        if quotes:
            assert self.peek() == MiscToken.quotes
        else:
            assert self.peek() == MiscToken.opening_brace

        self.advance()

        builder = PropertyValueBuilder()
        verbatim = False

        while not self.is_at_end():
            match head := self.peek():
                case Whitespace.line_break:
                    raise self.error('Unexpected line break', i_first_visible_token=entry_start_i)

                case MiscToken.quotes if quotes:
                    if quotes:
                        builder.flush()
                        self.advance()
                        return builder.get_value()

                case MiscToken.closing_brace:
                    if verbatim:
                        builder.append('}')
                        builder.flush()
                        verbatim = False
                        self.advance()
                    elif quotes:
                        builder.append('}')
                        self.advance()
                    else:
                        builder.flush()
                        self.advance()
                        return builder.get_value()

                case MiscToken.opening_brace:
                    lookahead = self.peek_multiple(3)

                    if quotes and lookahead == [MiscToken.opening_brace, MiscToken.quotes, MiscToken.closing_brace]:
                        builder.append('"')
                        self.advance(3)
                    else:
                        verbatim = True
                        builder.flush()
                        builder.append('{')
                        self.advance()

                case MiscToken.backslash:
                    lookahead = self.peek_multiple(2)

                    if len(lookahead) == 1:
                        raise self.error('Invalid escaped symbol', i_first_visible_token=entry_start_i)

                    match lookahead[1]:
                        case MiscToken.opening_brace | MiscToken.closing_brace | MiscToken.ampersand | MiscToken.backslash | MiscToken.at:
                            builder.append(str(lookahead[1]))
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

        raise self.error('Unclosed delimiter', i_first_token=value_start_i, i_first_visible_token=entry_start_i)

    def parse_author_string(self, string: str) -> BibAuthor:
        if string.startswith('{') and string.endswith('}'):
            return BibAuthor(full_name=string[1:-1], verbatim=True)

        return BibAuthor(full_name=string, verbatim=False)

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

            yield self.parse_author_string(segment.strip())

            expecting_and = True

        if not expecting_and:
            raise self.error('Cannot parse author string', **error_kwargs)

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

    def parse_entry_properties(self, entry_start_i: int) -> Iterable[tuple[str, PropertyValue]]:
        keys = set[str]()
        last_comma_i: int | None = None

        while not self.is_at_end() and self.peek() != MiscToken.closing_brace:
            key_start_i = self.index
            key = self.parse_property_key()

            if key in keys:
                raise self.error('Duplicate key', i_first_token=key_start_i, i_first_visible_token=entry_start_i, i_last_token=self.index - 1)

            if not BibEntry.is_known_key(key):
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
                    value = self.parse_value(entry_start_i, value_start_i, quotes=False)

                case MiscToken.quotes:
                    value = self.parse_value(entry_start_i, value_start_i, quotes=True)

                case _:
                    raise self.error('Invalid entry value', i_first_visible_token=entry_start_i)

            self.perform_inline_validation(key, value, entry_start_i, value_start_i)
            yield key, value
            self.skip_whitespace_and_comments()

            match head := self.peek():
                case MiscToken.comma:
                    last_comma_i = self.index
                    self.advance()

                case MiscToken.closing_brace:
                    self.advance()
                    return

                case _:
                    raise self.error('Entry values must end with a comma or closing brace', i_first_visible_token=entry_start_i)

            self.skip_whitespace_and_comments()

        if last_comma_i is not None:
            raise self.error('Trailing commas are disallowed', i_first_visible_token=entry_start_i, i_first_token=last_comma_i, i_last_token=last_comma_i)

    def perform_global_validation(self, properties: dict[str, PropertyValue], entry_start_i: int) -> None:
        if 'title' not in properties:
            raise self.error('Entry without title', i_first_token=entry_start_i, i_last_token=self.index - 1)

        if 'language' not in properties:
            raise self.error('Entry without language', i_first_token=entry_start_i, i_last_token=self.index - 1)

    @list_accumulator
    def process_authors(self, properties: dict[str, PropertyValue], key: str, entry_start_i: int) -> Iterable[BibAuthor]:
        if key not in properties:
            return

        short_key = f'short{key}'

        value = properties.pop(key)
        error_message = f'Property {short_key!r} does not match the structure of {key!r}'
        error_kwargs = dict(
            i_first_token=entry_start_i,
            i_last_token=self.index - 1
        )

        short_segments: deque[str] | None = None

        if short_key is not None and short_key in properties:
            short_segments = deque()

            for author in self.parse_authors(properties.pop(short_key), entry_start_i, entry_start_i):
                short_segments.append(author.full_name)

        for author in self.parse_authors(value, entry_start_i, entry_start_i):
            if short_segments is None:
                yield author
                continue

            if len(short_segments) == 0:
                raise self.error(error_message, **error_kwargs)

            yield author._replace(short_name=short_segments.popleft().strip())

        if short_segments and len(short_segments) > 0:
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
                authors=self.process_authors(properties, 'author', entry_start_i),
                translators=self.process_authors(properties, 'translator', entry_start_i),
                advisors=self.process_authors(properties, 'advisor', entry_start_i),
                editors=self.process_authors(properties, 'editor', entry_start_i),
                **{key: str(value) for key, value in properties.items()}
            )

            self.skip_whitespace_and_comments()


def parse_bibtex(string: str) -> Sequence[BibEntry]:
    tokens = tokenize_bibtex(string)

    with BibParser(tokens) as parser:
        return list(parser.parse())
