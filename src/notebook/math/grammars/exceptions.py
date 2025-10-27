from ..exceptions import NotebookMathError


class GrammarError(NotebookMathError):
    pass


class UnknownSymbolError(GrammarError):
    pass


class TokenizationError(GrammarError):
    pass


class ParserError(GrammarError):
    pass
