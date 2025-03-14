from collections.abc import Mapping, Sequence
from typing import Literal, get_args

from ....parsing import Token, map_of_str_enum_to_single_token
from ....support.inference import InferenceRuleConnective
from ..alphabet import BinaryConnective, PropConstant, Quantifier, SchemaConnective, UnaryConnective


LogicTokenKind = Literal[
    # Value-dependent
    'SIGNATURE_SYMBOL',
    'LATIN_IDENTIFIER',
    'GREEK_IDENTIFIER',
    'PROP_CONSTANT',
    'UNARY_CONNECTIVE',
    'BINARY_CONNECTIVE',
    'QUANTIFIER',

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
    SchemaConnective.SUBSTITUTION.value: 'SUBSTITUTION_ARROW',
    InferenceRuleConnective.SEQUENT.value: 'INFERENCE_RULE_SEQUENT',
    **map_of_str_enum_to_single_token('PROP_CONSTANT', PropConstant),
    **map_of_str_enum_to_single_token('UNARY_CONNECTIVE', UnaryConnective),
    **map_of_str_enum_to_single_token('BINARY_CONNECTIVE', BinaryConnective),
    **map_of_str_enum_to_single_token('QUANTIFIER', Quantifier),
}

LogicToken = Token[LogicTokenKind]
