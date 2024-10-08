from collections.abc import Collection, Iterable, Sequence

from .alphabet import NonTerminal, Terminal, new_non_terminal
from .grammar import Grammar, GrammarRule, GrammarSchema


def is_epsilon_rule(rule: GrammarRule) -> bool:
    return len(rule.dest) == 0


def is_epsilon_free(grammar: Grammar) -> bool:
    return all(not is_epsilon_rule(rule) for rule in grammar.schema.rules)


def is_essentially_epsilon_free(grammar: Grammar) -> bool:
    for rule in grammar.schema.rules:
        if is_epsilon_rule(rule) and (rule.src != [grammar.start] or any(grammar.start in r.dest for r in grammar.schema.rules)):
            return False

    return True


def identify_nullable_non_terminals(grammar: Grammar) -> Collection[NonTerminal]:
    nullable: set[NonTerminal] = set()
    added_during_iteration = False

    for rule in grammar.schema.rules:
        if is_epsilon_rule(rule):
            added_during_iteration = True
            nullable.add(rule.src_symbol)

    while added_during_iteration:
        added_during_iteration = False
        for rule in grammar.schema.rules:
            if all(sym in nullable for sym in rule.dest) and rule.src_symbol not in nullable:
                added_during_iteration = True
                nullable.add(rule.src_symbol)

    return nullable


def iter_rules_without_nullables(nullable: Collection[NonTerminal], dest: Sequence[NonTerminal | Terminal]) -> Iterable[Sequence[NonTerminal | Terminal]]:
    assert len(dest) > 0

    if len(dest) == 1:
        yield dest

        if dest[0] in nullable:
            yield []
    else:
        for part in iter_rules_without_nullables(nullable, dest[1:]):
            yield [dest[0], *part]

            if dest[0] in nullable and len(part) > 0:
                yield part


def remove_epsilon_rules(grammar: Grammar) -> Grammar:
    nullable = identify_nullable_non_terminals(grammar)
    new_start = new_non_terminal(
        grammar.start.value,
        grammar.schema.get_non_terminals()
    )

    new_rules = [GrammarRule(src=[new_start], dest=[grammar.start])]

    if grammar.start in nullable:
        new_rules.append(GrammarRule(src=[new_start], dest=[]))

    for rule in grammar.schema.rules:
        if is_epsilon_rule(rule):
            continue

        new_rules.extend(
            GrammarRule(rule.src, new_dest)
            for new_dest in iter_rules_without_nullables(nullable, rule.dest)
            if len(new_dest) > 0
        )

    new_schema = GrammarSchema(new_rules)
    return new_schema.instantiate(new_start)
