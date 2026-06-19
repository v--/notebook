# ruff: file-ignore[multiple-spaces-after-operator]

from enum import StrEnum


class LogicalConstantName(StrEnum):
    VERUM =         'L⊤'
    FALSUM =        'L⊥'
    NEGATION =      'L¬'
    CONJUNCTION =   'L∧'
    DISJUNCTION =   'L∨'
    CONDITIONAL =   'L→'
    BICONDITIONAL = 'L↔'
    EQUALITY =      'L='
    FORALL =        'L∀'
    EXISTS =        'L∃'


class LogicalTypeName(StrEnum):
    PROP = 'ο'


class SortName(StrEnum):
    INDIVIDUAL = 'ι'
