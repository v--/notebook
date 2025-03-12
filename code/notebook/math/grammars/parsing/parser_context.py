from ....parsing import ParserContext
from .tokens import GrammarTokenKind


class GrammarTerminalContext(ParserContext[GrammarTokenKind]):
    def get_terminal_value(self) -> str:
        context_string = self.get_context_string()
        return context_string[1:-1].replace('\\"', '"')


class GrammarNonterminalContext(ParserContext[GrammarTokenKind]):
    def get_nonterminal_value(self) -> str:
        context_string = self.get_context_string()
        return context_string[1:-1].replace('\\<', '<').replace('\\>', '>')


class GrammarSymbolRunContext(ParserContext[GrammarTokenKind]):
    pass
