from .titles import Titles, split_title


def test_split_title() -> None:
    assert split_title('A: B') == Titles('A', 'B')
    assert split_title('A: B: C') == Titles('A', 'B: C')
    assert split_title('A. B') == Titles('A', 'B')
    assert split_title('A: B. C') == Titles('A', 'B. C')
    assert split_title('A - B') == Titles('A', 'B')
    assert split_title('A -- B') == Titles('A', 'B')
    assert split_title('A --- B') == Titles('A', 'B')
    assert split_title('A-B C') == Titles('A-B C', None)
