from ..exceptions import NotebookCodeError


class BaseParsingError(NotebookCodeError):
    pass


class ParserError(BaseParsingError):
    pass


class InvalidTokenError(BaseParsingError):
    pass


class TokenizerError(BaseParsingError):
    pass
