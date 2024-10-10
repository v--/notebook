from ...exceptions import NotebookCodeError


class CollectionError(NotebookCodeError):
    pass


class MissingKeyError(CollectionError, KeyError):
    pass


class KeyExistsError(CollectionError, KeyError):
    pass
