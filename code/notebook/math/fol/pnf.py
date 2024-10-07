from ...exceptions import NotebookCodeError
from .alphabet import BinaryConnective, Quantifier
from .formulas import ConnectiveFormula, Formula, NegationFormula, QuantifierFormula
from .substitution import substitute_in_formula
from .variables import get_bound_variables, get_free_variables, new_variable
from .visitors import FormulaTransformationVisitor, FormulaVisitor


class PNFError(NotebookCodeError):
    pass


class QuantifierlessVerificationVisitor(FormulaVisitor[bool]):
    def generic_visit(self, formula: Formula) -> bool:  # noqa: ARG002
        return True

    def visit_negation(self, formula: NegationFormula) -> bool:
        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula) -> bool:
        return self.visit(formula.a) and self.visit(formula.b)

    def visit_quantifier(self, formula: QuantifierFormula) -> bool:  # noqa: ARG002
        return False


def is_formula_quantifierless(formula: Formula) -> bool:
    return QuantifierlessVerificationVisitor().visit(formula)


class PNFVerificationVisitor(FormulaVisitor[bool]):
    def generic_visit(self, formula: Formula) -> bool:  # noqa: ARG002
        return True

    def visit_negation(self, formula: NegationFormula) -> bool:
        if isinstance(formula.sub, QuantifierFormula):
            return False

        return self.visit(formula.sub)

    def visit_connective(self, formula: ConnectiveFormula) -> bool:
        if isinstance(formula.a, QuantifierFormula) or isinstance(formula.b, QuantifierFormula):
            return False

        return self.visit(formula.a) and self.visit(formula.b)

    def visit_quantifier(self, formula: QuantifierFormula) -> bool:
        return self.visit(formula.sub)


def is_formula_in_pnf(formula: Formula) -> bool:
    return PNFVerificationVisitor().visit(formula)


class ConditionalRemovalVisitor(FormulaTransformationVisitor):
    def visit_connective(self, formula: ConnectiveFormula) -> ConnectiveFormula:
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


def remove_conditionals(formula: Formula) -> Formula:
    return ConditionalRemovalVisitor().visit(formula)


class MoveNegationsVisitor(FormulaTransformationVisitor):
    def visit_negation(self, formula: NegationFormula) -> Formula:
        if isinstance(formula.sub, ConnectiveFormula):
            new_conn: BinaryConnective

            match formula.sub.conn:
                case BinaryConnective.disjunction:
                    new_conn = BinaryConnective.conjunction
                case BinaryConnective.conjunction:
                    new_conn = BinaryConnective.disjunction
                case _:
                    raise PNFError(f'Unexpected connective {formula.sub.conn}')

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
                    raise PNFError(f'Unexpected quantifier {formula.sub.quantifier}')

            return QuantifierFormula(
                new_quantifier,
                formula.sub.variable,
                self.visit(NegationFormula(formula.sub.sub))
            )

        if isinstance(formula.sub, NegationFormula):
            return self.visit(formula.sub.sub)

        return NegationFormula(self.visit(formula.sub))

    def visit_connective(self, formula: ConnectiveFormula) -> Formula:
        if formula.conn not in (BinaryConnective.disjunction, BinaryConnective.conjunction):
            raise PNFError(f'Unexpected connective {formula.conn}')

        return super().visit_connective(formula)


def move_negations(formula: Formula) -> Formula:
    return MoveNegationsVisitor().visit(formula)


class MoveQuantifiersVisitor(FormulaTransformationVisitor):
    def visit_connective(self, formula: ConnectiveFormula) -> Formula:
        if formula.conn not in (BinaryConnective.disjunction, BinaryConnective.conjunction):
            raise PNFError(f'Unexpected connective {formula.conn}')

        if isinstance(formula.a, QuantifierFormula):
            new_var = new_variable({*get_free_variables(formula.a.sub), *get_free_variables(formula.b)})

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
            new_var = new_variable({*get_free_variables(formula.a), *get_free_variables(formula.b.sub)})

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


def move_quantifiers(formula: Formula) -> Formula:
    return MoveQuantifiersVisitor().visit(formula)


# This is alg:prenex_normal_form_conversion in the monograph
def to_pnf(formula: Formula) -> Formula:
    return move_quantifiers(move_negations(remove_conditionals(formula)))
