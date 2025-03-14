from ...support.pytest import pytest_parametrize_kwargs
from .erasure import erase_annotations
from .parsing import parse_term
from .type_system import HOL_SIGNATURE
from .typing import TypingStyle


@pytest_parametrize_kwargs(
    dict(typed='Q',        untyped='Q'),
    dict(typed='x',        untyped='x'),
    dict(typed='(xy)',     untyped='(xy)'),
    dict(typed='(λx:ι.x)', untyped='(λx.x)'),
    dict(
        typed='(λx:o.(λy:ι.(xy)))',
        untyped='(λx.(λy.(xy)))'
    )
)
def test_erase_annotations(typed: str, untyped: str) -> None:
    typed_term = parse_term(HOL_SIGNATURE, typed, TypingStyle.EXPLICIT)
    untyped_term = parse_term(HOL_SIGNATURE, untyped, TypingStyle.IMPLICIT)
    assert erase_annotations(typed_term) == untyped_term
