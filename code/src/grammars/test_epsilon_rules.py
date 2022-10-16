from ..support.parsing import ParserError

from .epsilon_rules import remove_epsilon_rules, is_epsilon_free, is_essentially_epsilon_free
from .brute_force_parse import parse
from .fixtures import *


def test_remove_epsilon_rules_simple():
    grammar = GrammarSchema.parse('''
        <S> → ε | "a" <S>
    ''').instantiate(NonTerminal('S'))

    assert_an(grammar)
    assert not is_essentially_epsilon_free(grammar)

    new_grammar = remove_epsilon_rules(grammar)

    assert is_essentially_epsilon_free(new_grammar)
    assert_an(new_grammar)


def test_remove_epsilon_rules_terminal_rule():
    grammar = GrammarSchema.parse('''
        <S> → <A> <B>
        <A> → ε | "a"
        <B> → ε
    ''').instantiate(NonTerminal('S'))

    assert derives(grammar, '')
    assert derives(grammar, 'a')

    assert not is_essentially_epsilon_free(grammar)

    new_grammar = remove_epsilon_rules(grammar)

    assert derives(new_grammar, '')
    assert derives(new_grammar, 'a')

    assert is_essentially_epsilon_free(new_grammar)

    # Verify that there are "dead" rules
    assert len(list(new_grammar.schema.instantiate(NonTerminal('B')).iter_starting_rules())) == 0


def test_remove_epsilon_rules_natural():
    grammar = GrammarSchema.parse('''
        <N> → "0" | "1" <B>
        <B> → ε | "0" <B> | "1" <B>
    ''').instantiate(NonTerminal('N'))

    assert_binary(grammar)
    assert not is_essentially_epsilon_free(grammar)

    new_grammar = remove_epsilon_rules(grammar)

    assert is_essentially_epsilon_free(new_grammar)
    assert is_epsilon_free(new_grammar)
    assert_binary(new_grammar)
