from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor, Node, RegexNode

from .types import Variable, FunctionTerm, Formula, EqualityFormula, PredicateFormula, NegationFormula, ConnectiveFormula, QuantifierFormula, Formula


# https://github.com/erikrose/parsimonious/issues/131
grammar = Grammar(r'''
    variable      = greek_name ''
    constant      = latin_name ''
    function      = latin_name arg_list
    term          = function / constant / variable

    equality      = '(' term opt_space '=' opt_space term ')'
    predicate     = latin_name arg_list
    atomic        = equality / predicate
    negation      = '¬' formula
    conn_formula  = '(' formula opt_space connective opt_space formula ')'
    quan_formula  = quantifier variable '.' formula
    formula       = atomic / negation / conn_formula / quan_formula

    quantifier    = '∀' / '∃'
    connective    = '∨' / '∧' / '→' / '↔'

    arg_list      = '(' opt_space term (',' opt_space term opt_space)* ')'
    opt_space     = ~'\\s*'
    greek_name    = ~'[\\p{Greek}]+([1-9]\\d*)?'
    latin_name    = ~'[\\p{Latin}]+([1-9]\\d*)?'
''')


class FormulaVisitor(NodeVisitor):
    def visit_variable(self, node: Node, visited_children: list):
        name, _ = visited_children
        return Variable(name)

    def visit_constant(self, node: Node, visited_children: list):
        name, _ = visited_children
        return FunctionTerm(name, [])

    def visit_function(self, node: Node, visited_children: list):
        name, arguments = visited_children
        return FunctionTerm(name, arguments)

    def visit_term(self, node: Node, visited_children: list):
        term, = visited_children
        return term

    def visit_equality(self, node: Node, visited_children: list):
        (_, a, _, _, _, b, _) = visited_children
        return EqualityFormula(a, b)

    def visit_predicate(self, node: Node, visited_children: list):
        name, arguments = visited_children
        return PredicateFormula(name, arguments)

    def visit_atomic(self, node: Node, visited_children: list):
        formula, = visited_children
        return formula

    def visit_negation(self, node: Node, visited_children: list):
        _, formula = visited_children
        return NegationFormula(formula)

    def visit_conn_formula(self, node: Node, visited_children: list):
        _, a, _, conn, _, b, _ = visited_children
        return ConnectiveFormula(conn, a, b)

    def visit_quan_formula(self, node: Node, visited_children: list):
        quantifier, var, _, formula = visited_children
        return QuantifierFormula(quantifier, var, formula)

    def visit_formula(self, node: Node, visited_children: list):
        formula, = visited_children
        return formula

    def visit_quantifier(self, node: Node, visited_children: list):
        return visited_children[0].text

    def visit_connective(self, node: Node, visited_children: list):
        return visited_children[0].text

    def visit_arg_list(self, node: Node, visited_children: list):
        (_, _, first, rest, _) = visited_children
        return [first] + [var for (_, _, var, _) in rest]

    def visit_opt_space(self, node: RegexNode, visited_children: list):
        return None

    def visit_greek_name(self, node: RegexNode, visited_children: list):
        return node.text

    def visit_latin_name(self, node: RegexNode, visited_children: list):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


visitor = FormulaVisitor()


def parse(string: str, rule: str):
    return visitor.visit(grammar.default(rule).parse(string))


def parse_formula(string: str) -> Formula:
    return parse(string, rule='formula')
