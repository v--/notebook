from ..exceptions import FormalLogicError


class FormulaTransformationError(FormalLogicError):
    pass


class DisallowedFormulaError(FormulaTransformationError):
    pass


class VariableNameError(FormulaTransformationError):
    pass
