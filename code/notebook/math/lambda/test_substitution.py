from .parsing import parse_term, parse_variable
from .substitution import Substitution, apply_substitution


def test_substitute_in_term() -> None:
    def t(term: str, **kwargs: str) -> str:
        return str(
            apply_substitution(
                parse_term(term),
                Substitution({ parse_variable(key): parse_term(value) for key, value in kwargs.items() })
            )
        )

    # Variables and applications
    assert t('x', x='y') == 'y'
    assert t('z', x='y') == 'z'
    assert t('(xy)', x='y') == '(yy)'

    # Multiple replacements in abstractions
    ## ex:def:lambda_substitution/simultaneous
    assert t('(λx.((xy)z))', x='a', y='b', z='c') == '(λx.((xb)c))'

    # Combinators should remain unchanged
    ## ex:def:lambda_substitution/nested_noop
    i = '(λx.x)'
    assert t(i, y='x') == i

    k = '(λx.(λy.(yx)))'
    assert t(k, y='x') == k

    # Renaming
    ## ex:def:lambda_substitution/capture
    assert t('(λx.(xy))', y='x') == '(λa.(ax))'
    ## ex:def:lambda_substitution/ignoring
    assert t('(λx.(xy))', y='z') == '(λx.(xz))'
