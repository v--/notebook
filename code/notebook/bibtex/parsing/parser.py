from collections import deque
from collections.abc import Collection, Iterable, Sequence
from typing import cast, get_args

from ...parsing.mixins.whitespace import WhitespaceParserMixin
from ...parsing.parser import Parser
from ...parsing.whitespace import Whitespace
from ...support.iteration import list_accumulator
from ..entry import BibAuthor, BibEntry, BibEntryType
from ..string import BibString, CompositeString, CompositeStringBuilder
from .tokenizer import tokenize_bibtex
from .tokens import BibToken, MiscToken, NumberToken, WordToken


AUTHOR_KEYS = frozenset(key_name for _, key_name, _ in BibEntry.get_author_fields()) | frozenset(short_key_name for _, _, short_key_name in BibEntry.get_author_fields())
LIST_KEYS = AUTHOR_KEYS | frozenset(key_name for _, key_name in BibEntry.get_list_fields())


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

    def parse_entry_name(self, existing: Collection[str]) -> str:
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

    def parse_escape_sequence(self, i_start: int) -> str:
        lookahead = self.peek_multiple(2)
        assert lookahead[0] == MiscToken.backslash

        if len(lookahead) == 1:
            raise self.error('No symbol to escape', i_first_visible_token=i_start)

        self.advance(2)

        match lookahead[1]:
            case MiscToken.opening_brace | MiscToken.closing_brace | MiscToken.ampersand | MiscToken.backslash | MiscToken.at:
                return str(lookahead[1])

            case _:
                return str(lookahead[0]) + str(lookahead[1])

    def parse_value(self, key: str, entry_start_i: int, value_start_i: int, *, quotes: bool) -> BibString:  # noqa: PLR0912
        if quotes:
            assert self.peek() == MiscToken.quotes
        else:
            assert self.peek() == MiscToken.opening_brace

        self.advance()

        builder = CompositeStringBuilder()
        verbatim = False

        while not self.is_at_end():
            match head := self.peek():
                case Whitespace.line_break:
                    raise self.error('Unexpected line break', i_first_visible_token=entry_start_i)

                case MiscToken.quotes if quotes:
                    if quotes:
                        builder.flush(verbatim=verbatim)
                        self.advance()
                        return builder.get_value()

                case MiscToken.closing_brace:
                    if verbatim:
                        builder.flush(verbatim=True)
                        verbatim = False
                        self.advance()
                    elif quotes:
                        builder.append('}')
                        self.advance()
                    else:
                        builder.flush(verbatim=False)
                        self.advance()
                        return builder.get_value()

                case MiscToken.opening_brace:
                    lookahead = self.peek_multiple(3)

                    if quotes and lookahead == [MiscToken.opening_brace, MiscToken.quotes, MiscToken.closing_brace]:
                        builder.append('"')
                        self.advance(3)
                    else:
                        builder.flush(verbatim=verbatim)
                        verbatim = True
                        self.advance()

                case MiscToken.backslash:
                    builder.append(self.parse_escape_sequence(i_start=entry_start_i))

                case WordToken('and') | WordToken('AND') if key in LIST_KEYS:
                    if verbatim:
                        builder.append(str(head))
                    else:
                        builder.flush(verbatim=False)
                        builder.append(str(head))
                        builder.flush(verbatim=False)

                    self.advance()

                case _:
                    builder.append(str(head))
                    self.advance()

        raise self.error('Unclosed delimiter', i_first_token=value_start_i, i_first_visible_token=entry_start_i)

    def parse_raw_value(self) -> BibString:
        builder = CompositeStringBuilder()
        verbatim = False
        i_start = self.index

        while not self.is_at_end():
            match head := self.peek():
                case Whitespace.line_break:
                    raise self.error('Unexpected line break', i_first_visible_token=i_start)

                case MiscToken.closing_brace:
                    if verbatim:
                        builder.flush(verbatim=verbatim)
                        verbatim = False
                        self.advance()
                    else:
                        builder.flush(verbatim=verbatim)
                        self.advance()

                case MiscToken.opening_brace:
                    builder.flush(verbatim=verbatim)
                    verbatim = True
                    self.advance()

                case MiscToken.backslash:
                    builder.append(self.parse_escape_sequence(i_start=i_start))

                case _:
                    builder.append(str(head))
                    self.advance()

        builder.flush(verbatim=verbatim)
        return builder.get_value()

    def parse_author_string(self, string: BibString) -> BibAuthor:
        return BibAuthor(full_name=string.strip())

    def parse_list(self, value: BibString, entry_start_i: int, value_start_i: int) -> Iterable[BibString]:
        expecting_and = False

        error_message = 'Cannot parse list'
        error_kwargs = dict(
            i_first_token=value_start_i,
            i_last_token=self.index - 1,
            i_first_visible_token=entry_start_i
        )

        buffer = list[BibString]()

        for segment in value.segments if isinstance(value, CompositeString) else [value]:
            if segment == 'and' or segment == 'AND':
                if expecting_and:
                    if len(buffer) > 0:
                        yield CompositeString(buffer) if len(buffer) > 1 else buffer[0].strip()
                        buffer = []

                    expecting_and = False
                    continue
                else:
                    raise self.error(error_message, **error_kwargs)
            elif not segment.isspace():
                buffer.append(segment)
                expecting_and = True

        if not expecting_and:
            raise self.error(error_message, **error_kwargs)

        if len(buffer) > 0:
            yield CompositeString(buffer) if len(buffer) > 1 else buffer[0].strip()

    def parse_authors(self, value: BibString, entry_start_i: int, value_start_i: int) -> Iterable[BibAuthor]:
        for entry in self.parse_list(value, entry_start_i, value_start_i):
            yield self.parse_author_string(entry)

    def perform_inline_validation(self, key: str, value: BibString, entry_start_i: int, value_start_i: int) -> None:
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

    def parse_entry_properties(self, entry_start_i: int) -> Iterable[tuple[str, BibString]]:
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
            value: BibString

            match head := self.peek():
                case NumberToken():
                    value = str(head)
                    self.advance()

                case MiscToken.opening_brace:
                    value = self.parse_value(key, entry_start_i, value_start_i, quotes=False)

                case MiscToken.quotes:
                    value = self.parse_value(key, entry_start_i, value_start_i, quotes=True)

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

    def perform_global_validation(self, properties: dict[str, BibString], entry_start_i: int) -> None:
        if 'title' not in properties:
            raise self.error('Entry without title', i_first_token=entry_start_i, i_last_token=self.index - 1)

    @list_accumulator
    def process_authors(self, properties: dict[str, BibString], key: str, entry_start_i: int) -> Iterable[BibAuthor]:
        if key not in properties:
            return

        short_key = f'short{key}'

        value = properties.pop(key)
        error_message = f'Property {short_key!r} does not match the structure of {key!r}'
        error_kwargs = dict(
            i_first_token=entry_start_i,
            i_last_token=self.index - 1
        )

        short_segments: deque[BibString] | None = None

        if short_key is not None and short_key in properties:
            short_segments = deque()

            for author in self.parse_authors(properties.pop(short_key), entry_start_i, entry_start_i):
                short_segments.append(author.full_name)

        for author in self.parse_authors(value, entry_start_i, entry_start_i):
            if short_segments is None or author.full_name == 'others':
                yield author
                continue

            if len(short_segments) == 0:
                raise self.error(error_message, **error_kwargs)

            yield author._replace(short_name=short_segments.popleft())

        if short_segments and len(short_segments) > 0:
            raise self.error(error_message, **error_kwargs)

    def process_language(self, properties: dict[str, BibString], key: str, entry_start_i: int) -> Sequence[BibString]:
        value = properties.pop(key, None)

        if value is None:
            return []

        return list(self.parse_list(value, entry_start_i, entry_start_i))

    def parse_entries(self) -> Iterable[BibEntry]:
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
                languages=self.process_language(properties, 'language', entry_start_i),
                origlanguages=self.process_language(properties, 'origlanguage', entry_start_i),
                authors=self.process_authors(properties, 'author', entry_start_i),
                translators=self.process_authors(properties, 'translator', entry_start_i),
                advisors=self.process_authors(properties, 'advisor', entry_start_i),
                editors=self.process_authors(properties, 'editor', entry_start_i),
                **properties
            )

            self.skip_whitespace_and_comments()

    parse = parse_entries


def parse_bibtex(string: str) -> Sequence[BibEntry]:
    tokens = tokenize_bibtex(string)

    with BibParser(tokens) as parser:
        return list(parser.parse())


def parse_value(string: str) -> BibString:
    tokens = tokenize_bibtex(string)

    with BibParser(tokens) as parser:
        return parser.parse_raw_value()
