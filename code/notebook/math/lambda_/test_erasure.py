from ...support.pytest import pytest_parametrize_kwargs
from .erasure import erase_annotations
from .parsing import parse_typed_term, parse_untyped_term


@pytest_parametrize_kwargs(
    dict(typed='x',        untyped='x'),
    dict(typed='(xy)',     untyped='(xy)'),
    dict(typed='(λx:τ.x)', untyped='(λx.x)'),
    dict(
        typed='(λx:σ.(λy:τ.(xy)))',
        untyped='(λx.(λy.(xy)))'
    )
)
def test_erase_annotations(typed: str, untyped: str) -> None:
    typed_term = parse_typed_term(typed)
    untyped_term = parse_untyped_term(untyped)
    assert erase_annotations(typed_term) == untyped_term
