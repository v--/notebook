from .grammar import GrammarSchema, Grammar, GrammarRule


def is_context_free(grammar: Grammar):
    return all(len(rule.src) == 1 for rule in grammar.schema.rules)


def reverse_grammar(grammar: Grammar):
    assert is_context_free(grammar)

    return GrammarSchema(
        rules=[
            GrammarRule(rule.src, list(reversed(rule.dest)))
            for rule in grammar.schema.rules
        ]
    ).instantiate(grammar.start)
