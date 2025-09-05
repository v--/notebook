from textwrap import dedent

from ..parsing import parse_type, parse_typed_term, parse_variable
from .type_inference import derive_type


def test_assumption() -> None:
    term = parse_typed_term('x')
    context = {parse_variable('x'): parse_type('τ')}
    assert str(derive_type(term, context)) == dedent('''\
        x: τ
        '''
    )


def test_arrow_elim() -> None:
    context = {
        parse_variable('x'): parse_type('(τ → τ)'),
        parse_variable('y'): parse_type('τ')
    }

    term = parse_typed_term('(xy)')
    assert str(derive_type(term, context)) == dedent('''\
        x: (τ → τ)      y: τ
        ______________________ →₋
               (xy): τ
        '''
    )


# ex:def:type_derivation_tree/i
def test_arrow_intro() -> None:
    term = parse_typed_term('(λx:τ.x)')
    assert str(derive_type(term)) == dedent('''\
               x: τ
        x _________________ →₊
          (λx:τ.x): (τ → τ)
        '''
    )


def test_nested_arrow_intro() -> None:
    term = parse_typed_term('(λx:τ.(λy:σ.x))')
    assert str(derive_type(term)) == dedent('''\
                     x: τ
                _________________ →₊
                (λy:σ.x): (σ → τ)
        x ______________________________ →₊
          (λx:τ.(λy:σ.x)): (τ → (σ → τ))
        '''
    )


# ex:def:type_derivation_tree/pairs
def test_cons() -> None:
    term = parse_typed_term('(λx:τ.(λy:σ.(λf:(τ→(σ→ρ)).((fx)y))))')

    assert str(derive_type(term)) == dedent('''\
                         f: (τ → (σ → ρ))      x: τ
                         ____________________________ →₋
                                (fx): (σ → ρ)               y: σ
                         _________________________________________ →₋
                                        ((fx)y): ρ
                    f _______________________________________________ →₊
                      (λf:(τ → (σ → ρ)).((fx)y)): ((τ → (σ → ρ)) → ρ)
              y ____________________________________________________________ →₊
                (λy:σ.(λf:(τ → (σ → ρ)).((fx)y))): (σ → ((τ → (σ → ρ)) → ρ))
        x _________________________________________________________________________ →₊
          (λx:τ.(λy:σ.(λf:(τ → (σ → ρ)).((fx)y)))): (τ → (σ → ((τ → (σ → ρ)) → ρ)))
        '''
    )
