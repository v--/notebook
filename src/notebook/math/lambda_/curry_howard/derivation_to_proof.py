from typing import TYPE_CHECKING, override

from notebook.math.lambda_.algebraic_types import SIMPLE_ALGEBRAIC_TYPE_SYSTEM
from notebook.math.lambda_.alphabet import BinaryTypeConnective
from notebook.math.lambda_.type_derivation import UnknownDerivationRuleError
from notebook.math.lambda_.type_derivation import tree as dtree
from notebook.math.lambda_.types import (
    BaseType,
    SimpleConnectiveType,
    SimpleType,
    TypePlaceholder,
    TypeVariable,
    TypeVisitor,
)
from notebook.math.logic.alphabet import BinaryConnective, PropConstantSymbol
from notebook.math.logic.classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from notebook.math.logic.deduction import MarkedFormula, Marker, NaturalDeductionRule
from notebook.math.logic.deduction import proof_tree as ptree
from notebook.math.logic.formulas import (
    ConnectiveFormula,
    Formula,
    FormulaPlaceholder,
    PredicateApplication,
    PropConstant,
)
from notebook.math.logic.instantiation import AtomicLogicSchemaInstantiation
from notebook.math.logic.propositional import PropVariableSymbol
from notebook.parsing import GreekIdentifier
from notebook.support.coderefs import collector

from .exceptions import DerivationToProofError


if TYPE_CHECKING:
    from notebook.math.lambda_.instantiation import AtomicLambdaSchemaInstantiation
    from notebook.math.lambda_.type_system import TypingRule


def type_connective_to_formula_connective(conn: BinaryTypeConnective) -> BinaryConnective:
    match conn:
        case BinaryTypeConnective.ARROW:
            return BinaryConnective.CONDITIONAL

        case BinaryTypeConnective.PRODUCT:
            return BinaryConnective.CONJUNCTION

        case BinaryTypeConnective.SUM:
            return BinaryConnective.DISJUNCTION


class TypeToFormulaVisitor(TypeVisitor[Formula]):
    @override
    def visit_base(self, type_: BaseType) -> PropConstant:
        match type_.value.name:
            case '𝟙':
                return PropConstant(PropConstantSymbol.VERUM)

            case '𝟘':
                return PropConstant(PropConstantSymbol.FALSUM)

            case _:
                raise DerivationToProofError(f'Unrecognized base type {type_!r}')

    @override
    def visit_variable(self, type_: TypeVariable) -> PredicateApplication:
        # We have not implemented a dedicated syntax for propositional logic
        # We treat propositional variables as nullary predicates
        # As per rem:curry_howard_variables, we adjust our predicates so that they match the syntax of type variables
        return PredicateApplication(PropVariableSymbol(str(type_.identifier)), [])

    @override
    def visit_connective(self, type_: SimpleConnectiveType) -> ConnectiveFormula:
        return ConnectiveFormula(
            type_connective_to_formula_connective(type_.conn),
            self.visit(type_.left),
            self.visit(type_.right),
        )


def type_to_formula(type_: SimpleType) -> Formula:
    return TypeToFormulaVisitor().visit(type_)


def type_derivation_premise_to_proof_tree_premise(premise: dtree.RuleApplicationPremise) -> ptree.RuleApplicationPremiseConfig:
    return ptree.premise_config(
        tree=type_derivation_to_proof_tree(premise.tree),
        attachments=[
            MarkedFormula(
                type_to_formula(att.type),
                Marker(att.term.identifier),
            ) if att else None
            for att in premise.attachments
        ],
    )


def lambda_instantiation_to_logic_instantiation(instantiation: AtomicLambdaSchemaInstantiation) -> AtomicLogicSchemaInstantiation:
    return AtomicLogicSchemaInstantiation(
        formula_mapping={
            FormulaPlaceholder(placeholder.identifier): type_to_formula(type_)
            for placeholder, type_ in instantiation.type_mapping.items()
        },
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


def translate_instantiation(instantiation: AtomicLambdaSchemaInstantiation, **kwargs: str) -> AtomicLogicSchemaInstantiation:
    return AtomicLogicSchemaInstantiation(
        formula_mapping={
            FormulaPlaceholder(GreekIdentifier(value)):
                type_to_formula(instantiation.type_mapping[TypePlaceholder(GreekIdentifier(key))])

            for key, value in kwargs.items()
        },
    )


def translate_application(
    derivation: dtree.RuleApplicationTree,
    rule: NaturalDeductionRule,
    **kwargs: str,
) -> ptree.RuleApplicationTree:
    instantiation = translate_instantiation(derivation.instantiation, **kwargs)
    return ptree.apply(
        rule,
        *(
            type_derivation_premise_to_proof_tree_premise(premise)
            for premise in derivation.premises
        ),
        instantiation=instantiation,
    )


@collector.ref('alg:type_derivation_to_proof_tree')
def type_derivation_to_proof_tree(derivation: dtree.TypeDerivationTree) -> ptree.ProofTree:
    if isinstance(derivation, dtree.AssumptionTree):
        return ptree.assume(
            type_to_formula(derivation.conclusion.type),
            Marker(derivation.conclusion.term.identifier),
        )

    if not isinstance(derivation, dtree.RuleApplicationTree):
        raise DerivationToProofError('Unrecognized derivation tree')

    match derivation.rule.name:
        case '𝟘₋':
            return translate_application(
                derivation,
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['EFQ'],
                τ='φ',
            )

        case '+₊ₗ':
            return translate_application(
                derivation,
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨₊ₗ'],
                σ='ψ',
            )

        case '+₊ᵣ':
            return translate_application(
                derivation,
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨₊ᵣ'],
                τ='φ',
            )

        case _:
            return translate_application(
                derivation,
                typing_rule_to_natural_deduction_rule(derivation.rule),
            )
