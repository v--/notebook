import itertools
from typing import TYPE_CHECKING

from notebook.math.graphs.graph import DirectedEdge, DirectedGraph
from notebook.math.lambda_.hol.expression import HolExpression
from notebook.math.lambda_.hol.theories.digraphs import DIRECTED_GRAPH_SIGNATURE, DirectedGraphStructure
from notebook.math.lambda_.parsing import parse_type, parse_typed_term

from .signature import hol_signature_to_fol
from .structure import hol_structure_to_fol


if TYPE_CHECKING:
    from notebook.math.lambda_.hol.signature import HolSignature
    from notebook.math.lambda_.hol.structure import HolStructure
    from notebook.math.logic.signature import FormalLogicSignature
    from notebook.math.logic.structure import FormalLogicStructure


def test_hol_expression_to_fol_digraph() -> None:
    expression = HolExpression(
        parse_typed_term('(L∀(λa:arc.((L=(src a))(dest a))))', DIRECTED_GRAPH_SIGNATURE),
        parse_type('ο', DIRECTED_GRAPH_SIGNATURE),
    )

    graph = DirectedGraph[int]()

    for i in range(3):
        graph.edges.add(i, i + 1)

    translated_signature = hol_signature_to_fol(DIRECTED_GRAPH_SIGNATURE, expression)
    hol_model = DirectedGraphStructure(graph)
    translated = hol_structure_to_fol(hol_model, expression)

    assert not translated.apply(translated_signature.get_predicate_symbol('?arc'), 0)
    assert translated.apply(translated_signature.get_function_symbol('src¹'), DirectedEdge(0, 1)) == 0
    assert translated.apply(translated_signature.get_function_symbol('dest¹'), DirectedEdge(0, 1)) == 1


def test_hol_structure_to_fol_z3(
    fol_z3_signature: FormalLogicSignature,
    fol_z3_model: FormalLogicStructure,
    hol_z3_signature: HolSignature,
    hol_z3_model: HolStructure,
) -> None:
    expression = HolExpression(
        parse_typed_term('(L∃(λx:ι.((+x)0)))', hol_z3_signature),
        parse_type('ι', hol_z3_signature),
    )

    translated_fol_model = hol_structure_to_fol(hol_z3_model, expression)
    translated_plus_sym = translated_fol_model.signature.get_function_symbol('+²')
    expected_plus_sym = fol_z3_signature.get_function_symbol('+')

    for a, b in itertools.product(fol_z3_model.universe, repeat=2):
        assert fol_z3_model.apply(expected_plus_sym, a, b) == translated_fol_model.apply(translated_plus_sym, a, b)
