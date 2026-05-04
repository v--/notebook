from notebook.math.logic.exceptions import FormalLogicError


class PropositionalLogicError(FormalLogicError):
    pass


class NonPropositionalFormulaError(PropositionalLogicError):
    pass


class MissingInterpretationError(PropositionalLogicError):
    pass
