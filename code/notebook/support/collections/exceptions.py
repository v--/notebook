from ...exceptions import NotebookCodeError


class CollectionError(NotebookCodeError):
    pass


class UnsupportedItemError(CollectionError, ValueError):
    pass


class MissingKeyError(CollectionError, KeyError):
    pass


class KeyExistsError(CollectionError, KeyError):
    pass
