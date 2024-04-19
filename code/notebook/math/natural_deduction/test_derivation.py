from ..fol.parsing.parser import parse_formula
from ..fol.signature import FOLSignature
from .derivation import get_identity_derivation, introduce_conclusion_hypothesis, is_valid_derivation
from .rules import FormulaPlaceholder


def test_minimal_implicational_derivation_validity(propositional_signature: FOLSignature, implicational_axioms: set[FormulaPlaceholder]) -> None:
    def t(derivation: list[str], /, premises: set[str] = set()) -> bool:  # noqa: B006
        derivation_formulas = [parse_formula(propositional_signature, s) for s in derivation]
        premise_formulas = {parse_formula(propositional_signature, s) for s in premises}
        return is_valid_derivation(implicational_axioms, premise_formulas, derivation_formulas)

    assert t(['(p → (q → p))'])
    assert t(['(p → (p → p))'])

    assert not t(['p'])
    assert t(['p'], premises={'p'})

    assert is_valid_derivation(
        implicational_axioms,
        premises=set(),
        derivation=get_identity_derivation(parse_formula(propositional_signature, 'p'))
    )


def test_introduce_conclusion_hypothesis(propositional_signature: FOLSignature, implicational_axioms: set[FormulaPlaceholder]) -> None:
    def t(derivation: list[str], /, hypothesis: str, premises: set[str] = set()) -> list[str]:  # noqa: B006
        derivation_formulas = [parse_formula(propositional_signature, s) for s in derivation]
        premise_formulas = {parse_formula(propositional_signature, s) for s in premises}
        assert is_valid_derivation(implicational_axioms, premise_formulas, derivation_formulas)
        hypothesis_formula = parse_formula(propositional_signature, hypothesis)
        relativized = introduce_conclusion_hypothesis(implicational_axioms, premise_formulas, derivation_formulas, hypothesis_formula)
        assert is_valid_derivation(implicational_axioms, premise_formulas - {hypothesis_formula}, relativized)
        return [str(formula) for formula in relativized]

    assert t(['p'], premises={'p'}, hypothesis='p') == [
        str(formula) for formula in get_identity_derivation(parse_formula(propositional_signature, 'p'))
    ]

    assert t(['q'], premises={'q'}, hypothesis='p') == [
        '(q → (p → q))',
        'q',
        '(p → q)'
    ]

    assert t(['p', '(p → q)', 'q'], premises={'p', '(p → q)'}, hypothesis='p') == ['(p → q)']
    assert t(['(p → q)', 'p', 'q'], premises={'p', '(p → q)'}, hypothesis='p') == ['(p → q)']

    assert t(['(p → q)', '(q → r)', 'p', 'q', 'r'], premises={'(p → q)', '(q → r)', 'p'}, hypothesis='p') == [
        '((q → r) → (p → (q → r)))',
        '(q → r)',
        '(p → (q → r))',
        '((p → (q → r)) → ((p → q) → (p → r)))',
        '((p → q) → (p → r))',
        '(p → q)',
        '(p → r)'
    ]

    assert t(['(p → (q → r))', 'p', '(q → r)', 'q', 'r'], premises={'(p → (q → r))', 'p', 'q'}, hypothesis='p') == [
        '(p → (q → r))',
        '((p → (q → r)) → ((p → q) → (p → r)))',
        '((p → q) → (p → r))',
        '(q → (p → q))',
        'q',
        '(p → q)',
        '(p → r)'
    ]
