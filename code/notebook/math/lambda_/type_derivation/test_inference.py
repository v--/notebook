from textwrap import dedent

from ..parsing import parse_term
from ..signature import LambdaSignature
from ..typing import TypingStyle
from .inference import derive_type


# ex:def:type_derivation_tree/i
def test_arrow_intro(dummy_signature: LambdaSignature) -> None:
    term = parse_term(dummy_signature, '(λx:α.x)', TypingStyle.explicit)
    assert str(derive_type(term)) == dedent('''\
               x: α
        x _________________ →⁺
          (λx:α.x): (α → α)
        '''
    )


def test_nested_arrow_intro(dummy_signature: LambdaSignature) -> None:
    term = parse_term(dummy_signature, '(λx:α.(λy:β.x))', TypingStyle.explicit)
    assert str(derive_type(term)) == dedent('''\
                     x: α
                _________________ →⁺
                (λy:β.x): (β → α)
        x ______________________________ →⁺
          (λx:α.(λy:β.x)): (α → (β → α))
        '''
    )


# ex:def:type_derivation_tree/pairs
def test_cons(dummy_signature: LambdaSignature) -> None:
    term = parse_term(dummy_signature, '(λx:α.(λy:β.(λf:(α→(β→γ)).((fx)y))))', TypingStyle.explicit)
    assert str(derive_type(term)) == dedent('''\
                         f: (α → (β → γ))      x: α
                         ____________________________ →⁻
                                (fx): (β → γ)               y: β
                         _________________________________________ →⁻
                                        ((fx)y): γ
                    f _______________________________________________ →⁺
                      (λf:(α → (β → γ)).((fx)y)): ((α → (β → γ)) → γ)
              y ____________________________________________________________ →⁺
                (λy:β.(λf:(α → (β → γ)).((fx)y))): (β → ((α → (β → γ)) → γ))
        x _________________________________________________________________________ →⁺
          (λx:α.(λy:β.(λf:(α → (β → γ)).((fx)y)))): (α → (β → ((α → (β → γ)) → γ)))
        '''
    )
