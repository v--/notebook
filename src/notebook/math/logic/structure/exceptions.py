from ..exceptions import FormalLogicError


class FormalLogicStructureError(FormalLogicError):
    pass


class MissingVariableError(FormalLogicStructureError, KeyError):
    pass
