from textwrap import dedent

from ..parsing import parse_term, parse_type, parse_variable
from ..signature import LambdaSignature
from ..typing import TypingStyle
from .inference import derive_type


def test_assumption(dummy_signature: LambdaSignature) -> None:
    term = parse_term(dummy_signature, 'x', TypingStyle.explicit)
    context = {parse_variable('x'): parse_type(dummy_signature, 'τ')}
    assert str(derive_type(term, context)) == dedent('''\
        x: τ
        '''
    )


def test_arrow_elim(dummy_signature: LambdaSignature) -> None:
    context = {
        parse_variable('x'): parse_type(dummy_signature, '(τ → τ)'),
        parse_variable('y'): parse_type(dummy_signature, 'τ')
    }

    term = parse_term(dummy_signature, '(xy)', TypingStyle.explicit)
    assert str(derive_type(term, context)) == dedent('''\
        x: (τ → τ)      y: τ
        ______________________ →⁻
               (xy): τ
        '''
    )


# ex:def:type_derivation_tree/i
def test_arrow_intro(dummy_signature: LambdaSignature) -> None:
    term = parse_term(dummy_signature, '(λx:τ.x)', TypingStyle.explicit)
    assert str(derive_type(term)) == dedent('''\
               x: τ
        x _________________ →⁺
          (λx:τ.x): (τ → τ)
        '''
    )


def test_nested_arrow_intro(dummy_signature: LambdaSignature) -> None:
    term = parse_term(dummy_signature, '(λx:τ.(λy:σ.x))', TypingStyle.explicit)
    assert str(derive_type(term)) == dedent('''\
                     x: τ
                _________________ →⁺
                (λy:σ.x): (σ → τ)
        x ______________________________ →⁺
          (λx:τ.(λy:σ.x)): (τ → (σ → τ))
        '''
    )


# ex:def:type_derivation_tree/pairs
def test_cons(dummy_signature: LambdaSignature) -> None:
    term = parse_term(dummy_signature, '(λx:τ.(λy:σ.(λf:(τ→(σ→ρ)).((fx)y))))', TypingStyle.explicit)
    assert str(derive_type(term)) == dedent('''\
                       f: (τ → (σ → ρ))      x: τ
                       ____________________________ →⁻
                              (fx): (σ → ρ)               y: σ
                       _________________________________________ →⁻
                                      ((fx)y): ρ
                    _______________________________________________ →⁺
                    (λf:(τ → (σ → ρ)).((fx)y)): ((τ → (σ → ρ)) → ρ)
              ____________________________________________________________ →⁺
              (λy:σ.(λf:(τ → (σ → ρ)).((fx)y))): (σ → ((τ → (σ → ρ)) → ρ))
        _________________________________________________________________________ →⁺
        (λx:τ.(λy:σ.(λf:(τ → (σ → ρ)).((fx)y)))): (τ → (σ → ((τ → (σ → ρ)) → ρ)))
        '''
    )
