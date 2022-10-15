from .grammar import Grammar, NonTerminal


def is_context_free(grammar: Grammar):
    return all(len(rule.src) == 1 for rule in grammar.schema.rules)
