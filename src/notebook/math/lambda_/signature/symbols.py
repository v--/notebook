import abc
from dataclasses import dataclass
from typing import override

from ....parsing import is_greek_identifier, is_latin_identifier
from ....support.inference import ImproperInferenceRuleSymbol
from ....support.unicode import Capitalization
from ..alphabet import AuxImproperSymbol, BinaryTypeConnective, BinderSymbol
from .exceptions import LambdaSignatureError


@dataclass(unsafe_hash=True)
class BaseSignatureSymbol(abc.ABC):
    name: str

    def __init__(self, name: str) -> None:
        self.validate(name)
        self.name = name

    @abc.abstractmethod
    def validate(self, name: str) -> None:
        ...

    @abc.abstractmethod
    def get_kind_string(self) -> str:
        ...

    def __str__(self) -> str:
        return self.name


class ConstantTermSymbol(BaseSignatureSymbol):
    @override
    def validate(self, name: str) -> None:
        if name in BinderSymbol or name in AuxImproperSymbol or name in ImproperInferenceRuleSymbol:
            raise LambdaSignatureError(f'Cannot use the improper symbol {name} as a λ-term constant')

        if is_latin_identifier(name, Capitalization.SMALL):
            raise LambdaSignatureError(f'Cannot use {name} as a λ-term constant because that conflicts with the grammar of variables')

        if is_latin_identifier(name, Capitalization.CAPITAL):
            raise LambdaSignatureError(f'Cannot use {name} as a λ-term constant because that conflicts with the grammar of placeholders')

    @override
    def get_kind_string(self) -> str:
        return 'constant term'


class BaseTypeSymbol(BaseSignatureSymbol):
    @override
    def get_kind_string(self) -> str:
        return 'base type'

    @override
    def validate(self, name: str) -> None:
        if name in BinaryTypeConnective or name in AuxImproperSymbol or name in ImproperInferenceRuleSymbol:
            raise LambdaSignatureError(f'Cannot use the improper symbol {name} as a base type')

        if is_greek_identifier(name, Capitalization.SMALL):
            raise LambdaSignatureError(f'Cannot use {name} as a base type because that conflicts with the grammar of type variables')


SignatureSymbol = ConstantTermSymbol | BaseTypeSymbol
