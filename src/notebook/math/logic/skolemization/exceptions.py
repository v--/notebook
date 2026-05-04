from notebook.math.logic.exceptions import FormalLogicError


class SkolemizationError(FormalLogicError):
    pass


class InvalidModelError(SkolemizationError):
    pass
