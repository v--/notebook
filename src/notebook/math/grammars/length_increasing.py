from typing import TYPE_CHECKING, cast

from ...support.coderefs import collector
from .epsilon_rules import is_epsilon_rule
from .exceptions import IncompatibleGrammarError
from .symbols import Terminal


if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    from .grammar import Grammar, GrammarSchema
    from .symbols import NonTerminal


def is_length_increasing_grammar(grammar: Grammar) -> bool:
    return all(len(rule.src) <= len(rule.dest) for rule in grammar.schema.rules)


def is_essentially_length_increasing_grammar(grammar: Grammar) -> bool:
    return all(
        (is_epsilon_rule(rule) and rule.src == [grammar.start]) or len(rule.src) <= len(rule.dest)
        for rule in grammar.schema.rules
    )


def _iter_all_derivations_one_step(schema: GrammarSchema, current: Iterable[Sequence[Terminal | NonTerminal]]) -> Iterable[Sequence[Terminal | NonTerminal]]:
    for derivation in current:
        for rule in schema.rules:
            if is_epsilon_rule(rule):
                continue

            for i in range(len(derivation) - len(rule.src) + 1):
                if rule.src == derivation[i: len(rule.src) + i]:
                    yield [*derivation[:i], *rule.dest, *derivation[len(rule.src) + i:]]


def iter_derivations(grammar: Grammar, max_derivation_length: int) -> Iterable[Sequence[Terminal]]:
    if not is_essentially_length_increasing_grammar(grammar):
        raise IncompatibleGrammarError('Expected an essentially length-increasing grammar')

    for rule in grammar.schema.rules:
        if is_epsilon_rule(rule):
            yield []

    derivable: Sequence[Sequence[Terminal | NonTerminal]] = [[grammar.start]]

    for _ in range(max_derivation_length):
        derivable = list(_iter_all_derivations_one_step(grammar.schema, derivable))

        for derivation in derivable:
            if all(isinstance(sym, Terminal) for sym in derivation):
                yield cast('Sequence[Terminal]', derivation)


@collector.ref('alg:context_sensitive_string_membership')
def naive_membership(grammar: Grammar, string: str) -> bool:
    if not is_essentially_length_increasing_grammar(grammar):
        raise IncompatibleGrammarError('Expected an essentially length-increasing grammar')

    m = len(grammar.schema.get_non_terminals()) + len(grammar.schema.get_terminals())
    n = len(string)

    max_derivation_length = (1 - m ** (n + 1)) // (1 - m) if m > 1 else n

    for derivation in iter_derivations(grammar, max_derivation_length):
        if ''.join(sym.value for sym in derivation) == string:
            return True

    return False
