from .grammar import GrammarRule, NonTerminal, Terminal, epsilon
from .parse_tree import Derivation, DerivationStep, ParseTree, derivation_to_parse_tree, parse_tree_to_derivation


def test_derivation_to_parse_tree_basic():
    derivation = Derivation(
        start=NonTerminal('S'),
        steps=[
            DerivationStep(
                payload=[Terminal('a')],
                rule=GrammarRule([NonTerminal('S')], [Terminal('a')])
            )
        ]
    )

    tree = ParseTree(NonTerminal('S'), children=[ParseTree(Terminal('a'))])

    assert derivation_to_parse_tree(derivation) == tree
    assert parse_tree_to_derivation(tree) == derivation


def test_derivation_to_parse_tree_branching():
    rule_a = GrammarRule([NonTerminal('S')], [Terminal('a'), NonTerminal('S'), Terminal('b')])
    rule_b = GrammarRule([NonTerminal('S')], [Terminal('a'), Terminal('b')])
    derivation = Derivation(
        start=NonTerminal('S'),
        steps=[
            DerivationStep(
                payload=[Terminal('a'), NonTerminal('S'), Terminal('b')],
                rule=rule_a
            ),
            DerivationStep(
                payload=[Terminal('a'), Terminal('a'), NonTerminal('S'), Terminal('b'), Terminal('b')],
                rule=rule_a
            ),
            DerivationStep(
                payload=[Terminal('a'), Terminal('a'), Terminal('a'), Terminal('b'), Terminal('b'), Terminal('b')],
                rule=rule_b
            )
        ]
    )

    tree = ParseTree(
        NonTerminal('S'),
        children=[
            ParseTree(Terminal('a')),
            ParseTree(
                NonTerminal('S'),
                children=[
                    ParseTree(Terminal('a')),
                    ParseTree(
                        NonTerminal('S'),
                        children=[
                            ParseTree(Terminal('a')),
                            ParseTree(Terminal('b'))
                        ]
                    ),
                    ParseTree(Terminal('b'))
                ]
            ),
            ParseTree(Terminal('b'))
        ]
    )

    assert derivation_to_parse_tree(derivation) == tree
    assert parse_tree_to_derivation(tree) == derivation


def test_derivation_to_parse_tree_epsilon():
    rule_a = GrammarRule([NonTerminal('S')], [Terminal('a'), NonTerminal('S'), Terminal('b')])
    rule_b = GrammarRule([NonTerminal('S')], [epsilon])
    derivation = Derivation(
        start=NonTerminal('S'),
        steps=[
            DerivationStep(
                payload=[Terminal('a'), NonTerminal('S'), Terminal('b')],
                rule=rule_a
            ),
            DerivationStep(
                payload=[Terminal('a'), Terminal('b')],
                rule=rule_b
            )
        ]
    )

    tree = ParseTree(
        NonTerminal('S'),
        children=[
            ParseTree(Terminal('a')),
            ParseTree(NonTerminal('S'), children=[ParseTree(epsilon)]),
            ParseTree(Terminal('b'))
        ]
    )

    assert derivation_to_parse_tree(derivation) == tree
    assert parse_tree_to_derivation(tree) == derivation


def test_derivation_to_parse_tree_left_recursion():
    rule_a = GrammarRule([NonTerminal('S')], [NonTerminal('S'), Terminal('a')])
    rule_b = GrammarRule([NonTerminal('S')], [Terminal('a')])
    derivation = Derivation(
        start=NonTerminal('S'),
        steps=[
            DerivationStep(
                payload=[NonTerminal('S'), Terminal('a')],
                rule=rule_a
            ),
            DerivationStep(
                payload=[NonTerminal('S'), Terminal('a'), Terminal('a')],
                rule=rule_a
            ),
            DerivationStep(
                payload=[Terminal('a'), Terminal('a'), Terminal('a')],
                rule=rule_b
            )
        ]
    )

    tree = ParseTree(
        NonTerminal('S'),
        children=[
            ParseTree(
                NonTerminal('S'),
                children=[
                    ParseTree(
                        NonTerminal('S'),
                        children=[
                            ParseTree(Terminal('a'))
                        ]
                    ),
                    ParseTree(Terminal('a'))
                ]
            ),
            ParseTree(Terminal('a'))
        ]
    )

    assert derivation_to_parse_tree(derivation) == tree
    assert parse_tree_to_derivation(tree) == derivation
