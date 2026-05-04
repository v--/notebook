from notebook.math.logic.exceptions import FormalLogicError


class AxiomaticDerivationError(FormalLogicError):
    pass


class InvalidDerivationError(AxiomaticDerivationError):
    pass
