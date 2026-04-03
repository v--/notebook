# ruff: noqa: E222

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
