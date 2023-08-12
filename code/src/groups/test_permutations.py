import functools
import operator

from .cycles import Cycle
from .permutations import Permutation, Cycle


def test_permutation_completion():
    p = Permutation.from_incomplete_mapping({1: 1, 2: 3})
    assert p.mapping == {1: 1, 2: 3, 3: 2}


def test_cycle_to_permutation():
    empty = Permutation.from_cycle(Cycle([]))
    assert empty.mapping == {}

    p = Permutation.from_cycle(Cycle([1, 2, 3]))
    assert p.mapping == {1: 2, 2: 3, 3: 1}


def test_permutation_composition():
    p1 = Permutation.from_cycle(Cycle([1, 2, 3]))
    p2 = Permutation.from_cycle(Cycle([1, 3, 2]))
    res = Permutation.identity([1, 2, 3])

    assert p1 @ p2 == res


def test_disjoint_permutation_composition():
    p1 = Permutation.from_cycle(Cycle([1, 2]))
    p2 = Permutation.from_cycle(Cycle([3, 4]))
    res = Permutation({ 1: 2, 2: 1, 3: 4, 4: 3 })

    assert p1 @ p2 == res


def test_semidisjoint_permutation_composition():
    p1 = Permutation.from_cycle(Cycle([1, 2]))
    p2 = Permutation.from_cycle(Cycle([2, 3]))
    res = Permutation.from_cycle(Cycle([1, 2, 3]))

    assert p1 @ p2 == res


def test_inverse_transposition():
    transposition = Permutation.from_cycle(Cycle([1, 2]))
    assert transposition.inverse() @ transposition == Permutation.identity([1, 2])
    assert transposition.inverse() == transposition


def test_inverse_permutation():
    p1 = Permutation.from_cycle(Cycle([1, 2, 3]))
    p2 = Permutation.from_cycle(Cycle([1, 3, 2]))
    res = Permutation.identity(Cycle([1, 2, 3]))

    assert p1.inverse() == p2
    assert p1 @ p2 == res


def test_cycle_decomposition():
    cycle = Cycle([1, 2, 3])
    assert list(Permutation.from_cycle(cycle).iter_decomposed()) == [cycle]


def test_complex_permutation_decomposition():
    src_cycles = [Cycle([1, 2]), Cycle([2, 3]), Cycle([3, 4]), Cycle([5, 6]), Cycle([7])]
    dest_cycles = [Cycle([1, 2, 3, 4]), Cycle([5, 6]), Cycle([7])]

    perm = functools.reduce(
        operator.matmul,
        (Permutation.from_cycle(c) for c in src_cycles),
        Permutation.identity([])
    )

    assert list(perm.iter_decomposed()) == dest_cycles
