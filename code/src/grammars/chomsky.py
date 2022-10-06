from .grammar import Grammar, NonTerminal


def is_epsilon_free(grammar: Grammar):
    return all(not rule.is_epsilon for rule in grammar.schema.rules)


def is_essentially_epsilon_free(grammar: Grammar):
    for rule in grammar.schema.rules:
        if rule.is_epsilon:
            if rule.src != [grammar.start]:
                return False
            elif any(grammar.start in r.dest for r in grammar.schema.rules):
                return False

    return True


def is_context_free(grammar: Grammar):
    return all(len(rule.src) == 1 for rule in grammar.schema.rules)


def is_left_linear(grammar: Grammar):
    for rule in grammar.schema.rules:
        for i, sym in enumerate(rule.dest):
            if isinstance(sym, NonTerminal) and 0 < i:
                return False

    return True


def is_right_linear(grammar: Grammar):
    for rule in grammar.schema.rules:
        for i, sym in enumerate(rule.dest):
            if isinstance(sym, NonTerminal) and i < len(rule.dest) - 1:
                return False

    return True


def is_regular(grammar: Grammar):
    return is_left_linear(grammar) or is_right_linear(grammar)
