from ..exceptions import NotebookMathError


class GrammarError(NotebookMathError):
    pass


class IncompatibleGrammarError(GrammarError):
    pass


class IncompatibleRuleError(GrammarError):
    pass


class UnknownSymbolError(GrammarError):
    pass


class TokenizationError(GrammarError):
    pass
