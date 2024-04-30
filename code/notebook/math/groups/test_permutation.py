import functools
import operator

from .cycle import Cycle
from .permutation import Permutation


def test_permutation_completion() -> None:
    domain = [1, 2, 3]
    p = Permutation.from_incomplete_mapping(domain, {2: 3})
    assert p.get_mapping() == {1: 1, 2: 3, 3: 2}


def test_cycle_to_permutation() -> None:
    domain = [1, 2, 3]
    p = Permutation.from_cycle(domain, Cycle([1, 2, 3]))
    assert p.get_mapping() == {1: 2, 2: 3, 3: 1}


def test_permutation_composition() -> None:
    domain = [1, 2, 3]
    p1 = Permutation.from_cycle(domain, Cycle([1, 2, 3]))
    p2 = Permutation.from_cycle(domain, Cycle([1, 3, 2]))
    res = Permutation.identity(domain)

    assert p1 @ p2 == res


def test_disjoint_permutation_composition() -> None:
    domain = [1, 2, 3]
    p1 = Permutation.from_cycle(domain, Cycle([1, 2]))
    p2 = Permutation.from_cycle(domain, Cycle([3, 4]))
    res = Permutation(domain, { 1: 2, 2: 1, 3: 4, 4: 3 })

    assert p1 @ p2 == res


def test_semidisjoint_permutation_composition() -> None:
    domain = [1, 2, 3]
    p1 = Permutation.from_cycle(domain, Cycle([1, 2]))
    p2 = Permutation.from_cycle(domain, Cycle([2, 3]))
    res = Permutation.from_cycle(domain, Cycle([1, 2, 3]))

    assert p1 @ p2 == res


def test_inverse_transposition() -> None:
    domain = [1, 2]
    transposition = Permutation.from_cycle(domain, Cycle([1, 2]))
    assert transposition.inverse() @ transposition == Permutation.identity(domain)
    assert transposition.inverse() == transposition


def test_inverse_permutation() -> None:
    domain = [1, 2, 3]
    p1 = Permutation.from_cycle(domain, Cycle([1, 2, 3]))
    p2 = Permutation.from_cycle(domain, Cycle([1, 3, 2]))
    res = Permutation.identity(domain)

    assert p1.inverse() == p2
    assert p1 @ p2 == res


def test_cycle_decomposition() -> None:
    domain = [1, 2, 3]
    cycle = Cycle([1, 2, 3])
    assert list(Permutation.from_cycle(domain, cycle).iter_decomposed()) == [cycle]


def test_complex_permutation_decomposition() -> None:
    src_cycles = [Cycle([1, 2]), Cycle([2, 3]), Cycle([3, 4]), Cycle([5, 6]), Cycle([7])]
    dest_cycles = [Cycle([1, 2, 3, 4]), Cycle([5, 6]), Cycle([7])]

    domain = [1, 2, 3, 4, 5, 6, 7]
    perm: Permutation[int] = functools.reduce(
        operator.matmul,
        (Permutation.from_cycle(domain, c) for c in src_cycles),
        Permutation.identity(domain)
    )

    assert list(perm.iter_decomposed()) == dest_cycles
