from ..exceptions import FOLError


class AxiomaticDerivationError(FOLError):
    pass


class InvalidDerivationError(AxiomaticDerivationError):
    pass
