from ..exceptions import NotebookCodeError
from ..support.names import new_var_name

from .tokens import SingletonFOLToken, meet, join, conditional, biconditional, universal_quantifier, existential_quantifier
from .types import Formula, EqualityFormula, PredicateFormula, NegationFormula, ConnectiveFormula, QuantifierFormula, Formula, Variable
from .visitors import FormulaVisitor, FormulaTransformationVisitor
from .substitution import substitute_in_formula
from .variables import get_bound_variables, get_free_variables


class PNFVerificationVisitor(FormulaVisitor):
    def visit_equality(self, formula: EqualityFormula):
        return True

    def visit_predicate(self, formula: PredicateFormula):
        return True

    def visit_negation(self, formula: NegationFormula):
        if isinstance(formula.sub, QuantifierFormula):
            return False

        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula):
        if isinstance(formula.a, QuantifierFormula) or isinstance(formula.b, QuantifierFormula):
            return False

        return self.visit(formula.a) and self.visit(formula.b)

    def visit_quantifier(self, formula: QuantifierFormula):
        return self.visit(formula.sub)


def is_formula_in_pnf(formula: Formula):
    return PNFVerificationVisitor().visit(formula)


class ConditionalRemovalVisitor(FormulaTransformationVisitor):
    def visit_connective(self, formula: ConnectiveFormula):
        a = self.visit(formula.a)
        b = self.visit(formula.b)

        if formula.conn == join or formula.conn == meet:
            return ConnectiveFormula(formula.conn, a, b)

        if formula.conn == conditional:
            return ConnectiveFormula(join, NegationFormula(a), b)

        if formula.conn == biconditional:
            return ConnectiveFormula(
                meet,
                ConnectiveFormula(join, NegationFormula(a), b),
                ConnectiveFormula(join, a, NegationFormula(b))
            )


def remove_conditionals(formula: Formula):
    return ConditionalRemovalVisitor().visit(formula)


class MoveNegationsVisitor(FormulaTransformationVisitor):
    def visit_negation(self, formula: NegationFormula):
        if isinstance(formula.sub, ConnectiveFormula):
            new_conn: SingletonFOLToken

            if formula.sub.conn == join:
                new_conn = meet
            elif formula.sub.conn == meet:
                new_conn = join
            else:
                raise NotebookCodeError(f'Unexpected connective {formula.sub.conn}')

            return ConnectiveFormula(
                new_conn,
                self.visit(NegationFormula(formula.sub.a)),
                self.visit(NegationFormula(formula.sub.b))
            )

        if isinstance(formula.sub, QuantifierFormula):
            new_quantifier: SingletonFOLToken

            if formula.sub.quantifier == universal_quantifier:
                new_quantifier = existential_quantifier
            elif formula.sub.quantifier == existential_quantifier:
                new_quantifier = universal_quantifier
            else:
                raise NotebookCodeError(f'Unexpected quantifier {formula.sub.quantifier}')

            return QuantifierFormula(
                new_quantifier,
                formula.sub.variable,
                self.visit(NegationFormula(formula.sub.sub))
            )

        if isinstance(formula.sub, NegationFormula):
            return self.visit(formula.sub.sub)

        return NegationFormula(self.visit(formula.sub))

    def visit_connective(self, formula: ConnectiveFormula):
        if formula.conn != join and formula.conn != meet:
            raise NotebookCodeError(f'Unexpected connective {formula.conn}')

        return super().visit_connective(formula)


def move_negations(formula: Formula):
    return MoveNegationsVisitor().visit(formula)


class MoveQuantifiersVisitor(FormulaTransformationVisitor):
    def visit_connective(self, formula: ConnectiveFormula):
        if formula.conn != join and formula.conn != meet:
            raise NotebookCodeError(f'Unexpected connective {formula.conn}')

        if isinstance(formula.a, QuantifierFormula):
            old_name = formula.a.variable.name
            new_name = new_var_name(old_name, get_free_variables(formula.a.sub) | get_free_variables(formula.b))
            new_var = Variable(new_name)

            return QuantifierFormula(
                formula.a.quantifier,
                new_var,
                self.visit(
                    ConnectiveFormula(
                        formula.conn,
                        substitute_in_formula(formula.a.sub, formula.a.variable, new_var),
                        formula.b
                    )
                )
            )

        if isinstance(formula.b, QuantifierFormula):
            old_name = formula.b.variable.name
            new_name = new_var_name(old_name, get_free_variables(formula.a) | get_free_variables(formula.b.sub))
            new_var = Variable(new_name)

            return QuantifierFormula(
                formula.b.quantifier,
                new_var,
                self.visit(
                    ConnectiveFormula(
                        formula.conn,
                        formula.a,
                        substitute_in_formula(formula.b.sub, formula.b.variable, new_var),
                    )
                )
            )

        if len(get_bound_variables(formula.a)) == 0 and len(get_bound_variables(formula.b)) == 0:
            return formula

        return self.visit(
            ConnectiveFormula(
                formula.conn,
                self.visit(formula.a),
                self.visit(formula.b)
            )
        )


def move_quantifiers(formula: Formula):
    return MoveQuantifiersVisitor().visit(formula)


# This is alg:prenex_normal_form_conversion in the text
def to_pnf(formula: Formula):
    return move_quantifiers(move_negations(remove_conditionals(formula)))
