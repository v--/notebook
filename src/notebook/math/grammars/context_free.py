from .exceptions import IncompatibleGrammarError
from .grammar import Grammar, GrammarRule, GrammarSchema


def is_context_free(grammar: Grammar) -> bool:
    return all(len(rule.src) == 1 for rule in grammar.schema.rules)


def reverse_grammar(grammar: Grammar) -> Grammar:
    if not is_context_free(grammar):
        raise IncompatibleGrammarError('Expected a context-free grammar')

    return GrammarSchema(
        rules=[
            GrammarRule(rule.src, list(reversed(rule.dest)))
            for rule in grammar.schema.rules
        ],
    ).instantiate(grammar.start)
