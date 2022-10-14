from dataclasses import dataclass


@dataclass
class FOLToken:
    value: str

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object):
        return isinstance(other, type(self)) and self.value == other.value


class NaturalNumber(FOLToken):
    pass


class LatinName(FOLToken):
    pass


class GreekName(FOLToken):
    pass


class SingletonFOLToken(FOLToken):
    pass


left_parenthesis = SingletonFOLToken('(')
right_parenthesis = SingletonFOLToken(')')
comma = SingletonFOLToken(',')
dot = SingletonFOLToken('.')
space = SingletonFOLToken(' ')

equality = SingletonFOLToken('=')
negation = SingletonFOLToken('¬')

verum = SingletonFOLToken('⊤')
falsum = SingletonFOLToken('⊥')

PROP_CONSTANTS = [
    verum, falsum
]

join = SingletonFOLToken('∨')
meet = SingletonFOLToken('∧')
conditional = SingletonFOLToken('→')
biconditional = SingletonFOLToken('↔')

CONNECTIVES = [
    join, meet, conditional, biconditional
]

universal_quantifier = SingletonFOLToken('∀')
existential_quantifier = SingletonFOLToken('∃')

QUANTIFIERS = [
    universal_quantifier, existential_quantifier
]

LITERALS = [
    left_parenthesis,
    right_parenthesis,
    comma,
    dot,
    space,
    equality,
    negation,
    *PROP_CONSTANTS,
    *CONNECTIVES,
    *QUANTIFIERS
]
