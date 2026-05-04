from textwrap import dedent
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .conftest import GrammarFixture


def test_an(an: GrammarFixture) -> None:
    schema = an.grammar.schema
    assert str(schema) == dedent("""\
        <S> → ε
        <S> → <A>
        <A> → <A> "a"
        <A> → "a"
        """,
        )
