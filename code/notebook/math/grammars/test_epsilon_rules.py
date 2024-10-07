from textwrap import dedent

from .alphabet import NonTerminal
from .brute_force_parse import derives
from .conftest import GrammarFixture
from .epsilon_rules import (
    is_epsilon_free,
    is_essentially_epsilon_free,
    remove_epsilon_rules,
)
from .parsing import parse_grammar_schema


# See ex:alg:epsilon_rule_removal/an in the monograph
def test_remove_epsilon_rules_simple(an: GrammarFixture) -> None:
    grammar = parse_grammar_schema(
        dedent('''\
            <S> → ε | "a" <S>
            '''
        )
    ).instantiate(NonTerminal('S'))

    an.assert_equivalent(grammar)
    assert not is_essentially_epsilon_free(grammar)

    new_grammar = remove_epsilon_rules(grammar)

    assert is_essentially_epsilon_free(new_grammar)
    an.assert_equivalent(new_grammar)


# See ex:alg:epsilon_rule_removal/dead in the monograph
def test_remove_epsilon_rules_terminal_rule() -> None:
    grammar = parse_grammar_schema(
        dedent('''\
            <S> → <A> <B>
            <A> → ε | "a"
            <B> → ε
            '''
        )
    ).instantiate(NonTerminal('S'))

    assert derives(grammar, '')
    assert derives(grammar, 'a')

    assert not is_essentially_epsilon_free(grammar)

    new_grammar = remove_epsilon_rules(grammar)

    assert derives(new_grammar, '')
    assert derives(new_grammar, 'a')

    assert is_essentially_epsilon_free(new_grammar)

    # Verify that there are "dead" rules
    assert len(list(new_grammar.schema.instantiate(NonTerminal('B')).iter_starting_rules())) == 0


# See ex:alg:epsilon_rule_removal/natural in the monograph
def test_remove_epsilon_rules_natural(binary: GrammarFixture) -> None:
    grammar = parse_grammar_schema(
        dedent('''\
            <N> → "0" | "1" <B>
            <B> → ε | "0" <B> | "1" <B>
            '''
        )
    ).instantiate(NonTerminal('N'))

    binary.assert_equivalent(grammar)
    assert not is_essentially_epsilon_free(grammar)

    new_grammar = remove_epsilon_rules(grammar)

    assert is_essentially_epsilon_free(new_grammar)
    assert is_epsilon_free(new_grammar)
    binary.assert_equivalent(new_grammar)
