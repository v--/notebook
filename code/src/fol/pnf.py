from ..exceptions import NotebookCodeError

from .tokens import BinaryConnective, Quantifier
from .formulas import Formula, NegationFormula, ConnectiveFormula, QuantifierFormula
from .visitors import FormulaVisitor, FormulaTransformationVisitor
from .substitution import substitute_in_formula
from .variables import new_variable, get_bound_variables, get_free_variables


class QuantifierlessVerificationVisitor(FormulaVisitor):
    def generic_visit(self, formula: Formula):
        return True

    def visit_negation(self, formula: NegationFormula):
        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula):
        return self.visit(formula.a) and self.visit(formula.b)

    def visit_quantifier(self, formula: QuantifierFormula):
        return False


def is_formula_quantifierless(formula: Formula):
    return QuantifierlessVerificationVisitor().visit(formula)


class PNFVerificationVisitor(FormulaVisitor):
    def generic_visit(self, formula: Formula):
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

        match formula.conn:
            case BinaryConnective.disjunction | BinaryConnective.conjunction:
                return ConnectiveFormula(formula.conn, a, b)

            case BinaryConnective.conditional:
                return ConnectiveFormula(BinaryConnective.disjunction, NegationFormula(a), b)

            case BinaryConnective.biconditional:
                return ConnectiveFormula(
                    BinaryConnective.conjunction,
                    ConnectiveFormula(BinaryConnective.disjunction, NegationFormula(a), b),
                    ConnectiveFormula(BinaryConnective.disjunction, a, NegationFormula(b))
                )


def remove_conditionals(formula: Formula):
    return ConditionalRemovalVisitor().visit(formula)


class MoveNegationsVisitor(FormulaTransformationVisitor):
    def visit_negation(self, formula: NegationFormula):
        if isinstance(formula.sub, ConnectiveFormula):
            new_conn: BinaryConnective

            match formula.sub.conn:
                case BinaryConnective.disjunction:
                    new_conn = BinaryConnective.conjunction
                case BinaryConnective.conjunction:
                    new_conn = BinaryConnective.disjunction
                case _:
                    raise NotebookCodeError(f'Unexpected connective {formula.sub.conn}')

            return ConnectiveFormula(
                new_conn,
                self.visit(NegationFormula(formula.sub.a)),
                self.visit(NegationFormula(formula.sub.b))
            )

        if isinstance(formula.sub, QuantifierFormula):
            new_quantifier: Quantifier

            match formula.sub.quantifier:
                case Quantifier.universal:
                    new_quantifier = Quantifier.existential
                case Quantifier.existential:
                    new_quantifier = Quantifier.universal
                case _:
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
        if formula.conn != BinaryConnective.disjunction and formula.conn != BinaryConnective.conjunction:
            raise NotebookCodeError(f'Unexpected connective {formula.conn}')

        return super().visit_connective(formula)


def push_negations(formula: Formula):
    return MoveNegationsVisitor().visit(formula)


class MoveQuantifiersVisitor(FormulaTransformationVisitor):
    def visit_connective(self, formula: ConnectiveFormula):
        if formula.conn != BinaryConnective.disjunction and formula.conn != BinaryConnective.conjunction:
            raise NotebookCodeError(f'Unexpected connective {formula.conn}')

        if isinstance(formula.a, QuantifierFormula):
            new_var = new_variable(formula.a.variable, get_free_variables(formula.a.sub) | get_free_variables(formula.b))

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
            new_var = new_variable(formula.b.variable, get_free_variables(formula.a) | get_free_variables(formula.b.sub))

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
    return move_quantifiers(push_negations(remove_conditionals(formula)))
