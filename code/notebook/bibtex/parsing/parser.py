from collections import deque
from collections.abc import Collection, Iterable, Sequence
from dataclasses import replace
from typing import cast

from ...parsing.parser import Parser
from ...support.iteration import list_accumulator
from ..entry import ENTRY_KEYS, ENTRY_TYPE_LIST, BibAuthor, BibEntry, BibEntryType
from ..string import BibString, CompositeString, CompositeStringBuilder
from .parser_context import BibEntryContext, BibValueContext
from .tokenizer import tokenize_bibtex
from .tokens import BibToken


class BibParser(Parser[BibToken]):
    def skip_spaces(self) -> BibToken | None:
        while head := self.peek():
            match head.kind:
                case 'SPACE' | 'TAB':
                    self.advance()

                case _:
                    return head

        return None

    def skip_whitespace_and_comments(self) -> BibToken | None:
        while head := self.peek():
            match head.kind:
                case 'SPACE' | 'TAB' | 'LINE_BREAK':
                    self.advance()

                case 'PERCENT':
                    self.advance()

                    while (head := self.peek()) and head.kind != 'LINE_BREAK':
                        self.advance()

                case _:
                    return head

        return None

    def parse_entry_name(self, name_context: 'BibValueContext', existing_names: Collection[str]) -> str:
        # Entry names may even contain %, which is otherwise used for comments
        while (head := self.peek()) and head.kind not in ['CLOSING_BRACE', 'COMMA', 'LINE_BREAK']:
            self.advance()

        if name_context.is_empty():
            raise name_context.annotate_token_error('Expected an entry name')

        name_context.close_at_previous_token()
        entry_name = name_context.get_context_string()

        if len(entry_name) == 0:
            raise name_context.annotate_context_error('Expected an entry name')

        if entry_name in existing_names:
            raise name_context.annotate_context_error('Duplicate entry name')

        return entry_name

    def parse_property_key(self, entry_context: 'BibEntryContext', existing_keys: Collection[str]) -> str:
        head = self.peek_unsafe()

        if head.kind != 'WORD':
            raise entry_context.annotate_token_error('Expected an entry key')

        if head.value in existing_keys:
            raise entry_context.annotate_token_error('Duplicate key')

        if head.value not in ENTRY_KEYS.known:
            raise entry_context.annotate_token_error('Unrecognized key')

        self.advance()
        return head.value

    def _parse_escape_sequence(self, value_context: 'BibValueContext') -> str:
        lookahead = self.peek_multiple(2)

        if len(lookahead) == 1:
            raise value_context.annotate_token_error('No symbol to escape')

        self.advance(2)

        match lookahead[1].kind:
            case 'OPENING_BRACE' | 'CLOSING_BRACE' | 'AMPERSAND' | 'BACKSLASH' | 'AT':
                return lookahead[1].value

            case _:
                return '\\' + lookahead[1].value

    def parse_value_in_context(self, value_context: 'BibValueContext', key: str, *, quotes: bool) -> None:
        self.advance()

        builder = value_context.string_builder
        verbatim = False

        while head := self.peek():
            match head.kind:
                case 'LINE_BREAK':
                    raise value_context.annotate_token_error('Unexpected line break')

                case 'DOUBLE_QUOTES' if quotes:
                    if quotes:
                        builder.flush(verbatim=verbatim)
                        self.advance()
                        return

                case 'CLOSING_BRACE':
                    if verbatim:
                        builder.flush(verbatim=True)
                        verbatim = False
                        self.advance()
                    elif quotes:
                        builder.append('"')
                        self.advance()
                    else:
                        builder.flush(verbatim=False)
                        self.advance()
                        return

                case 'OPENING_BRACE':
                    lookahead = self.peek_multiple(3)

                    if quotes and \
                        lookahead[0].kind == 'OPENING_BRACE' and \
                        lookahead[1].kind == 'DOUBLE_QUOTES' and \
                        lookahead[2].kind == 'CLOSING_BRACE':
                        builder.append('"')
                        self.advance(3)
                    else:
                        builder.flush(verbatim=verbatim)
                        verbatim = True
                        self.advance()

                case 'BACKSLASH':
                    builder.append(self._parse_escape_sequence(value_context))

                case 'WORD' if key in ENTRY_KEYS.list and (head.value == 'AND' or head.value == 'and'):
                    if verbatim:
                        builder.append(head.value)
                    else:
                        builder.flush(verbatim=False)
                        builder.append(head.value)
                        builder.flush(verbatim=False)

                    self.advance()

                case _:
                    builder.append(head.value)
                    self.advance()

        raise value_context.annotate_context_error('Unclosed delimiter')

    def parse_raw_value(self) -> BibString:
        builder = CompositeStringBuilder()
        verbatim = False
        value_context = BibValueContext(self, entry_context=None)

        while head := self.peek():
            match head.kind:
                case 'LINE_BREAK':
                    raise value_context.annotate_token_error('Unexpected line break')

                case 'CLOSING_BRACE':
                    if verbatim:
                        builder.flush(verbatim=verbatim)
                        verbatim = False
                        self.advance()
                    else:
                        builder.flush(verbatim=verbatim)
                        self.advance()

                case 'OPENING_BRACE':
                    builder.flush(verbatim=verbatim)
                    verbatim = True
                    self.advance()

                case 'BACKSLASH':
                    builder.append(self._parse_escape_sequence(value_context))

                case _:
                    builder.append(head.value)
                    self.advance()

        builder.flush(verbatim=verbatim)
        return builder.get_value()

    def parse_author_string(self, source: BibString) -> BibAuthor:
        return BibAuthor(full_name=source.strip())

    def parse_list(self, value_context: 'BibValueContext') -> Iterable[BibString]:
        value = value_context.string_builder.get_value()
        expecting_and = False
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
                    raise value_context.annotate_context_error('Cannot parse list')
            elif not segment.isspace():
                buffer.append(segment)
                expecting_and = True

        if not expecting_and:
            raise value_context.annotate_context_error('Cannot parse list')

        if len(buffer) > 0:
            yield CompositeString(buffer) if len(buffer) > 1 else buffer[0].strip()

    def parse_authors(self, value_context: 'BibValueContext') -> Iterable[BibAuthor]:
        for entry in self.parse_list(value_context):
            yield self.parse_author_string(entry)

    def perform_inline_validation(self, value_context: 'BibValueContext', key: str) -> None:
        value_str = str(value_context.string_builder.get_value())

        if len(value_str) == 0 or value_str.isspace():
            raise value_context.annotate_context_error('Empty value')

        if key in ENTRY_KEYS.author:
            for _ in self.parse_authors(value_context):
                pass

    def parse_entry_properties(self, entry_context: 'BibEntryContext') -> Iterable[tuple[str, 'BibValueContext']]:
        existing_keys = set[str]()
        last_comma: BibToken | None = None

        while (head := self.peek()) and head.kind != 'CLOSING_BRACE':
            key = self.parse_property_key(entry_context, existing_keys)
            existing_keys.add(key)

            head = self.skip_spaces()

            if not head or head.kind != 'EQUALS':
                raise entry_context.annotate_token_error('Expected an equality sign')

            self.advance()
            head = self.skip_spaces()

            if not head:
                raise entry_context.annotate_token_error('Expected a value')

            value_context = BibValueContext(self, entry_context)

            match head.kind:
                case 'DECIMAL':
                    value_context.string_builder.append(head.value)
                    value_context.string_builder.flush(verbatim=False)
                    self.advance()

                case 'OPENING_BRACE':
                    self.parse_value_in_context(value_context, key, quotes=False)

                case 'DOUBLE_QUOTES':
                    self.parse_value_in_context(value_context, key, quotes=True)

                case _:
                    raise value_context.annotate_token_error('Invalid entry value')

            value_context.close_at_previous_token()
            self.perform_inline_validation(value_context, key)
            yield key, value_context

            head = self.skip_whitespace_and_comments()

            if not head:
                raise entry_context.annotate_token_error('Expected a closing brace')

            match head.kind:
                case 'COMMA':
                    last_comma = head
                    self.advance()

                case 'CLOSING_BRACE':
                    entry_context.close_at_current_token()
                    self.advance()
                    return

                case _:
                    raise entry_context.annotate_context_error('Entry values must end with a comma or closing brace')

            self.skip_whitespace_and_comments()

        if last_comma is not None:
            raise entry_context.annotate_token_error('Trailing commas are disallowed', token=last_comma)

    def perform_global_validation(self, entry_context: 'BibEntryContext', properties: dict[str, 'BibValueContext']) -> None:
        if 'title' not in properties:
            raise entry_context.annotate_context_error('Entry without title')

    @list_accumulator
    def process_authors(self, properties: dict[str, 'BibValueContext'], key: str) -> Iterable[BibAuthor]:
        if key not in properties:
            return

        short_key = f'short{key}'

        long_value_context = properties.pop(key)
        short_value_context = properties.pop(short_key, None)
        error_message = f'Property {short_key!r} does not match the structure of {key!r}'
        short_segments = deque[BibString]()

        if short_value_context:
            for author in self.parse_authors(short_value_context):
                short_segments.append(author.full_name)

        for author in self.parse_authors(long_value_context):
            if short_value_context is None or author.full_name == 'others':
                yield author
                continue

            if len(short_segments) == 0:
                raise short_value_context.annotate_context_error(error_message)

            yield replace(author, short_name=short_segments.popleft())

        if short_value_context and len(short_segments) > 0:
            raise short_value_context.annotate_context_error(error_message)

    def process_language(self, properties: dict[str, 'BibValueContext'], key: str) -> Sequence[BibString]:
        value_context = properties.pop(key, None)

        if value_context is None:
            return []

        return list(self.parse_list(value_context))

    def iter_entries(self) -> Iterable[BibEntry]:
        head = self.skip_whitespace_and_comments()

        if not head:
            return

        entry_names = set[str]()
        entry_context = BibEntryContext(self)
        name_context = BibValueContext(self, entry_context)

        while head := self.peek():
            entry_context.reset()

            if head.kind != 'AT':
                raise entry_context.annotate_token_error('A bibtex entry must start with @')

            head = self.advance_and_peek()

            if not head or head.kind != 'WORD':
                raise entry_context.annotate_token_error('Expected an entry type')

            entry_type = head.value

            if entry_type not in ENTRY_TYPE_LIST:
                raise entry_context.annotate_token_error('Unrecognized entry type')

            head = self.advance_and_peek()

            if not head or head.kind != 'OPENING_BRACE':
                raise entry_context.annotate_token_error('An opening brace must follow a bibtex entry type')

            head = self.advance_and_peek()

            if not head:
                raise name_context.annotate_token_error('Expected an entry name')

            name_context.reset()
            entry_name = self.parse_entry_name(name_context, entry_names)
            entry_names.add(entry_name)

            head = self.peek()

            if not head or head.kind == 'CLOSING_BRACE':
                raise entry_context.annotate_context_error('Entry without properties')

            if head.kind != 'COMMA':
                raise entry_context.annotate_token_error('An opening brace must follow a bibtex entry type')

            self.advance()
            self.skip_whitespace_and_comments()

            properties = dict(self.parse_entry_properties(entry_context))
            self.perform_global_validation(entry_context, properties)

            yield BibEntry(
                entry_type=cast('BibEntryType', entry_type),
                entry_name=entry_name,
                languages=self.process_language(properties, 'language'),
                origlanguages=self.process_language(properties, 'origlanguage'),
                authors=self.process_authors(properties, 'author'),
                compilers=self.process_authors(properties, 'compiler'),
                translators=self.process_authors(properties, 'translator'),
                advisors=self.process_authors(properties, 'advisor'),
                editors=self.process_authors(properties, 'editor'),
                annotators=self.process_authors(properties, 'annotator'),
                **{
                    key: context.string_builder.get_value() for key, context in properties.items()
                }
            )

            self.skip_whitespace_and_comments()


def parse_bibtex(source: str) -> Sequence[BibEntry]:
    tokens = tokenize_bibtex(source)

    with BibParser(source, tokens) as parser:
        return list(parser.iter_entries())


def parse_value(source: str) -> BibString:
    tokens = tokenize_bibtex(source)

    with BibParser(source, tokens) as parser:
        return parser.parse_raw_value()
