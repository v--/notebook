from collections.abc import Mapping, Sequence
from typing import Literal, get_args

from ....parsing import Token, map_of_str_enum_to_single_token, map_of_str_enum_to_tokens
from ....support.inference import ImproperInferenceRuleSymbol
from ..alphabet import AuxImproperSymbol, BinaryTypeConnective, BinderSymbol


LambdaTokenKind = Literal[
    # Value-dependent
    'SIGNATURE_SYMBOL',
    'SMALL_LATIN_IDENTIFIER',
    'CAPITAL_LATIN_IDENTIFIER',
    'SMALL_GREEK_IDENTIFIER',
    'BINARY_TYPE_CONNECTIVE',

    # Singletons
    'LAMBDA',
    'DOT',
    'COLON',
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'LEFT_BRACKET',
    'RIGHT_BRACKET',
    'PLACEHOLDER',

    'COMMA',
    'RULE_SEQUENT',
]


TOKEN_KIND_LIST: Sequence[LambdaTokenKind] = get_args(LambdaTokenKind)

SINGLETON_TOKEN_MAP: Mapping[str, LambdaTokenKind] = {
    ImproperInferenceRuleSymbol.SEQUENT.value: 'RULE_SEQUENT',
    ImproperInferenceRuleSymbol.COMMA.value: 'COMMA',
    **map_of_str_enum_to_tokens(TOKEN_KIND_LIST, BinderSymbol),
    **map_of_str_enum_to_tokens(TOKEN_KIND_LIST, AuxImproperSymbol),
    **map_of_str_enum_to_single_token('BINARY_TYPE_CONNECTIVE', BinaryTypeConnective),
}

LambdaToken = Token[LambdaTokenKind]
