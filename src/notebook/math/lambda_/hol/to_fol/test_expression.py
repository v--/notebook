from notebook.math.lambda_.hol import common
from notebook.math.lambda_.hol.expression import HolExpression
from notebook.math.lambda_.hol.theories.arithmetic import ARITHMETIC_SIGNATURE as HOL_ARITHMETIC_SIGNATURE
from notebook.math.lambda_.hol.theories.arithmetic import PEANO_INDUCTION_AXIOM as HOL_INDUCTION_AXIOM
from notebook.math.lambda_.hol.theories.digraphs import DIRECTED_GRAPH_SIGNATURE
from notebook.math.lambda_.parsing import parse_type, parse_typed_term
from notebook.math.logic.parsing import parse_formula
from notebook.math.logic.parsing import parse_term as parse_fol_term
from notebook.support.pytest import pytest_parametrize_kwargs

from .expression import hol_expression_to_fol
from .signature import hol_signature_to_fol


@pytest_parametrize_kwargs(
    dict(
        hol_term='L⊤',
        hol_type='ο',
        fol_expr='⊤',
    ),
    dict(
        hol_term='src',
        hol_type='(arc → vert)',
        fol_expr='src⁰',
    ),
    dict(
        hol='(L∀(λa:arc.((L=(src a))(dest a))))',
        hol_type='ο',
        fol_expr='∀a.(?arc(a) → (dest¹(a) = src¹(a)))',
    ),
    dict(
        hol_term='(L∀(λf:(arc → vert).(L∃(λa:arc.(L∃(λv:vert.((L=(fa))v)))))))',
        hol_type='ο',
        fol_expr='∀f.(?(arc → vert)(f) → ∃a.(?arc(a) ∧ ∃v.(?vert(v) ∧ (v = !(arc → vert)¹(f, a)))))',
    ),
)
def test_hol_expression_to_fol_digraph(hol_term: str, hol_type: str, fol_expr: str) -> None:
    expression = HolExpression(
        parse_typed_term(hol_term, DIRECTED_GRAPH_SIGNATURE),
        parse_type(hol_type, DIRECTED_GRAPH_SIGNATURE),
    )

    signature = hol_signature_to_fol(DIRECTED_GRAPH_SIGNATURE, expression)
    translated = hol_expression_to_fol(DIRECTED_GRAPH_SIGNATURE, expression)
    expected = (
        parse_formula(fol_expr, signature)
        if expression.type == common.prop
        else parse_fol_term(fol_expr, signature)
    )

    assert translated == expected


def test_induction_axiom_translation() -> None:
    actual = hol_expression_to_fol(HOL_ARITHMETIC_SIGNATURE, HOL_INDUCTION_AXIOM)
    signature = hol_signature_to_fol(HOL_ARITHMETIC_SIGNATURE, HOL_INDUCTION_AXIOM)
    expected = parse_formula(
        '∀p.(?(ι → ο)(p) → (∀n.(?ι(n) → !(ι → ο)¹(p, n)) → (∀n.(?ι(n) → (!(ι → ο)¹(p, S⁺¹(n)) → !(ι → ο)¹(p, n))) ∧ !(ι → ο)¹(p, 0⁰))))',
        signature,
    )

    assert actual == expected
