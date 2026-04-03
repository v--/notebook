from typing import TYPE_CHECKING

from ...rings.modular import Z3
from ..parsing import parse_type, parse_typed_term, parse_variable_assertion
from ..type_context import TypeContext
from .abstraction_elimination import eliminate_abstractions
from .alphabet import SortName
from .expression import HolExpression
from .signature import SortSymbol
from .structure import HolVariableAssignment, evaluate_hol_expression


if TYPE_CHECKING:
    from .signature import HolSignature
    from .structure import HolStructure


def test_eliminate_abstractions_forall(hol_z3_signature: HolSignature) -> None:
    expression = HolExpression(
        parse_typed_term('(L∀(λx:ι.x))', hol_z3_signature),
        parse_type('(ι → ι)', hol_z3_signature),
    )

    translated = eliminate_abstractions(hol_z3_signature, expression)
    assert translated.expression == expression


def test_eliminate_abstractions_i(hol_z3_signature: HolSignature, hol_z3_model: HolStructure) -> None:
    expression = HolExpression(
        parse_typed_term('(λx:ι.x)', hol_z3_signature),
        parse_type('(ι → ι)', hol_z3_signature),
    )

    translated = eliminate_abstractions(hol_z3_signature, expression, hol_z3_model)
    assert translated.expression.term == parse_typed_term('Λ₁', translated.signature)
    assert translated.structure

    original_fun = evaluate_hol_expression(expression, hol_z3_model)
    assert callable(original_fun)

    translated_fun = evaluate_hol_expression(translated.expression, translated.structure)
    assert callable(translated_fun)

    for x in hol_z3_model.sort_universes[SortSymbol(SortName.INDIVIDUAL)]:
        assert original_fun(x) == translated_fun(x)


def test_eliminate_abstractions_lxy(hol_z3_signature: HolSignature, hol_z3_model: HolStructure) -> None:
    expression = HolExpression(
        parse_typed_term('(λx:(ι → ι).(xy))', hol_z3_signature),
        parse_type('((ι → ι) → ι)', hol_z3_signature),
        TypeContext.infer(y=parse_type('ι', hol_z3_signature)),
    )

    translated = eliminate_abstractions(hol_z3_signature, expression, hol_z3_model)
    assert translated.expression.term == parse_typed_term('(Λ₁y)', translated.signature)
    assert translated.structure

    assignment = HolVariableAssignment[Z3]({parse_variable_assertion('y: ι', hol_z3_signature): Z3(0)})

    original_fun = evaluate_hol_expression(expression, hol_z3_model, assignment)
    assert callable(original_fun)

    translated_fun = evaluate_hol_expression(translated.expression, translated.structure, assignment)
    assert callable(translated_fun)

    assert original_fun(lambda x: x) == translated_fun(lambda x: x)
