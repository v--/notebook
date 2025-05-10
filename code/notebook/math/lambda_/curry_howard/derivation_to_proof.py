from typing import override

from ....parsing import GreekIdentifier
from ...logic.alphabet import BinaryConnective, PropConstant
from ...logic.deduction import proof_tree as ptree
from ...logic.deduction.classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ...logic.deduction.markers import Marker
from ...logic.formulas import ConnectiveFormula, ConstantFormula, Formula, FormulaPlaceholder, PredicateFormula
from ...logic.instantiation import FormalLogicSchemaInstantiation
from ..alphabet import BinaryTypeConnective
from ..instantiation import LambdaSchemaInstantiation
from ..type_derivation import tree as dtree
from ..type_system.explicit import EXPLICIT_SIMPLE_TYPE_SYSTEM
from ..types import BaseType, SimpleConnectiveType, SimpleType, TypePlaceholder, TypeVisitor
from .exceptions import DerivationToProofError


def type_connective_to_formula_connective(conn: BinaryTypeConnective) -> BinaryConnective:
    match conn:
        case BinaryTypeConnective.ARROW:
            return BinaryConnective.CONDITIONAL

        case BinaryTypeConnective.PROD:
            return BinaryConnective.CONJUNCTION

        case BinaryTypeConnective.SUM:
            return BinaryConnective.DISJUNCTION


class TypeToFormulaVisitor(TypeVisitor[Formula]):
    @override
    def visit_base(self, type_: BaseType) -> ConstantFormula | PredicateFormula:
        match type_.name:
            case '1':
                return ConstantFormula(PropConstant.VERUM)

            case '0':
                return ConstantFormula(PropConstant.FALSUM)

            case _:
                return PredicateFormula(type_.name, arguments=[])

    @override
    def visit_connective(self, type_: SimpleConnectiveType) -> ConnectiveFormula:
        return ConnectiveFormula(
            type_connective_to_formula_connective(type_.conn),
            self.visit(type_.a),
            self.visit(type_.b)
        )


def type_to_formula(type_: SimpleType) -> Formula:
    return TypeToFormulaVisitor().visit(type_)


def type_derivation_premise_to_proof_tree_premise(premise: dtree.RuleApplicationPremise) -> ptree.RuleApplicationPremise:
    if premise.discharge:
        return ptree.premise(
            tree=type_derivation_to_proof_tree(premise.tree),
            discharge=type_to_formula(premise.discharge.type),
            marker=Marker(premise.discharge.term.identifier),
        )

    return ptree.premise(
        tree=type_derivation_to_proof_tree(premise.tree)
    )


def lambda_instantiation_to_logic_instantiation(instantiation: LambdaSchemaInstantiation) -> FormalLogicSchemaInstantiation:
    return FormalLogicSchemaInstantiation(
        formula_mapping={
            FormulaPlaceholder(placeholder.identifier): type_to_formula(type_)
            for placeholder, type_ in instantiation.type_mapping.items()
        }
    )


def type_derivation_premise_to_proof_tree_rule(rule_name: str) -> str:
    if rule_name == '0₋':
        return 'EFQ'

    match rule_name[0]:
        case '1':
            return '⊤' + rule_name[1:]

        case '×':
            return '∧' + rule_name[1:]

        case '+':
            return '∨' + rule_name[1:]

        case '→':
            return rule_name

        case _:
            raise DerivationToProofError(f'Unrecognized rule {rule_name!r}')


def translate_instantiation(instantiation: LambdaSchemaInstantiation, **kwargs: str) -> FormalLogicSchemaInstantiation:
    return FormalLogicSchemaInstantiation(
        formula_mapping={
            FormulaPlaceholder(GreekIdentifier(value)):
                type_to_formula(instantiation.type_mapping[TypePlaceholder(GreekIdentifier(key))])

            for key, value in kwargs.items()
        }
    )


def type_derivation_to_proof_tree(derivation: dtree.TypeDerivationTree) -> ptree.ProofTree:
    if isinstance(derivation, dtree.AssumptionTree):
        return ptree.assume(
            type_to_formula(derivation.conclusion.type),
            Marker(derivation.conclusion.term.identifier),
        )

    if not isinstance(derivation, dtree.RuleApplicationTree):
        raise DerivationToProofError('Unrecognized derivation tree')

    if derivation.system != EXPLICIT_SIMPLE_TYPE_SYSTEM:
        raise DerivationToProofError('Unrecognized type system')

    premises = [
        type_derivation_premise_to_proof_tree_premise(premise)
        for premise in derivation.premises
    ]

    match derivation.rule_name:
        case '0₋':
            return ptree.apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM, 'EFQ',
                *premises,
                instantiation=translate_instantiation(derivation.instantiation, τ='φ')
            )

        case '+₊ₗ':
            return ptree.apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM, '∨₊ₗ',
                *premises,
                instantiation=translate_instantiation(derivation.instantiation, σ='ψ')
            )

        case '+₊ᵣ':
            return ptree.apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM, '∨₊ᵣ',
                *premises,
                instantiation=translate_instantiation(derivation.instantiation, τ='φ')
            )

        case _:
            return ptree.apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM,
                type_derivation_premise_to_proof_tree_rule(derivation.rule_name),
                *premises,
            )
