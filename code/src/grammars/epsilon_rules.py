from typing import cast

from ..support.names import new_var_name

from .grammar import Grammar, GrammarRule, GrammarSchema, NonTerminal, Terminal, SingletonSymbol


def is_epsilon_rule(rule: GrammarRule):
    return len(rule.src) == 1 and rule.dest == [SingletonSymbol.epsilon]


def is_epsilon_free(grammar: Grammar):
    return all(not is_epsilon_rule(rule) for rule in grammar.schema.rules)


def is_essentially_epsilon_free(grammar: Grammar):
    for rule in grammar.schema.rules:
        if is_epsilon_rule(rule):
            if rule.src != [grammar.start]:
                return False
            elif any(grammar.start in r.dest for r in grammar.schema.rules):
                return False

    return True


def identify_nullable_non_terminals(grammar: Grammar):
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


def iter_rules_without_nullables(nullable: set[NonTerminal], dest: list[NonTerminal | Terminal]):
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
    new_start = NonTerminal(
        new_var_name(
            grammar.start.value,
            {sym.value for sym in grammar.schema.get_non_terminals()}
        )
    )

    new_schema = GrammarSchema(rules=[GrammarRule(src=[new_start], dest=[grammar.start])])

    if grammar.start in nullable:
        new_schema.rules.append(GrammarRule(src=[new_start], dest=[SingletonSymbol.epsilon]))

    for rule in grammar.schema.rules:
        if is_epsilon_rule(rule):
            continue

        for new_dest in iter_rules_without_nullables(nullable, cast(list[NonTerminal | Terminal], rule.dest)):
            if len(new_dest) > 0:
                new_schema.rules.append(GrammarRule(rule.src, new_dest))

    return new_schema.instantiate(new_start)
