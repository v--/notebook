from abc import ABC, abstractmethod
from enum import Flag, auto

from .tokens import TokenMixin


class Capitalization(Flag):
    small = auto()
    capital = auto()
    mixed = capital | small



class AlphabeticIdentifier(TokenMixin, ABC):
    capitalization: Capitalization
    short: bool

    def __init__(self, value: str, capitalization: Capitalization = Capitalization.mixed, *, short: bool = False) -> None:
        super().__init__(value)
        self.capitalization = capitalization
        self.short = short

    @classmethod
    @abstractmethod
    def is_capital_letter(cls, sym: str) -> bool:
        ...

    @classmethod
    @abstractmethod
    def is_small_letter(cls, sym: str) -> bool:
        ...


class LatinIdentifier(AlphabeticIdentifier):
    @classmethod
    def is_capital_letter(cls, sym: str) -> bool:
        return 'A' <= sym <= 'Z'

    @classmethod
    def is_small_letter(cls, sym: str) -> bool:
        return 'a' <= sym <= 'z'


class GreekIdentifier(AlphabeticIdentifier):
    @classmethod
    def is_capital_letter(cls, sym: str) -> bool:
        return 'Α' <= sym <= 'Ω'

    @classmethod
    def is_small_letter(cls, sym: str) -> bool:
        return 'α' <= sym <= 'ω'
