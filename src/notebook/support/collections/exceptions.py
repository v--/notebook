from ..exceptions import NotebookSupportError


class CollectionError(NotebookSupportError):
    pass


class UnsupportedItemError(CollectionError, ValueError):
    pass


class MissingKeyError(CollectionError, KeyError):
    pass


class KeyExistsError(CollectionError, KeyError):
    pass
