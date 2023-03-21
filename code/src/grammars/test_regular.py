from ..automata.finite import FiniteAutomaton

from .grammar import GrammarSchema, Grammar, NonTerminal
from .regular import is_regular, is_right_linear, to_finite_automaton, from_finite_automaton

from .conftest import assert_an


def test_to_finite_automaton_an(an: Grammar):
    assert is_regular(an)
    aut = to_finite_automaton(an)

    assert aut.recognize('')
    assert aut.recognize('a')
    assert aut.recognize('aaaaa')
    assert aut.recognize('aaaaaaaaaa')


def test_from_finite_automaton_an():
    aut: FiniteAutomaton = FiniteAutomaton()
    aut.add_transition(1, 'a', 1)
    aut.initial.add(1)
    aut.terminal.add(1)

    grammar = from_finite_automaton(aut)
    assert is_right_linear(grammar)
    assert_an(grammar)


def test_to_finite_automaton_complex():
    grammar = GrammarSchema.parse('''
        <S> → "a" "b" "c" <D>
        <D> → "d" <E> | ε
        <E> → "e" "f" <E> | ε
    ''').instantiate(NonTerminal('S'))
    aut = to_finite_automaton(grammar)

    assert is_regular(grammar)
    assert aut.recognize('abc')
    assert aut.recognize('abcd')
    assert aut.recognize('abcdef')
    assert aut.recognize('abcdefefef')
    assert not aut.recognize('abcdd')
    assert not aut.recognize('abcdee')
