from collections.abc import Callable

from .cnf import function_to_cnf, is_formula_in_cnf, pull_conjunction, to_cnf
from .parsing import parse_formula
from .signature import FOLSignature


def test_is_formula_in_cnf(propositional_signature: FOLSignature) -> None:
    def t(string: str) -> bool:
        return is_formula_in_cnf(parse_formula(propositional_signature, string))

    assert t('p')
    assert t('(p ∧ q)')
    assert t('(p ∧ (q ∨ r))')

    assert not t('(p ∨ (q ∧ r))')
    assert not t('∀ξ.p')


def test_pull_conjunction(propositional_signature: FOLSignature) -> None:
    def t(string: str) -> str:
        return str(pull_conjunction(parse_formula(propositional_signature, string)))

    # Trivial cases
    assert t('p') == 'p'
    assert t('(p ∧ q)') == '(p ∧ q)'
    assert t('(p ∨ q)') == '(p ∨ q)'

    # Base cases
    assert t('(p ∨ (q ∧ r))') == '((p ∨ q) ∧ (p ∨ r))'
    assert t('((p ∧ q) ∨ r)') == '((p ∨ r) ∧ (q ∨ r))'

    # Test pulling out nested conjunctions
    assert t('((p ∧ q) ∨ (r ∧ s))') == '(((p ∨ r) ∧ (p ∨ s)) ∧ ((q ∨ r) ∧ (q ∨ s)))'
    assert t('(p ∧ (q ∨ (r ∧ s)))') == '(p ∧ ((q ∨ r) ∧ (q ∨ s)))'
    assert t('(p ∨ (q ∨ (r ∧ s)))') == '((p ∨ (q ∨ r)) ∧ (p ∨ (q ∨ s)))'
    assert t('(p ∨ (q ∧ (r ∧ s)))') == '((p ∨ q) ∧ ((p ∨ r) ∧ (p ∨ s)))'
    assert t('(p ∨ (q ∨ (r ∨ (s ∧ t))))') == '((p ∨ (q ∨ (r ∨ s))) ∧ (p ∨ (q ∨ (r ∨ t))))'

    # Other connectives are allowed, but we will stop once we reach them
    assert t('(p ∨ (q → (r ∧ s)))') == '(p ∨ (q → (r ∧ s)))'


def test_to_cnf(propositional_signature: FOLSignature) -> None:
    def t(string: str) -> str:
        cnf = to_cnf(parse_formula(propositional_signature, string))
        # assert is_formula_in_cnf(cnf)
        return str(cnf)

    assert t('p') == 'p'

    assert t('⊤') == '(p ∨ ¬p)'
    assert t('⊥') == '(p ∧ ¬p)'

    assert t('(p ∨ q)') == '(p ∨ q)'
    assert t('(p ∧ q)') == '(p ∧ q)'
    assert t('(p → q)') == '(¬p ∨ q)'
    assert t('(p ↔ q)') == '((¬p ∨ q) ∧ (p ∨ ¬q))'

    assert t('¬(p ∧ q)') == '(¬p ∨ ¬q)'
    assert t('¬(p ∨ q)') == '(¬p ∧ ¬q)'
    assert t('¬(p → q)') == '(p ∧ ¬q)'

    assert t('(p ∧ (q ∨ r))') == '(p ∧ (q ∨ r))'
    assert t('¬(p ∨ ¬(q ∨ r))') == '(¬p ∧ (q ∨ r))'
    assert t('¬(p ∧ ¬(q ∧ r))') == '((¬p ∨ q) ∧ (¬p ∨ r))'
    assert t('(p ∨ ¬(p ∧ ¬(q ∧ r)))') == '((p ∨ (¬p ∨ q)) ∧ (p ∨ (¬p ∨ r)))'


def test_function_to_cnf() -> None:
    def t(fun: Callable[..., bool]) -> str:
        return str(function_to_cnf(fun))

    assert t(lambda: True) == '(p ∨ ¬p)'
    assert t(lambda: False) == '(p ∧ ¬p)'
    assert t(lambda a, b: True) == '(a ∨ ¬a)'  # noqa: ARG005
    assert t(lambda a, b: a or b) == '(a ∨ b)'
    assert t(lambda a, b: a) == '((a ∨ b) ∧ (a ∨ ¬b))'  # noqa: ARG005
    assert t(lambda a, b: a and b) == '(((a ∨ b) ∧ (a ∨ ¬b)) ∧ (¬a ∨ b))'
    assert t(lambda a, b: False) == '((((a ∨ b) ∧ (a ∨ ¬b)) ∧ (¬a ∨ b)) ∧ (¬a ∨ ¬b))'  # noqa: ARG005
