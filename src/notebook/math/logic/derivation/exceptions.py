from ..exceptions import FormalLogicError


class AxiomaticDerivationError(FormalLogicError):
    pass


class InvalidDerivationError(AxiomaticDerivationError):
    pass
