from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, cast

from ...support.coderefs import collector
from .epsilon_rules import is_epsilon_rule
from .exceptions import IncompatibleGrammarError
from .symbols import Terminal, new_non_terminal
from .length_increasing import is_essentially_length_increasing_grammar
from .grammar import GrammarRule, Grammar, GrammarSchema

from .symbols import NonTerminal


def is_context_sensitive_rule(rule: GrammarRule) -> bool:
    for i in range(len(rule.src)):
        if not isinstance(rule.src[i], NonTerminal) or rule.src[:i] != rule.dest[:i]:
            continue

        for j in range(len(rule.dest), i, -1):
            if rule.src[i + 1:] == rule.dest[j:]:
                return True

    return False


def is_context_sensitive_grammar(grammar: Grammar) -> bool:
    return all(
        (is_epsilon_rule(rule) and rule.src == [grammar.start]) or is_context_sensitive_rule(rule)
        for rule in grammar.schema.rules
    )


@collector.ref('alg:length_increasing_to_context_sensitive')
def length_increasing_to_context_sensitive(grammar: Grammar) -> Grammar:
    if not is_essentially_length_increasing_grammar(grammar):
        raise IncompatibleGrammarError('Expected an essentially length-increasing grammar')

    non_terminals = list(grammar.schema.get_non_terminals())
    terminal_map = dict[Terminal, NonTerminal]()
    current_schema = GrammarSchema()

    for sym in grammar.schema.get_terminals():
        active_non_terminal = new_non_terminal(sym.value, non_terminals)
        current_schema.rules.append(
            GrammarRule(
                src=[active_non_terminal],
                dest=[sym]
            )
        )

        terminal_map[sym] = active_non_terminal
        non_terminals.append(active_non_terminal)

    # We iterate over rules from the original grammar and modify the result at every step
    for rule in grammar.schema.rules:
        if is_epsilon_rule(rule):
            current_schema.rules.append(rule)
            continue

        modified_src = [terminal_map[sym] if isinstance(sym, Terminal) else sym for sym in rule.src]
        modified_dest = [terminal_map[sym] if isinstance(sym, Terminal) else sym for sym in rule.dest]
        dest_tail = modified_dest[len(rule.src):]
        new_non_terminals = list[NonTerminal]()

        for i, sym in enumerate(rule.src):
            tail = modified_src[i + 1:] if i + 1 < len(rule.src) else dest_tail
            active_non_terminal = new_non_terminal(sym.value, non_terminals)
            current_schema.rules.append(
                GrammarRule(
                    src=[*new_non_terminals, *modified_src[i:]],
                    dest=[*new_non_terminals, active_non_terminal, *tail]
                )
            )

            new_non_terminals.append(active_non_terminal)
            non_terminals.append(active_non_terminal)

        for i in range(len(new_non_terminals)):
            current_schema.rules.append(
                GrammarRule(
                    src=[*modified_dest[:i], *new_non_terminals[i:], *dest_tail],
                    dest=[*modified_dest[:i + 1], *new_non_terminals[i + 1:], *dest_tail],
                )
            )

    print()
    print(current_schema)

    return current_schema.instantiate(grammar.start)
