from ...parsing import parse_type, parse_typed_term
from ..expression import HolExpression
from ..signature import PLAIN_HOL_SIGNATURE
from ..theories.digraphs import DIRECTED_GRAPH_SIGNATURE
from .signature import hol_signature_to_fol


def test_hol_signature_to_fol_plain() -> None:
    expression = HolExpression(
        parse_typed_term('(λx:ι.x)', PLAIN_HOL_SIGNATURE),
        parse_type('(ι → ι)', PLAIN_HOL_SIGNATURE),
    )

    signature = hol_signature_to_fol(PLAIN_HOL_SIGNATURE, expression)
    assert signature.get_predicate_symbol('?ι').arity == 1


def test_hol_signature_to_fol_digraph() -> None:
    expression = HolExpression(
        parse_typed_term('(L∀(λx:arc.((L=(src x))(dest x))))', DIRECTED_GRAPH_SIGNATURE),
        parse_type('ο', DIRECTED_GRAPH_SIGNATURE),
    )

    signature = hol_signature_to_fol(DIRECTED_GRAPH_SIGNATURE, expression)
    assert signature.get_predicate_symbol('?arc').arity == 1
    assert signature.get_function_symbol('src⁰').arity == 0
    assert signature.get_function_symbol('src¹').arity == 1
    assert signature.get_function_symbol('src⁰').arity == 0
    assert signature.get_function_symbol('src¹').arity == 1
