from ..exceptions import NotebookError


class BaseParsingError(NotebookError):
    pass


class ParserError(BaseParsingError):
    pass


class InvalidTokenError(BaseParsingError):
    pass


class TokenizerError(BaseParsingError):
    pass
