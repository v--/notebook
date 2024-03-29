from ..automata.finite import FiniteAutomaton, reverse_automaton
from ..automata.finite_determinize import determinize

from .alphabet import NonTerminal, Terminal
from .grammar import GrammarSchema, Grammar, GrammarRule
from .context_free import reverse_grammar
from .epsilon_rules import is_epsilon_rule, is_epsilon_free, remove_epsilon_rules
from .renaming_rules import collapse_renaming_rules

from ..support.names import new_var_name


def is_left_linear_rule(rule: GrammarRule):
    for i, sym in enumerate(rule.dest):
        if isinstance(sym, NonTerminal) and 0 < i:
            return False

    return True


def is_left_linear(grammar: Grammar):
    return all(is_left_linear_rule(rule) for rule in grammar.schema.rules)


def is_right_linear_rule(rule: GrammarRule):
    for i, sym in enumerate(rule.dest):
        if isinstance(sym, NonTerminal) and i < len(rule.dest) - 1:
            return False

    return True


def is_right_linear(grammar: Grammar):
    return all(is_right_linear_rule(rule) for rule in grammar.schema.rules)


def is_regular(grammar: Grammar):
    return is_left_linear(grammar) or is_right_linear(grammar)


# This is alg:regular_grammar_to_automaton in the text
def to_finite_automaton(grammar: Grammar) -> FiniteAutomaton:
    assert is_regular(grammar)

    if is_right_linear(grammar):
        g1 = grammar
    else:
        g1 = reverse_grammar(grammar)

    g2 = remove_epsilon_rules(g1)
    g3 = collapse_renaming_rules(g2)
    g4_schema = GrammarSchema(rules=[])
    new_names = {sym.value for sym in g3.schema.get_non_terminals()}

    for rule in g3.schema.rules:
        last = rule.src_symbol
        last_index = -1 if isinstance(rule.dest[-1], Terminal) else -2

        for sym in rule.dest[:last_index]:
            new_var = NonTerminal(new_var_name(rule.src_symbol.value, new_names))
            new_names.add(new_var.value)
            g4_schema.rules.append(GrammarRule(src=[last], dest=[sym, new_var]))
            last = new_var

        g4_schema.rules.append(GrammarRule(src=[last], dest=rule.dest[last_index:]))

    final = new_var_name('F', new_names)
    aut: FiniteAutomaton = FiniteAutomaton(
        triples=[
            (
                rule.src_symbol.value,
                rule.dest[0].value,
                rule.dest[1].value if len(rule.dest) == 2 else final
            ) for rule in g4_schema.rules if not is_epsilon_rule(rule)
        ],
        initial={g3.start.value},
        terminal={final} if is_epsilon_free(g3) else {final, g3.start.value}
    )

    if is_right_linear(grammar):
        return aut

    return reverse_automaton(aut)


# This is alg:finite_automaton_to_right_linear_grammar from the text
def from_finite_automaton(aut: FiniteAutomaton) -> Grammar:
    det = determinize(aut)
    schema = GrammarSchema([
        GrammarRule([NonTerminal(str(src))], [Terminal(str(label)), NonTerminal(str(dest))])
        for (src, label, dest) in det.triples
    ] + [
        GrammarRule([NonTerminal(str(src))], []) for src in det.terminal
    ])

    return schema.instantiate(NonTerminal(str(next(iter(det.initial)))))
