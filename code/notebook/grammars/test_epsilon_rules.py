from .alphabet import NonTerminal
from .brute_force_parse import derives
from .conftest import assert_an, assert_binary
from .epsilon_rules import (
    is_epsilon_free,
    is_essentially_epsilon_free,
    remove_epsilon_rules,
)
from .parsing.parser import parse_grammar_schema


# See ex:alg:epsilon_rule_removal/an in the text
def test_remove_epsilon_rules_simple():
    grammar = parse_grammar_schema('''
        <S> → ε | "a" <S>
    ''').instantiate(NonTerminal('S'))

    assert_an(grammar)
    assert not is_essentially_epsilon_free(grammar)

    new_grammar = remove_epsilon_rules(grammar)

    assert is_essentially_epsilon_free(new_grammar)
    assert_an(new_grammar)


# See ex:alg:epsilon_rule_removal/dead in the text
def test_remove_epsilon_rules_terminal_rule():
    grammar = parse_grammar_schema('''
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


# See ex:alg:epsilon_rule_removal/natural in the text
def test_remove_epsilon_rules_natural():
    grammar = parse_grammar_schema('''
        <N> → "0" | "1" <B>
        <B> → ε | "0" <B> | "1" <B>
    ''').instantiate(NonTerminal('N'))

    assert_binary(grammar)
    assert not is_essentially_epsilon_free(grammar)

    new_grammar = remove_epsilon_rules(grammar)

    assert is_essentially_epsilon_free(new_grammar)
    assert is_epsilon_free(new_grammar)
    assert_binary(new_grammar)
