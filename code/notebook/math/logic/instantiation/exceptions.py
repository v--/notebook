from ..exceptions import FormalLogicError


class InstantiationInferenceError(FormalLogicError):
    pass


class InsufficientInferenceDataError(InstantiationInferenceError):
    pass
