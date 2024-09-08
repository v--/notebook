from ...parsing.whitespace import Whitespace
from .token_sequence import TokenSequence


def test_split_by_whitespace(quick_fox: TokenSequence) -> None:
    splits = list(quick_fox.split_by(lambda token: isinstance(token, Whitespace)))
    assert splits == [TokenSequence([token]) for token in quick_fox if not isinstance(token, Whitespace)]


def test_split_by_the(quick_fox: TokenSequence) -> None:
    splits = [str(s) for s in quick_fox.split_by(lambda token: str(token).lower() == 'the')]
    assert splits == ['quick brown fox jumps over', 'lazy dog']
