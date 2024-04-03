from .parsing.parser import parse_term
from .substitution import substitute_in_term
from .terms import Variable


def test_substitute_in_term() -> None:
    def t(term: str, var: str, replacement: str) -> str:
        parsed_var = parse_term(var)
        assert isinstance(parsed_var, Variable)

        return str(
            substitute_in_term(
                parse_term(term),
                parsed_var,
                parse_term(replacement)
            )
        )

    # Verify all substitution rules in order
    assert t('x', 'x', 'y') == 'y'
    assert t('z', 'x', 'y') == 'z'
    assert t('(xy)', 'x', 'y') == '(yy)'
    assert t('(λx.(yz))', 'x', 'y') == '(λx.(yz))'
    assert t('(λy.(λx.(yz)))', 'x', 'y') == '(λy.(λx.(yz)))'
    assert t('(λx.(yz))', 'y', 'z') == '(λx.(zz))'
    assert t('(λx.(yz))', 'y', 'x') == '(λx₀.(xz))'
