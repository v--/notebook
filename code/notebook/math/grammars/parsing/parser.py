from collections.abc import Iterable

from ....parsing import Parser, ParsingError
from ..alphabet import NonTerminal, Terminal
from ..grammar import GrammarRule, GrammarSchema
from .parser_context import GrammarNonterminalContext, GrammarSymbolRunContext, GrammarTerminalContext
from .tokenizer import tokenize_grammar
from .tokens import GrammarToken


class GrammarParser(Parser[GrammarToken]):
    def _skip_spaces(self) -> GrammarToken | None:
        while (head := self.peek()) and head.kind == 'SPACE':
            self.advance()

        return head

    def _skip_empty_lines(self) -> GrammarToken | None:
        while (head := self.peek()) and head.kind == 'LINE_BREAK':
            self.advance()
            self._skip_spaces()

        return head

    def parse_terminal(self) -> Terminal:
        if (head := self.peek()) is None:
            raise ParsingError('Empty input')

        context = GrammarTerminalContext(self)

        if head.kind != 'DOUBLE_QUOTES':
            raise self.annotate_token_error('Expected double quotes')

        head = self.advance_and_peek()

        if head is None:
            raise self.annotate_token_error('Expected a terminal')

        if head.kind == 'DOUBLE_QUOTES':
            raise context.annotate_context_error('Empty terminals are disallowed')

        while (head := self.peek()) and head.kind != 'DOUBLE_QUOTES':
            lookahead = self.peek_multiple(2)

            if len(lookahead) == 2 and lookahead[0].kind == 'BACKSLASH' and lookahead[1].kind == 'DOUBLE_QUOTES':
                self.advance(2)
            else:
                self.advance()

        if head is None:
            raise context.annotate_context_error('Terminal has no matching closing quotes')

        self.advance()
        context.close_at_previous_token()
        value = context.get_terminal_value()

        if len(value) > 1:
            raise context.annotate_context_error('Multi-symbol terminals are disallowed')

        return Terminal(value)

    def parse_nonterminal(self) -> NonTerminal:
        if (head := self.peek()) is None:
            raise ParsingError('Empty input')

        context = GrammarNonterminalContext(self)

        if head.kind != 'OPENING_CHEVRON':
            raise self.annotate_token_error('Expected an opening chevron')

        head = self.advance_and_peek()

        if head is None:
            raise self.annotate_token_error('Expected a nonterminal')

        if head.kind == 'CLOSING_CHEVRON':
            raise context.annotate_context_error('Empty nonterminals are disallowed')

        while (head := self.peek()) and head.kind != 'CLOSING_CHEVRON':
            lookahead = self.peek_multiple(2)

            if len(lookahead) == 2 and \
                lookahead[0].kind == 'BACKSLASH' and \
                (lookahead[1].kind == 'OPENING_CHEVRON' or lookahead[1].kind == 'CLOSING_CHEVRON'):
                self.advance(2)
            elif head.kind == 'OPENING_CHEVRON':
                raise context.annotate_context_error('Nested nonterminals are disallowed')
            else:
                self.advance()

        if head is None:
            raise context.annotate_context_error('Nonterminal has no matching closing chevron')

        self.advance()
        context.close_at_previous_token()
        return NonTerminal(context.get_nonterminal_value())

    def _iter_rule_src_symbols(self, context: GrammarSymbolRunContext) -> Iterable[Terminal | NonTerminal]:
        contains_nonterminal = False

        while head := self.peek():
            match head.kind:
                case 'EPSILON':
                    raise self.annotate_token_error('ε is disallowed on the left side of a rule')

                case 'DOUBLE_QUOTES':
                    yield self.parse_terminal()
                    context.close_at_previous_token()
                    self._skip_spaces()

                case 'OPENING_CHEVRON':
                    yield self.parse_nonterminal()
                    context.close_at_previous_token()
                    contains_nonterminal = True
                    self._skip_spaces()

                case _:
                    break

        if not contains_nonterminal:
            raise context.annotate_context_error('The left side of a rule must contain at least one nonterminal')

    def parse_rule_dest(self, context: GrammarSymbolRunContext) -> Iterable[Terminal | NonTerminal]:
        is_non_epsilon_rule = False
        is_epsilon_rule = False

        while head := self.peek():
            match head.kind:
                case 'EPSILON':
                    is_epsilon_rule = True
                    self.advance()
                    context.close_at_previous_token()
                    self._skip_spaces()

                case 'DOUBLE_QUOTES':
                    is_non_epsilon_rule = True
                    yield self.parse_terminal()
                    context.close_at_previous_token()
                    self._skip_spaces()

                case 'OPENING_CHEVRON':
                    is_non_epsilon_rule = True
                    yield self.parse_nonterminal()
                    context.close_at_previous_token()
                    self._skip_spaces()

                case _:
                    break

        if is_epsilon_rule == is_non_epsilon_rule:
            raise context.annotate_context_error('The right side of a rule must contain terminals and nonterminals and at most a single ε')

    def iter_rules_on_line(self) -> Iterable[GrammarRule]:
        head = self._skip_spaces()

        if head is None:
            raise ParsingError('Expected a rule')

        if head.kind == 'RIGHT_ARROW':
            raise self.annotate_token_error('The left side of a rule must be nonempty')

        context = GrammarSymbolRunContext(self)
        src = list(self._iter_rule_src_symbols(context))

        head = self.peek()

        if head is None or head.kind != 'RIGHT_ARROW':
            raise context.annotate_context_error('Expected an arrow after the left side of a rule')

        self.advance()
        self._skip_spaces()

        while self.peek():
            context.reset()
            dest = list(self.parse_rule_dest(context))

            yield GrammarRule(src, dest)
            head = self._skip_spaces()

            if head:
                self.advance()
                self._skip_spaces()

                if head.kind == 'LINE_BREAK':
                    return

            if head is None or head.kind != 'PIPE':
                break

        while (head := self.peek()) and head.kind != 'LINE_BREAK':
            self.advance()

        context.close_at_previous_token()
        raise context.annotate_context_error('The right side of a rule must contain a pipe between runs of terminals, nonterminals and ε')

    def iter_rules(self) -> Iterable[GrammarRule]:
        self._skip_empty_lines()

        while self.peek():
            yield from self.iter_rules_on_line()
            self._skip_empty_lines()

    def parse_schema(self) -> GrammarSchema:
        rules = list(self.iter_rules())

        if len(rules) == 0:
            raise ParsingError('Expected at least one grammar rule')

        return GrammarSchema(rules)


def parse_grammar_schema(source: str) -> GrammarSchema:
    tokens = tokenize_grammar(source)

    with GrammarParser(source, tokens) as parser:
        return parser.parse_schema()


def parse_grammar_rule_line(source: str) -> GrammarSchema:
    tokens = tokenize_grammar(source)

    with GrammarParser(source, tokens) as parser:
        return GrammarSchema(list(parser.iter_rules_on_line()))


def parse_terminal(source: str) -> Terminal:
    tokens = tokenize_grammar(source)

    with GrammarParser(source, tokens) as parser:
        return parser.parse_terminal()


def parse_nonterminal(source: str) -> NonTerminal:
    tokens = tokenize_grammar(source)

    with GrammarParser(source, tokens) as parser:
        return parser.parse_nonterminal()
