from collections.abc import Mapping, Sequence
from typing import Literal, get_args

from ....parsing import Token, map_of_str_enum_to_single_token
from ....support.inference import InferenceRuleConnective
from ....support.substitution import SubstitutionConnective
from ..alphabet import BinaryConnective, PropConstant, Quantifier, UnaryPrefix


LogicTokenKind = Literal[
    # Value-dependent
    'SIGNATURE_SYMBOL',
    'LATIN_IDENTIFIER',
    'GREEK_IDENTIFIER',
    'PROP_CONSTANT',
    'UNARY_CONNECTIVE',
    'BINARY_CONNECTIVE',
    'QUANTIFIER',
    'SUBSTITUTION_CONNECTIVE',

    # Singletons
    'COMMA',
    'DOT',
    'STAR',
    'EQUALITY',
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'LEFT_BRACKET',
    'RIGHT_BRACKET',
    'SUBSTITUTION_ARROW',
    'INFERENCE_RULE_SEQUENT',
]


TOKEN_KIND_LIST: Sequence[LogicTokenKind] = get_args(LogicTokenKind)
SINGLETON_TOKEN_MAP: Mapping[str, LogicTokenKind] = {
    ',': 'COMMA',
    '.': 'DOT',
    '*': 'STAR',
    '=': 'EQUALITY',
    '(': 'LEFT_PARENTHESIS',
    ')': 'RIGHT_PARENTHESIS',
    '[': 'LEFT_BRACKET',
    ']': 'RIGHT_BRACKET',
    InferenceRuleConnective.SEQUENT.value: 'INFERENCE_RULE_SEQUENT',
    **map_of_str_enum_to_single_token('PROP_CONSTANT', PropConstant),
    **map_of_str_enum_to_single_token('UNARY_CONNECTIVE', UnaryPrefix),
    **map_of_str_enum_to_single_token('BINARY_CONNECTIVE', BinaryConnective),
    **map_of_str_enum_to_single_token('QUANTIFIER', Quantifier),
    **map_of_str_enum_to_single_token('SUBSTITUTION_CONNECTIVE', SubstitutionConnective),
}

LogicToken = Token[LogicTokenKind]
