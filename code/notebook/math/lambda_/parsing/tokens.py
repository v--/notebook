from collections.abc import Mapping, Sequence
from typing import Literal, get_args

from ....parsing import Token, map_of_str_enum_to_single_token
from ....support.inference import InferenceRuleConnective
from ..alphabet import BinaryTypeConnective, ImproperTermSymbol


LambdaTokenKind = Literal[
    # Value-dependent
    'SIGNATURE_SYMBOL',
    'LATIN_IDENTIFIER',
    'GREEK_IDENTIFIER',
    'BINARY_TYPE_CONNECTIVE',

    # Singletons
    'COMMA',
    'DOT',
    'EQUALITY',
    'COLON',
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'LEFT_BRACKET',
    'RIGHT_BRACKET',
    'LAMBDA',
    'INFERENCE_RULE_SEQUENT',
]


TOKEN_KIND_LIST: Sequence[LambdaTokenKind] = get_args(LambdaTokenKind)
SINGLETON_TOKEN_MAP: Mapping[str, LambdaTokenKind] = {
    ',': 'COMMA',
    '.': 'DOT',
    ':': 'COLON',
    '=': 'EQUALITY',
    '(': 'LEFT_PARENTHESIS',
    ')': 'RIGHT_PARENTHESIS',
    '[': 'LEFT_BRACKET',
    ']': 'RIGHT_BRACKET',
    ImproperTermSymbol.LAMBDA.value: 'LAMBDA',
    InferenceRuleConnective.SEQUENT.value: 'INFERENCE_RULE_SEQUENT',
    **map_of_str_enum_to_single_token('BINARY_TYPE_CONNECTIVE', BinaryTypeConnective),
}

LambdaToken = Token[LambdaTokenKind]
