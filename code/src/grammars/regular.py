from .grammar import Grammar, NonTerminal


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
