from typing import NamedTuple, TypeGuard

from ...parsing.identifiers import GreekIdentifier
from .alphabet import BinaryConnective, PropConstant, Quantifier, SchemaConnective, UnaryConnective
from .terms import FunctionLikeTerm, Term, TermSchema, Variable, VariablePlaceholder


class ConstantFormula(NamedTuple):
    value: PropConstant

    def __str__(self) -> str:
        return str(self.value)


class EqualityFormula(NamedTuple):
    a: Term
    b: Term

    def __str__(self) -> str:
        return f'({self.a} = {self.b})'


class PredicateFormula(FunctionLikeTerm['Term']):
    pass


class NegationFormula(NamedTuple):
    sub: 'Formula'

    def __str__(self) -> str:
        return f'{UnaryConnective.negation}{self.sub}'


class ConnectiveFormula(NamedTuple):
    conn: BinaryConnective
    a: 'Formula'
    b: 'Formula'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


class QuantifierFormula(NamedTuple):
    quantifier: Quantifier
    variable: Variable
    sub: 'Formula'

    def __str__(self) -> str:
        return f'{self.quantifier.value}{self.variable}.{self.sub}'


Formula = ConstantFormula | EqualityFormula | PredicateFormula | NegationFormula | ConnectiveFormula | QuantifierFormula


def is_atomic(formula: Formula) -> TypeGuard[ConstantFormula | EqualityFormula | PredicateFormula]:
    return isinstance(formula, ConstantFormula | EqualityFormula | PredicateFormula)


def is_disjunction(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.disjunction


def is_conjunction(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.conjunction


def is_conditional(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.conditional


def is_biconditional(formula: Formula) -> TypeGuard[ConnectiveFormula]:
    return isinstance(formula, ConnectiveFormula) and formula.conn == BinaryConnective.biconditional


def is_subformula(formula: Formula, subformula: Formula) -> bool:
    if formula == subformula:
        return True

    match formula:
        case NegationFormula():
            return is_subformula(formula.sub, subformula)

        case ConnectiveFormula():
            return is_subformula(formula.a, subformula) or is_subformula(formula.b, subformula)

        case QuantifierFormula():
            return is_subformula(formula.sub, subformula)

    return False


class FormulaPlaceholder(NamedTuple):
    identifier: GreekIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


class EqualityFormulaSchema(NamedTuple):
    a: TermSchema
    b: TermSchema

    def __str__(self) -> str:
        return f'({self.a} = {self.b})'


class NegationFormulaSchema(NamedTuple):
    sub: 'FormulaSchema'

    def __str__(self) -> str:
        return f'{UnaryConnective.negation}{self.sub}'


class ConnectiveFormulaSchema(NamedTuple):
    conn: BinaryConnective
    a: 'FormulaSchema'
    b: 'FormulaSchema'

    def __str__(self) -> str:
        return f'({self.a} {self.conn} {self.b})'


class QuantifierFormulaSchema(NamedTuple):
    quantifier: Quantifier
    variable: VariablePlaceholder
    sub: 'FormulaSchema'

    def __str__(self) -> str:
        return f'{self.quantifier.value}{self.variable}.{self.sub}'


FormulaSchema = FormulaPlaceholder | ConstantFormula | EqualityFormulaSchema | NegationFormulaSchema | ConnectiveFormulaSchema | QuantifierFormulaSchema


class StarredTermSchema(NamedTuple):
    term: TermSchema

    def __str__(self) -> str:
        return f'{self.term}*'


class SubstitutionSchema(NamedTuple):
    formula: FormulaSchema
    var: VariablePlaceholder
    dest: StarredTermSchema

    def __str__(self) -> str:
        return f'{self.formula}[{self.var} {SchemaConnective.substitution} {self.dest}]'


ExtendedFormulaSchema = FormulaSchema | SubstitutionSchema
