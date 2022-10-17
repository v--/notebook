from .renaming_rules import has_renaming_rules, collapse_renaming_rules
from .fixtures import *


def test_collapse_renaming_rules_simple():
    grammar = GrammarSchema.parse('''
        <S> → <A>
        <A> → "a"
    ''').instantiate(NonTerminal('S'))

    assert derives(grammar, 'a')
    assert not derives(grammar, '')
    assert not derives(grammar, 'aa')
    assert has_renaming_rules(grammar)

    new_grammar = collapse_renaming_rules(grammar)

    assert derives(grammar, 'a')
    assert not derives(grammar, '')
    assert not derives(grammar, 'aa')
    assert not has_renaming_rules(new_grammar)


def test_collapse_renaming_rules_cyclic():
    grammar = GrammarSchema.parse('''
        <S> → <A>
        <A> → "a" | <S>
    ''').instantiate(NonTerminal('S'))

    assert has_renaming_rules(grammar)
    new_grammar = collapse_renaming_rules(grammar)
    assert not has_renaming_rules(new_grammar)


def test_collapse_renaming_rules_complex():
    grammar = GrammarSchema.parse('''
        <S> → <A> | <C> | <E>
        <A> → <B>
        <B> → "c"
        <B> → <C>
        <C> → "d"
        <E> → "e"
    ''').instantiate(NonTerminal('S'))

    assert derives(grammar, 'c')
    assert derives(grammar, 'd')
    assert derives(grammar, 'e')
    assert not derives(grammar, '')
    assert has_renaming_rules(grammar)

    new_grammar = collapse_renaming_rules(grammar)

    assert derives(new_grammar, 'c')
    assert derives(new_grammar, 'd')
    assert derives(new_grammar, 'e')
    assert not derives(new_grammar, '')
    assert not has_renaming_rules(new_grammar)
