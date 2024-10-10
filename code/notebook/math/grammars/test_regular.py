from textwrap import dedent

from ..automata.finite import FiniteAutomaton
from .alphabet import NonTerminal
from .conftest import GrammarFixture
from .parsing import parse_grammar_schema
from .regular import (
    from_finite_automaton,
    is_regular,
    is_right_linear,
    to_finite_automaton,
)


def test_to_finite_automaton_an(an: GrammarFixture) -> None:
    assert is_regular(an.grammar)
    aut = to_finite_automaton(an.grammar)

    for string in an.whitelist:
        assert aut.recognize(string)

    for string in an.blacklist:
        assert not aut.recognize(string)


def test_from_finite_automaton_an(an: GrammarFixture) -> None:
    aut: FiniteAutomaton = FiniteAutomaton()
    aut.add_transition(src=1, dest=1, symbol='a')
    aut.initial.add(1)
    aut.terminal.add(1)

    grammar = from_finite_automaton(aut)
    assert is_right_linear(grammar)
    an.assert_equivalent(grammar)


def test_to_finite_automaton_complex() -> None:
    grammar = parse_grammar_schema(
        dedent('''\
            <S> → "a" "b" "c" <D>
            <D> → "d" <E> | ε
            <E> → "e" "f" <E> | ε
            '''
        )
    ).instantiate(NonTerminal('S'))

    aut = to_finite_automaton(grammar)

    assert is_regular(grammar)
    assert aut.recognize('abc')
    assert aut.recognize('abcd')
    assert aut.recognize('abcdef')
    assert aut.recognize('abcdefefef')
    assert not aut.recognize('abcdd')
    assert not aut.recognize('abcdee')
