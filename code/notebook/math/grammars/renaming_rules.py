from collections.abc import Iterable, Sequence

from .alphabet import NonTerminal, Terminal
from .epsilon_rules import is_essentially_epsilon_free
from .grammar import Grammar, GrammarRule, GrammarSchema


def is_rule_renaming(rule: GrammarRule) -> bool:
    return len(rule.dest) == 1 and isinstance(rule.dest[0], NonTerminal)


def has_renaming_rules(grammar: Grammar) -> bool:
    return any(is_rule_renaming(rule) for rule in grammar.schema.rules)


def iter_renamed_targets(grammar: Grammar, traversed: set[NonTerminal]) -> Iterable[Sequence[NonTerminal | Terminal]]:
    if grammar.start in traversed:
        return

    for rule in grammar.iter_starting_rules():
        if is_rule_renaming(rule):
            assert isinstance(rule.dest[0], NonTerminal)
            yield from iter_renamed_targets(grammar.schema.instantiate(rule.dest[0]), traversed | {grammar.start})
        else:
            yield rule.dest


# This is alg:renaming_rule_collapse in the monograph
def collapse_renaming_rules(grammar: Grammar) -> Grammar:
    assert is_essentially_epsilon_free(grammar)
    new_rules = list[GrammarRule]()

    for non_terminal in grammar.schema.get_non_terminals():
        for dest in iter_renamed_targets(grammar.schema.instantiate(non_terminal), set()):
            new_rules.append(GrammarRule([non_terminal], dest))

    return GrammarSchema(new_rules).instantiate(grammar.start)
