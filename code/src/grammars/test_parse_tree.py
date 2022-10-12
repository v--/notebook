from .grammar import GrammarRule, NonTerminal, Terminal, epsilon
from .parse_tree import Derivation, DerivationStep, ParseTree, derivation_to_parse_tree


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


def test_derivation_to_parse_tree_branching():
    rule = GrammarRule([NonTerminal('S')], [Terminal('a'), NonTerminal('S'), Terminal('b')])
    derivation = Derivation(
        start=NonTerminal('S'),
        steps=[
            DerivationStep(
                payload=[Terminal('a'), NonTerminal('S'), Terminal('b')],
                rule=rule
            ),
            DerivationStep(
                payload=[Terminal('a'), NonTerminal('S'), Terminal('b')],
                rule=rule
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
                    ParseTree(NonTerminal('S')),
                    ParseTree(Terminal('b'))
                ]
            ),
            ParseTree(Terminal('b'))
        ]
    )

    assert derivation_to_parse_tree(derivation) == tree


def test_derivation_to_parse_tree_epsilon():
    rule_a = GrammarRule([NonTerminal('S')], [Terminal('a'), NonTerminal('S'), Terminal('b')])
    rule_b = GrammarRule([NonTerminal('S')], [])
    derivation = Derivation(
        start=NonTerminal('S'),
        steps=[
            DerivationStep(
                payload=[NonTerminal('a'), NonTerminal('S'), Terminal('a')],
                rule=rule_a
            ),
            DerivationStep(
                payload=[NonTerminal('a'), Terminal('b')],
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


def test_left_recursion():
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
                payload=[NonTerminal('S'), NonTerminal('S'), Terminal('a')],
                rule=rule_a
            ),
            DerivationStep(
                payload=[NonTerminal('S'), NonTerminal('a'), Terminal('a')],
                rule=rule_b
            ),
            DerivationStep(
                payload=[NonTerminal('a'), NonTerminal('a'), Terminal('a')],
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
                    ParseTree(Terminal('a'))
                ]
            ),
            ParseTree(Terminal('a'))
        ]
    )

    assert derivation_to_parse_tree(derivation) == tree
