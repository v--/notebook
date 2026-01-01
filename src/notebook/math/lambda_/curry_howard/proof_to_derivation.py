from typing import override

from ....parsing import GreekIdentifier
from ...logic.alphabet import BinaryConnective, PropConstantSymbol
from ...logic.classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ...logic.deduction import NaturalDeductionRule, UnknownNaturalDeductionRuleError
from ...logic.deduction import proof_tree as ptree
from ...logic.formulas import (
    ConnectiveFormula,
    Formula,
    FormulaPlaceholder,
    FormulaVisitor,
    PredicateApplication,
    PropConstant,
)
from ...logic.instantiation import AtomicLogicSchemaInstantiation
from ..algebraic_types import SIMPLE_ALGEBRAIC_TYPE_SYSTEM
from ..alphabet import BinaryTypeConnective
from ..assertions import VariableTypeAssertion
from ..instantiation import AtomicLambdaSchemaInstantiation
from ..parsing import parse_type_variable
from ..terms import Variable
from ..type_derivation import tree as dtree
from ..type_system import TypingRule
from ..types import (
    BaseType,
    SimpleConnectiveType,
    SimpleType,
    TypePlaceholder,
    TypeVariable,
)
from .exceptions import ProofToDerivationError


def formula_connective_to_type_connective(conn: BinaryConnective) -> BinaryTypeConnective:
    match conn:
        case BinaryConnective.CONDITIONAL:
            return BinaryTypeConnective.ARROW

        case BinaryConnective.CONJUNCTION:
            return BinaryTypeConnective.PRODUCT

        case BinaryConnective.DISJUNCTION:
            return BinaryTypeConnective.SUM

        case BinaryConnective.BICONDITIONAL:
            raise ProofToDerivationError('No simple type corresponds to biconditional formulas')


class FormulaToTypeVisitor(FormulaVisitor[SimpleType]):
    @override
    def visit_prop_constant(self, formula: PropConstant) -> BaseType:
        match formula.value:
            case PropConstantSymbol.VERUM:
                return BaseType('𝟙')

            case PropConstantSymbol.FALSUM:
                return BaseType('𝟘')

    @override
    def visit_predicate(self, formula: PredicateApplication) -> TypeVariable:
        if len(formula.arguments) > 0:
            raise ProofToDerivationError('Only nullary predicates can be converted to types')

        # We encode propositional variables as nullary predicates
        # As per rem:curry_howard_variables, we adjust our predicates so that they match the syntax of type variables
        return parse_type_variable(formula.symbol.name)

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> SimpleType:
        return SimpleConnectiveType(
            formula_connective_to_type_connective(formula.conn),
            self.visit(formula.left),
            self.visit(formula.right)
        )

    @override
    def generic_visit(self, formula: Formula) -> SimpleType:
        raise ProofToDerivationError('Can only convert propositional formulas to types')


def formula_to_type(formula: Formula) -> SimpleType:
    return FormulaToTypeVisitor().visit(formula)


def proof_tree_premise_to_derivation_tree_premise(premise: ptree.RuleApplicationPremise) -> dtree.RuleApplicationPremise:
    if premise.discharge and premise.marker:
        return dtree.premise(
            tree=proof_tree_to_type_derivation(premise.tree),
            discharge=VariableTypeAssertion(
                Variable(premise.marker.identifier),
                formula_to_type(premise.discharge.formula)
            )
        )

    return dtree.premise(
        tree=proof_tree_to_type_derivation(premise.tree)
    )


def natural_deduction_rule_to_typing_rule(rule: NaturalDeductionRule) -> TypingRule:
    if rule == CLASSICAL_NATURAL_DEDUCTION_SYSTEM['EFQ']:
        return SIMPLE_ALGEBRAIC_TYPE_SYSTEM['𝟘₋']

    prefix = rule.name[0]
    suffix = rule.name[1:]

    match prefix:
        case '⊤' if rule == CLASSICAL_NATURAL_DEDUCTION_SYSTEM[rule.name]:
            return SIMPLE_ALGEBRAIC_TYPE_SYSTEM['𝟙' + suffix]

        case '∧' if rule == CLASSICAL_NATURAL_DEDUCTION_SYSTEM[rule.name]:
            return SIMPLE_ALGEBRAIC_TYPE_SYSTEM['×' + suffix]

        case '∨' if rule == CLASSICAL_NATURAL_DEDUCTION_SYSTEM[rule.name]:
            return SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+' + suffix]

        case '→' if rule == CLASSICAL_NATURAL_DEDUCTION_SYSTEM[rule.name]:
            return SIMPLE_ALGEBRAIC_TYPE_SYSTEM[rule.name]

        case _:
            raise UnknownNaturalDeductionRuleError(rule)


def translate_instantiation(instantiation: AtomicLogicSchemaInstantiation, **kwargs: str) -> AtomicLambdaSchemaInstantiation:
    return AtomicLambdaSchemaInstantiation(
        type_mapping={
            TypePlaceholder(GreekIdentifier(value)):
                formula_to_type(instantiation.formula_mapping[FormulaPlaceholder(GreekIdentifier(key))])

            for key, value in kwargs.items()
        }
    )


# This is alg:proof_tree_to_type_derivation in the monograph
def proof_tree_to_type_derivation(proof: ptree.ProofTree) -> dtree.TypeDerivationTree:
    if isinstance(proof, ptree.AssumptionTree):
        return dtree.assume(
            VariableTypeAssertion(
                Variable(proof.marker.identifier),
                formula_to_type(proof.conclusion.formula)
            )
        )

    if not isinstance(proof, ptree.RuleApplicationTree):
        raise ProofToDerivationError('Unrecognized proof tree')

    premises = [
        proof_tree_premise_to_derivation_tree_premise(premise)
        for premise in proof.premises
    ]

    match proof.rule.name:
        case 'EFQ':
            return dtree.apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['𝟘₋'],
                *premises,
                instantiation=translate_instantiation(proof.instantiation, φ='τ')
            )

        case '∨₊ₗ':
            return dtree.apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₊ₗ'],
                *premises,
                instantiation=translate_instantiation(proof.instantiation, ψ='σ')
            )

        case '∨₊ᵣ':
            return dtree.apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₊ᵣ'],
                *premises,
                instantiation=translate_instantiation(proof.instantiation, φ='τ')
            )

        case _:
            return dtree.apply(
                natural_deduction_rule_to_typing_rule(proof.rule),
                *premises,
            )
