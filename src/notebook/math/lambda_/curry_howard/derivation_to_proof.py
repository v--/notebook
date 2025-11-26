from typing import override

from ....parsing import GreekIdentifier
from ...logic.alphabet import BinaryConnective, PropConstant
from ...logic.classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ...logic.deduction import Marker, NaturalDeductionRule
from ...logic.deduction import proof_tree as ptree
from ...logic.formulas import ConnectiveFormula, ConstantFormula, Formula, FormulaPlaceholder, PredicateApplication
from ...logic.instantiation import FormalLogicSchemaInstantiation
from ...logic.propositional import PropositionalVariable
from ..algebraic_types import SIMPLE_ALGEBRAIC_TYPE_SYSTEM
from ..alphabet import BinaryTypeConnective
from ..instantiation import LambdaSchemaInstantiation
from ..type_derivation import UnknownDerivationRuleError
from ..type_derivation import tree as dtree
from ..type_system import TypingRule
from ..types import BaseType, SimpleConnectiveType, SimpleType, TypePlaceholder, TypeVariable, TypeVisitor
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
    def visit_base(self, type_: BaseType) -> ConstantFormula:
        match type_.name:
            case '𝟙':
                return ConstantFormula(PropConstant.VERUM)

            case '𝟘':
                return ConstantFormula(PropConstant.FALSUM)

            case _:
                raise DerivationToProofError(f'Unrecognized base type {type_!r}')

    @override
    def visit_variable(self, type_: TypeVariable) -> PredicateApplication:
        # We have not implemented a dedicated syntax for propositional logic
        # We treat propositional variables as nullary predicates
        # As per rem:curry_howard_variables, we adjust our predicates so that they match the syntax of type variables
        return PredicateApplication(PropositionalVariable(str(type_.identifier)), [])

    @override
    def visit_connective(self, type_: SimpleConnectiveType) -> ConnectiveFormula:
        return ConnectiveFormula(
            type_connective_to_formula_connective(type_.conn),
            self.visit(type_.left),
            self.visit(type_.right)
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


def typing_rule_to_natural_deduction_rule(rule: TypingRule) -> NaturalDeductionRule:
    if rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM['𝟘₋']:
        return CLASSICAL_NATURAL_DEDUCTION_SYSTEM['EFQ']

    prefix = rule.name[0]
    suffix = rule.name[1:]

    match prefix:
        case '𝟙' if rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM[rule.name]:
            return CLASSICAL_NATURAL_DEDUCTION_SYSTEM['⊤' + suffix]

        case '×' if rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM[rule.name]:
            return CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∧' + suffix]

        case '+' if rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM[rule.name]:
            return CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨' + suffix]

        case '→' if rule == SIMPLE_ALGEBRAIC_TYPE_SYSTEM[rule.name]:
            return CLASSICAL_NATURAL_DEDUCTION_SYSTEM[rule.name]

        case _:
            raise UnknownDerivationRuleError(rule)


def translate_instantiation(instantiation: LambdaSchemaInstantiation, **kwargs: str) -> FormalLogicSchemaInstantiation:
    return FormalLogicSchemaInstantiation(
        formula_mapping={
            FormulaPlaceholder(GreekIdentifier(value)):
                type_to_formula(instantiation.type_mapping[TypePlaceholder(GreekIdentifier(key))])

            for key, value in kwargs.items()
        }
    )


# This is alg:type_derivation_to_proof_tree in the monograph
def type_derivation_to_proof_tree(derivation: dtree.TypeDerivationTree) -> ptree.ProofTree:
    if isinstance(derivation, dtree.AssumptionTree):
        return ptree.assume(
            type_to_formula(derivation.conclusion.type),
            Marker(derivation.conclusion.term.identifier),
        )

    if not isinstance(derivation, dtree.RuleApplicationTree):
        raise DerivationToProofError('Unrecognized derivation tree')

    premises = [
        type_derivation_premise_to_proof_tree_premise(premise)
        for premise in derivation.premises
    ]

    match derivation.rule.name:
        case '𝟘₋':
            return ptree.apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['EFQ'],
                *premises,
                instantiation=translate_instantiation(derivation.instantiation, τ='φ')
            )

        case '+₊ₗ':
            return ptree.apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨₊ₗ'],
                *premises,
                instantiation=translate_instantiation(derivation.instantiation, σ='ψ')
            )

        case '+₊ᵣ':
            return ptree.apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨₊ᵣ'],
                *premises,
                instantiation=translate_instantiation(derivation.instantiation, τ='φ')
            )

        case _:
            return ptree.apply(
                typing_rule_to_natural_deduction_rule(derivation.rule),
                *premises,
            )
