from ..fol.alphabet import BinaryConnective
from ..fol.formulas import ConnectiveFormula, Formula, is_conditional
from .rules import FormulaPlaceholder
from .schemas import is_schema_instance


def is_valid_derivation(axiom_schemas: set[FormulaPlaceholder], premises: set[Formula], derivation: list[Formula]) -> bool:  # noqa: PLR0911
    if len(derivation) == 0:
        return True

    *rest, conclusion = derivation

    if not is_valid_derivation(axiom_schemas, premises, rest):
        return False

    if conclusion in premises:
        return True

    if any(is_schema_instance(schema, conclusion) for schema in axiom_schemas):
        return True

    for premise in premises:
        if is_conditional(premise) and premise.b == conclusion and any(premise.a == derived for derived in rest):
            return True

    for derived in rest:
        if is_conditional(derived) and derived.b == conclusion and any(derived.a == past for past in rest):
            return True

    return False


def get_identity_derivation(formula: Formula) -> list[Formula]:
    """Axiomatic derivation of (P → P)"""
    goal = ConnectiveFormula(BinaryConnective.conditional, formula, formula)

    # The first two are axioms from the first schema
    a = ConnectiveFormula(BinaryConnective.conditional, formula, goal)
    b = ConnectiveFormula(BinaryConnective.conditional, formula, ConnectiveFormula(BinaryConnective.conditional, goal, formula))

    # This is an intermediate step obtained from axioms
    i = ConnectiveFormula(BinaryConnective.conditional, a, goal)

    # This is an axiom from the second schema
    c = ConnectiveFormula(BinaryConnective.conditional, b, i)

    return [a, b, c, i, goal]


def introduce_conclusion_hypothesis(axiom_schemas: set[FormulaPlaceholder], premises: set[Formula], derivation: list[Formula], hypothesis: Formula) -> list[Formula]:
    if len(derivation) == 0:
        return derivation

    *rest, conclusion = derivation

    goal = ConnectiveFormula(BinaryConnective.conditional, hypothesis, conclusion)

    if goal in premises or any(is_schema_instance(schema, goal) for schema in axiom_schemas):
        return [goal]

    if conclusion == hypothesis:
        return get_identity_derivation(conclusion)

    if conclusion in premises or any(is_schema_instance(schema, conclusion) for schema in axiom_schemas):
        return [
            ConnectiveFormula(BinaryConnective.conditional, conclusion, ConnectiveFormula(BinaryConnective.conditional, hypothesis, conclusion)),
            conclusion,
            goal
        ]

    for i, formula in enumerate(rest):  # noqa: B007
        if is_conditional(formula) and formula.b == conclusion:
            break
    else:
        return derivation

    j = rest.index(formula.a)
    rel_i = introduce_conclusion_hypothesis(axiom_schemas, premises, rest[:i + 1], hypothesis)
    rel_j = introduce_conclusion_hypothesis(axiom_schemas, premises, rest[:j + 1], hypothesis)

    dist = ConnectiveFormula(
        BinaryConnective.conditional,
        ConnectiveFormula(BinaryConnective.conditional, hypothesis, formula.a),
        ConnectiveFormula(BinaryConnective.conditional, hypothesis, formula.b)
    )

    return [
        *rel_i,
        ConnectiveFormula(BinaryConnective.conditional, rel_i[-1], dist),
        dist,
        *rel_j,
        goal
    ]
