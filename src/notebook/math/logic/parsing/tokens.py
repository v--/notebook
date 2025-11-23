from collections.abc import Mapping, Sequence
from typing import Literal, get_args

from ....parsing import Token, map_of_str_enum_to_single_token, map_of_str_enum_to_tokens
from ....support.inference import ImproperInferenceRuleSymbol
from ....support.substitution import ImproperSubstitutionSymbol
from ..alphabet import AuxImproperSymbol, BinaryConnective, EqualitySymbol, PropConstant, Quantifier, UnaryPrefix


LogicTokenKind = Literal[
    # Value-dependent
    'SIGNATURE_SYMBOL',
    'LATIN_IDENTIFIER',
    'GREEK_IDENTIFIER',

    # Singletons
    'PROP_CONSTANT',
    'UNARY_CONNECTIVE',
    'BINARY_CONNECTIVE',
    'QUANTIFIER',

    'EQUALITY',

    'DOT',
    'COMMA',
    'ASTERISK',
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'LEFT_BRACKET',
    'RIGHT_BRACKET',

    'RULE_SEQUENT',
    'SUBSTITUTION_CONNECTIVE',
]


TOKEN_KIND_LIST: Sequence[LogicTokenKind] = get_args(LogicTokenKind)

# It is important here that the same tokens have the same name everywhere they occur
SINGLETON_TOKEN_MAP: Mapping[str, LogicTokenKind] = {
    ImproperInferenceRuleSymbol.SEQUENT.value: 'RULE_SEQUENT',
    ImproperSubstitutionSymbol.CONNECTIVE.value: 'SUBSTITUTION_CONNECTIVE',
    **map_of_str_enum_to_tokens(TOKEN_KIND_LIST, EqualitySymbol),
    **map_of_str_enum_to_tokens(TOKEN_KIND_LIST, AuxImproperSymbol),
    **map_of_str_enum_to_single_token('PROP_CONSTANT', PropConstant),
    **map_of_str_enum_to_single_token('UNARY_CONNECTIVE', UnaryPrefix),
    **map_of_str_enum_to_single_token('BINARY_CONNECTIVE', BinaryConnective),
    **map_of_str_enum_to_single_token('QUANTIFIER', Quantifier),
}

LogicToken = Token[LogicTokenKind]
