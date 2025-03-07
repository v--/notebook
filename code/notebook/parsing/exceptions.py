from ..exceptions import NotebookCodeError


class ParsingError(NotebookCodeError):
    pass


class TokenizationError(ParsingError):
    pass
