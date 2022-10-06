from .grammar import Grammar


def is_epsilon_free(grammar: Grammar):
    return all(not rule.is_epsilon for rule in grammar.schema.rules)


def is_essentially_epsilon_free(grammar: Grammar):
    for rule in grammar.schema.rules:
        if rule.dest == []:
            if rule.src != [grammar.start]:
                return False
            elif any(grammar.start in r.dest for r in grammar.schema.rules):
                return False

    return True


def is_context_free(grammar: Grammar):
    return all(len(rule.src) == 1 for rule in grammar.schema.rules)
