from notebook.math.logic.exceptions import FormalLogicError


class FormalLogicStructureError(FormalLogicError):
    pass


class FormalLogicInterpretationError(FormalLogicStructureError):
    pass


class MissingInterpretationError(FormalLogicInterpretationError):
    pass
