from collections.abc import Iterable, Sequence

from ...parsing import Parser
from ...support.unicode import Capitalization, is_latin_string
from ..nodes import (
    BraceGroup,
    BracketGroup,
    Command,
    Environment,
    Group,
    LaTeXNode,
    SpecialNode,
    Text,
    Whitespace,
)
from .parser_context import LaTeXGroupContext
from .tokenizer import tokenize_latex
from .tokens import LaTeXTokenKind


class LaTeXParser(Parser[LaTeXTokenKind]):
    def _parse_brace[GroupT: Group](self, cls: type[GroupT], closing_kind: LaTeXTokenKind) -> GroupT:
        brace_context = LaTeXGroupContext(self)
        self.advance()

        contents = list[LaTeXNode]()

        while (head := self.peek()) and head.kind != closing_kind:
            contents.append(self.parse_node())

        if (head := self.peek()) is None or head.kind != closing_kind:
            raise brace_context.annotate_context_error(f'Unmatched {brace_context.get_first_token().value}')

        self.advance()
        return cls(contents)

    def _parse_environment(self) -> Environment:
        env_context = LaTeXGroupContext(self)
        env_context.index_start -= 1
        head = self.advance_and_peek()

        if not head or head.kind != 'OPENING_BRACE':
            raise env_context.annotate_context_error('No environment name specified')

        head = self.advance_and_peek()

        if not head or head.kind != 'TEXT':
            raise env_context.annotate_context_error('No environment name specified')

        env_name_token = head
        head = self.advance_and_peek()

        if not head or head.kind != 'CLOSING_BRACE':
            raise env_context.annotate_token_error('Unclosed brace when specifying environment name', token=env_name_token)

        head = self.advance_and_peek()

        if not head:
            raise env_context.annotate_context_error(f'Unclosed environment {env_name_token.value!r}')

        contents = list[LaTeXNode]()

        while head := self.peek():
            next_tokens = self.peek_multiple(5)

            if len(next_tokens) == 5 and \
                next_tokens[0].kind == 'BACKSLASH' and \
                next_tokens[1].kind == 'TEXT' and next_tokens[1].value == 'end' and \
                next_tokens[2].kind == 'OPENING_BRACE' and \
                next_tokens[3].kind == 'TEXT' and \
                next_tokens[4].kind == 'CLOSING_BRACE':
                self.advance(5)

                if next_tokens[3].value == env_name_token.value:
                    return Environment(name=env_name_token.value, contents=contents)

                env_context.close_at_previous_token()
                raise env_context.annotate_context_error(f'Mismatched environment {env_name_token.value!r}')

            contents.append(self.parse_node())

        raise env_context.annotate_context_error(f'Unclosed environment {env_name_token.value!r}')

    def parse_node(self) -> LaTeXNode:  # noqa: PLR0911
        head = self.peek()

        if not head:
            raise self.annotate_token_error('Unexpected end of input')

        match head.kind:
            case 'TEXT':
                self.advance()
                return Text(head.value)

            case 'BACKSLASH':
                head = self.advance_and_peek()

                if not head:
                    raise self.annotate_token_error('Unexpected end of input after backslash')

                if head.value == 'begin':
                    return self._parse_environment()

                self.advance()

                match head.kind:
                    case 'TEXT' if is_latin_string(head.value, Capitalization.mixed):
                        return Command(head.value)

                    case 'BACKSLASH':
                        return Command('\\')

                    case _:
                        return Text('\\' + head.value)

            case 'WHITESPACE':
                self.advance()
                return Whitespace(head.value)

            case 'OPENING_BRACE':
                return self._parse_brace(BraceGroup, 'CLOSING_BRACE')

            case 'OPENING_BRACKET':
                return self._parse_brace(BracketGroup, 'CLOSING_BRACKET')

            case 'CLOSING_BRACE':
                self.advance()
                return Text(head.value)

            case 'CLOSING_BRACKET':
                self.advance()
                return Text(head.value)

            case 'AT' | 'CARET' | 'PERCENT' | 'AMPERSAND' | 'UNDERSCORE' | 'DOLLAR' | 'LINE_BREAK':
                self.advance()
                return getattr(SpecialNode, head.kind.lower())

            case _:
                raise self.annotate_token_error('Unexpected token')

    def iter_nodes(self) -> Iterable[LaTeXNode]:
        while self.peek():
            yield self.parse_node()


def parse_latex(source: str) -> Sequence[LaTeXNode]:
    tokens = tokenize_latex(source)

    with LaTeXParser(source, tokens) as parser:
        return list(parser.iter_nodes())
