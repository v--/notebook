from typing import TYPE_CHECKING, override

from notebook.math.lambda_.algebraic_types import SIMPLE_ALGEBRAIC_TYPE_SYSTEM
from notebook.math.lambda_.alphabet import BinaryTypeConnective
from notebook.math.lambda_.assertions import VariableTypeAssertion
from notebook.math.lambda_.instantiation import AtomicLambdaSchemaInstantiation
from notebook.math.lambda_.parsing import parse_type_variable
from notebook.math.lambda_.signature import BaseTypeSymbol
from notebook.math.lambda_.terms import Variable
from notebook.math.lambda_.type_derivation import tree as dtree
from notebook.math.lambda_.types import BaseType, SimpleConnectiveType, SimpleType, TypePlaceholder, TypeVariable
from notebook.math.logic.alphabet import BinaryConnective, PropConstantSymbol
from notebook.math.logic.classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from notebook.math.logic.deduction import NaturalDeductionRule, UnknownNaturalDeductionRuleError
from notebook.math.logic.deduction import proof_tree as ptree
from notebook.math.logic.formulas import (
    ConnectiveFormula,
    Formula,
    FormulaPlaceholder,
    FormulaVisitor,
    PredicateApplication,
    PropConstant,
)
from notebook.parsing import GreekIdentifier
from notebook.support.coderefs import collector

from .exceptions import ProofToDerivationError


if TYPE_CHECKING:
    from notebook.math.lambda_.type_system import TypingRule
    from notebook.math.logic.instantiation import AtomicLogicSchemaInstantiation


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
                return BaseType(BaseTypeSymbol('𝟙'))

            case PropConstantSymbol.FALSUM:
                return BaseType(BaseTypeSymbol('𝟘'))

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
            self.visit(formula.right),
        )

    @override
    def generic_visit(self, formula: Formula) -> SimpleType:
        raise ProofToDerivationError('Can only convert propositional formulas to types')


def formula_to_type(formula: Formula) -> SimpleType:
    return FormulaToTypeVisitor().visit(formula)


def proof_tree_premise_to_derivation_tree_premise(premise: ptree.RuleApplicationPremise) -> dtree.RuleApplicationPremise:
    return dtree.premise_config(
        tree=proof_tree_to_type_derivation(premise.tree),
        attachments=[
            VariableTypeAssertion(
                Variable(att.marker.identifier),
                formula_to_type(att.formula),
            ) if att else None
            for att in premise.attachments
        ],
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


def create_instantiation(instantiation: AtomicLogicSchemaInstantiation, **kwargs: str) -> AtomicLambdaSchemaInstantiation:
    return AtomicLambdaSchemaInstantiation(
        type_mapping={
            TypePlaceholder(GreekIdentifier(value)):
                formula_to_type(instantiation.formula_mapping[FormulaPlaceholder(GreekIdentifier(key))])

            for key, value in kwargs.items()
        },
    )


def translate_application(
    derivation: ptree.RuleApplicationTree,
    rule: TypingRule,
    **kwargs: str,
) -> dtree.RuleApplicationTree:
    instantiation = create_instantiation(derivation.instantiation, **kwargs)
    return dtree.apply(
        rule,
        *(
            proof_tree_premise_to_derivation_tree_premise(premise)
            for premise in derivation.premises
        ),
        instantiation=instantiation,
    )


@collector.ref('alg:proof_tree_to_type_derivation')
def proof_tree_to_type_derivation(proof: ptree.ProofTree) -> dtree.TypeDerivationTree:
    if isinstance(proof, ptree.AssumptionTree):
        return dtree.assume(
            VariableTypeAssertion(
                Variable(proof.marker.identifier),
                formula_to_type(proof.conclusion),
            ),
        )

    if not isinstance(proof, ptree.RuleApplicationTree):
        raise ProofToDerivationError('Unrecognized proof tree')

    match proof.rule.name:
        case 'EFQ':
            return translate_application(
                proof,
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['𝟘₋'],
                φ='τ',
            )

        case '∨₊ₗ':
            return translate_application(
                proof,
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₊ₗ'],
                ψ='σ',
            )

        case '∨₊ᵣ':
            return translate_application(
                proof,
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₊ᵣ'],
                φ='τ',
            )

        case _:
            return translate_application(
                proof,
                natural_deduction_rule_to_typing_rule(proof.rule),
            )
