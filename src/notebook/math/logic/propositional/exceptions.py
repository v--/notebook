from ..exceptions import FormalLogicError


class PropositionalLogicError(FormalLogicError):
    pass


class PropositionalInterpretationError(PropositionalLogicError):
    pass


class MissingInterpretationError(PropositionalInterpretationError):
    pass


class NonPropositionalFormulaError(PropositionalLogicError):
    pass
