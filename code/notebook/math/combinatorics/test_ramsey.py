from .ramsey import RamseyNumberComputation, compute_ramsey_naive, ramsey_upper_bound


def test_ramsey_upper_bound() -> None:
    assert ramsey_upper_bound(1, 5) == 1
    assert ramsey_upper_bound(2, 5) == 5
    assert ramsey_upper_bound(3, 5) == 15
    assert ramsey_upper_bound(4, 5) == 35
    assert ramsey_upper_bound(5, 5) == 70

    assert ramsey_upper_bound(3, 3) == 6
    assert ramsey_upper_bound(3, 3, 3) == 21


def test_compute_ramsey_naive() -> None:
    assert compute_ramsey_naive(1, 3) == RamseyNumberComputation(result=1, subgraphs_traversed=0, args=[1, 3])
    assert compute_ramsey_naive(2, 3) == RamseyNumberComputation(result=3, subgraphs_traversed=2, args=[2, 3])
    assert compute_ramsey_naive(3, 3) == RamseyNumberComputation(result=6, subgraphs_traversed=1150, args=[3, 3])
