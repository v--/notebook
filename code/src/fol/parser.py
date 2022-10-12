from typing import Literal, cast
from ..support.parsing import ParserError
from ..grammars.grammar import GrammarSchema, NonTerminal
from ..grammars.parse_tree import ParseTree, RuleVisitor
from ..grammars import unger

from .types import Term, Variable, FunctionTerm, Formula


grammar_schema = GrammarSchema.parse('''
    <variable>           →   <greek_name>
    <constant>           →   <latin_name>
    <function>           →   <latin_name> <arg_list>
    <term>               →   <function> | <constant> | <variable>

    <equality>           →   "(" <term> <opt_space> "=" <opt_space> <term> ")"
    <predicate>          →   <latin_name> <arg_list>
    <atomic>             →   <equality> | <predicate>
    <negation>           →   "¬" <formula>
    <conn_formula>       →   "(" <formula> <opt_space> <connective> <opt_space> <formula> ")"
    <quan_formula>       →   <quantifier> <variable> "." <formula>
    <formula>            →   <atomic> | <negation> | <conn_formula> | <quan_formula>
    <quantifier>         →   "∀" | "∃"
    <connective>         →   "∨" | "∧" | "→" | "↔"

    <latin_letter>       →   "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
    <latin_string>       →   <latin_letter> | <latin_letter> <latin_string>
    <latin_name>         →   <latin_string> | <latin_string> <natural_number>

    <greek_letter>       →   "α" | "β" | "γ" | "δ" | "ε" | "ζ" | "η" | "θ" | "ι" | "κ" | "λ" | "μ" | "ν" | "ξ" | "ο" | "π" | "ρ" | "σ" | "τ" | "υ" | "φ" | "χ" | "ψ" | "ω"
    <greek_string>       →   <greek_letter> | <greek_letter> <greek_string>
    <greek_name>         →   <greek_string> | <greek_string> <natural_number>

    <nonzero_digit>      →   "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
    <digit>              →   "0" | <nonzero_digit>
    <natural_number_aux> →   <digit> | <digit> <natural_number_aux>
    <natural_number>     →   <digit> | <nonzero_digit> <natural_number_aux>

    <arg_list_aux>       →   ε | "," <opt_space> <term> <opt_space> <arg_list_aux>
    <arg_list>           →   "(" <opt_space> <term> <arg_list_aux> <opt_space> ")"
    <opt_space>          →   ε | " " | " " <opt_space>
''')


class FOLVisitor(RuleVisitor):
    def visit_variable(self, tree: ParseTree, name: str):
        return Variable(name)

    def visit_constant(self, tree: ParseTree, name: str):
        return FunctionTerm(name, [])

    def visit_function(self, tree: ParseTree, name: str, args: list[Term]):
        return FunctionTerm(name, args)

    def visit_term(self, tree: ParseTree, value: Term):
        return value

    # def visit_equality(self, tree: ParseTree):
    #     (_, a, _, _, _, b, _) = visited_children
    #     return EqualityFormula(a, b)

    # def visit_predicate(self, tree: ParseTree):
    #     name, arguments = visited_children
    #     return PredicateFormula(name, arguments)

    # def visit_atomic(self, tree: ParseTree):
    #     formula, = visited_children
    #     return formula

    # def visit_negation(self, tree: ParseTree):
    #     _, formula = visited_children
    #     return NegationFormula(formula)

    # def visit_conn_formula(self, tree: ParseTree):
    #     _, a, _, conn, _, b, _ = visited_children
    #     return ConnectiveFormula(conn, a, b)

    # def visit_quan_formula(self, tree: ParseTree):
    #     quantifier, var, _, formula = visited_children
    #     return QuantifierFormula(quantifier, var, formula)

    # def visit_formula(self, tree: ParseTree):
    #     formula, = visited_children
    #     return formula

    # def visit_quantifier(self, tree: ParseTree):
    #     return visited_children[0].text

    # def visit_connective(self, tree: ParseTree):
    #     return visited_children[0].text

    # def visit_arg_list(self, tree: ParseTree):
    #     (_, _, first, rest, _) = visited_children
    #     return [first] + [var for (_, _, var, _) in rest]

    def visit_latin_letter(self, tree: ParseTree, letter: str):
        return letter

    def visit_latin_string(self, tree: ParseTree, letter: str, rest: str = ''):
        return letter + rest

    def visit_latin_name(self, tree: ParseTree, string: str, number: str = ''):
        return string + number

    def visit_greek_letter(self, tree: ParseTree, letter: str):
        return letter

    def visit_greek_string(self, tree: ParseTree, letter: str, rest: str = ''):
        return letter + rest

    def visit_greek_name(self, tree: ParseTree, string: str, number: str = ''):
        return string + number

    def visit_nonzero_digit(self, tree: ParseTree, digit: str):
        return digit

    def visit_digit(self, tree: ParseTree, digit: str):
        return digit

    def visit_natural_number_aux(self, tree: ParseTree, digit: str, aux: str = ''):
        return digit + aux

    def visit_natural_number(self, tree: ParseTree, digit: str, aux: str = ''):
        return digit + aux

    def visit_arg_list_aux(
        self,
        tree: ParseTree,
        comma: Literal['<'] | None = None,
        opt_space_1: str | None = None,
        term: Term | None = None,
        opt_space_2: str | None = None,
        aux: list[Term] | None = None
    ):
        # This will always short-circuit, but both conditions are necessary for mypy
        if term is None or aux is None:
            return []

        return [term] + aux

    def visit_arg_list(
        self,
        tree: ParseTree,
        opening_brace: Literal['('],
        opt_space_1: str,
        term: str,
        aux: list[Term],
        opt_space_2: str,
        closing_brace: Literal[')']
    ):
        return [term] + aux

    def visit_opt_space(self, tree: ParseTree, space: str, more_space: str = ''):
        # <space> may be ε
        return (space or '') + more_space


visitor = FOLVisitor()


def parse(string: str, rule: NonTerminal):
    # Return first
    for tree in unger.parse(grammar_schema.instantiate(rule), string):
        return visitor.visit(tree)

    raise ParserError(f'Could not parse {string} as {rule}')


def parse_formula(string: str) -> Formula:
    return parse(string, rule=NonTerminal('formula'))
