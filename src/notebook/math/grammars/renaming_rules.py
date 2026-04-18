from typing import TYPE_CHECKING

from ...support.coderefs import collector
from .epsilon_rules import is_essentially_epsilon_free
from .exceptions import IncompatibleGrammarError
from .grammar import Grammar, GrammarRule, GrammarSchema
from .symbols import NonTerminal, Terminal


if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence


def is_rule_renaming(rule: GrammarRule) -> bool:
    return len(rule.dest) == 1 and isinstance(rule.dest[0], NonTerminal)


def has_renaming_rules(grammar: Grammar) -> bool:
    return any(is_rule_renaming(rule) for rule in grammar.schema.rules)


def iter_renamed_targets(grammar: Grammar, traversed: set[NonTerminal]) -> Iterable[Sequence[NonTerminal | Terminal]]:
    if grammar.start in traversed:
        return

    for rule in grammar.iter_starting_rules():
        if is_rule_renaming(rule):
            if TYPE_CHECKING:
                assert isinstance(rule.dest[0], NonTerminal)

            yield from iter_renamed_targets(grammar.schema.instantiate(rule.dest[0]), traversed | {grammar.start})
        else:
            yield rule.dest


@collector.ref('alg:renaming_rule_collapse')
def collapse_renaming_rules(grammar: Grammar) -> Grammar:
    if not is_essentially_epsilon_free(grammar):
        raise IncompatibleGrammarError('Expected an essentially ε-free grammar')

    new_rules = list[GrammarRule]()

    for non_terminal in grammar.schema.get_non_terminals():
        for dest in iter_renamed_targets(grammar.schema.instantiate(non_terminal), set()):
            new_rules.append(GrammarRule([non_terminal], dest))

    return GrammarSchema(new_rules).instantiate(grammar.start)
