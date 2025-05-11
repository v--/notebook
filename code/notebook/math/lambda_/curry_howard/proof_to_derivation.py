from typing import override

from ....parsing import GreekIdentifier
from ...logic.alphabet import BinaryConnective, PropConstant
from ...logic.deduction import proof_tree as ptree
from ...logic.deduction.classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ...logic.formulas import (
    ConnectiveFormula,
    ConstantFormula,
    Formula,
    FormulaPlaceholder,
    FormulaVisitor,
    PredicateFormula,
)
from ...logic.instantiation import FormalLogicSchemaInstantiation
from ..alphabet import BinaryTypeConnective
from ..assertions import VariableTypeAssertion
from ..instantiation import LambdaSchemaInstantiation
from ..terms import Variable
from ..type_derivation import tree as dtree
from ..type_system.explicit import SIMPLE_ALGEBRAIC_TYPE_SYSTEM
from ..types import BaseType, SimpleConnectiveType, SimpleType, TypePlaceholder
from .exceptions import ProofToDerivationError


def formula_connective_to_type_connective(conn: BinaryConnective) -> BinaryTypeConnective:
    match conn:
        case BinaryConnective.CONDITIONAL:
            return BinaryTypeConnective.ARROW

        case BinaryConnective.CONJUNCTION:
            return BinaryTypeConnective.PROD

        case BinaryConnective.DISJUNCTION:
            return BinaryTypeConnective.SUM

        case BinaryConnective.BICONDITIONAL:
            raise ProofToDerivationError('Biconditional formulas have no equivalent type')


class FormulaToTypeVisitor(FormulaVisitor[SimpleType]):
    @override
    def visit_constant(self, formula: ConstantFormula) -> BaseType:
        match formula.value:
            case PropConstant.VERUM:
                return BaseType('1')

            case PropConstant.FALSUM:
                return BaseType('0')

    @override
    def visit_predicate(self, formula: PredicateFormula) -> BaseType:
        if len(formula.arguments) > 0:
            raise ProofToDerivationError('Only nullary predicates can be converted to types')

        return BaseType(formula.name)

    @override
    def visit_connective(self, formula: ConnectiveFormula) -> SimpleType:
        return SimpleConnectiveType(
            formula_connective_to_type_connective(formula.conn),
            self.visit(formula.a),
            self.visit(formula.b)
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
                formula_to_type(premise.discharge)
            )
        )

    return dtree.premise(
        tree=proof_tree_to_type_derivation(premise.tree)
    )


def proof_tree_premise_to_derivation_tree_rule(rule_name: str) -> str:
    if rule_name == 'EFQ':
        return '0₋'

    match rule_name[0]:
        case '⊤':
            return '1' + rule_name[1:]

        case '∧':
            return '×' + rule_name[1:]

        case '∨':
            return '+' + rule_name[1:]

        case '→':
            return rule_name

        case _:
            raise ProofToDerivationError(f'Unrecognized rule {rule_name!r}')


def translate_instantiation(instantiation: FormalLogicSchemaInstantiation, **kwargs: str) -> LambdaSchemaInstantiation:
    return LambdaSchemaInstantiation(
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
                formula_to_type(proof.conclusion)
            )
        )

    if not isinstance(proof, ptree.RuleApplicationTree):
        raise ProofToDerivationError('Unrecognized proof tree')

    if proof.system != CLASSICAL_NATURAL_DEDUCTION_SYSTEM:
        raise ProofToDerivationError('Unrecognized type system')

    premises = [
        proof_tree_premise_to_derivation_tree_premise(premise)
        for premise in proof.premises
    ]

    match proof.rule_name:
        case 'EFQ':
            return dtree.apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM, '0₋',
                *premises,
                instantiation=translate_instantiation(proof.instantiation, φ='τ')
            )

        case '∨₊ₗ':
            return dtree.apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM, '+₊ₗ',
                *premises,
                instantiation=translate_instantiation(proof.instantiation, ψ='σ')
            )

        case '∨₊ᵣ':
            return dtree.apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM, '+₊ᵣ',
                *premises,
                instantiation=translate_instantiation(proof.instantiation, φ='τ')
            )

        case _:
            return dtree.apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM,
                proof_tree_premise_to_derivation_tree_rule(proof.rule_name),
                *premises,
            )
