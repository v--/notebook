from ..automata.finite import FiniteAutomaton, reverse_automaton
from ..automata.finite_determinize import determinize
from .alphabet import NonTerminal, Terminal, new_non_terminal
from .context_free import reverse_grammar
from .epsilon_rules import is_epsilon_free, is_epsilon_rule, remove_epsilon_rules
from .grammar import Grammar, GrammarRule, GrammarSchema
from .renaming_rules import collapse_renaming_rules


def is_left_linear_rule(rule: GrammarRule) -> bool:
    if is_epsilon_rule(rule):
        return True

    return all(isinstance(sym, Terminal) for sym in rule.dest[1:])


def is_left_linear(grammar: Grammar) -> bool:
    return all(is_left_linear_rule(rule) for rule in grammar.schema.rules)


def is_right_linear_rule(rule: GrammarRule) -> bool:
    if is_epsilon_rule(rule):
        return True

    return all(isinstance(sym, Terminal) for sym in rule.dest[:-1])


def is_right_linear(grammar: Grammar) -> bool:
    return all(is_right_linear_rule(rule) for rule in grammar.schema.rules)


def is_regular(grammar: Grammar) -> bool:
    return is_left_linear(grammar) or is_right_linear(grammar)


# This is alg:regular_grammar_to_automaton in the monograph
def to_finite_automaton(grammar: Grammar) -> FiniteAutomaton[str, str]:
    assert is_regular(grammar)

    g1 = grammar if is_right_linear(grammar) else reverse_grammar(grammar)

    g2 = remove_epsilon_rules(g1)
    g3 = collapse_renaming_rules(g2)
    g4_rules = list[GrammarRule]()
    new_names = set(g3.schema.get_non_terminals())

    for rule in g3.schema.rules:
        if is_epsilon_rule(rule):
            assert rule.src == [g3.start]
            g4_rules.append(rule)
            continue

        last = rule.src_symbol
        last_index = -1 if isinstance(rule.dest[-1], Terminal) else -2

        for sym in rule.dest[:last_index]:
            new_var = new_non_terminal(rule.src_symbol.value, new_names)
            new_names.add(new_var)
            g4_rules.append(GrammarRule(src=[last], dest=[sym, new_var]))
            last = new_var

        g4_rules.append(GrammarRule(src=[last], dest=rule.dest[last_index:]))

    final = new_non_terminal('F', new_names)
    aut = FiniteAutomaton[str, str]()

    aut.initial.add(g3.start.value)
    aut.terminal.add(final.value)

    if not is_epsilon_free(g3):
        aut.terminal.add(g3.start.value)

    for rule in g4_rules:
        if not is_epsilon_rule(rule):
            aut.add_transition(
                src=rule.src_symbol.value,
                dest=rule.dest[1].value if len(rule.dest) > 1 else final.value,
                symbol=rule.dest[0].value
            )

    if is_right_linear(grammar):
        return aut

    return reverse_automaton(aut)


# This is alg:finite_automaton_to_right_linear_grammar from the text
def from_finite_automaton[StateT, SymbolT](aut: FiniteAutomaton[StateT, SymbolT]) -> Grammar:
    det = determinize(aut)
    schema = GrammarSchema([
        GrammarRule([NonTerminal(str(src))], [Terminal(str(label)), NonTerminal(str(dest))])
        for (src, dest, label) in det.transitions
    ] + [
        GrammarRule([NonTerminal(str(src))], []) for src in det.terminal
    ])

    return schema.instantiate(NonTerminal(str(next(iter(det.initial)))))
