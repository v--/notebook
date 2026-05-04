from typing import TYPE_CHECKING, cast, overload

from notebook.exceptions import UnreachableException
from notebook.math.lambda_.hol import common
from notebook.math.lambda_.hol.exceptions import HolTranslationError
from notebook.math.lambda_.hol.signature import HolSignature, NonLogicalConstantSymbol
from notebook.math.lambda_.terms import Constant, TypedAbstraction, TypedApplication, TypedTerm
from notebook.math.lambda_.terms import Variable as LambdaVariable
from notebook.math.lambda_.variables import is_closed_term
from notebook.math.logic.alphabet import BinaryConnective, PropConstantSymbol, Quantifier
from notebook.math.logic.formulas import (
    ConnectiveFormula,
    EqualityFormula,
    NegationFormula,
    PredicateApplication,
    PropConstant,
    QuantifierFormula,
)
from notebook.math.logic.formulas import Formula as FolFormula
from notebook.math.logic.signature import FunctionSymbol, PredicateSymbol, SignatureSymbol
from notebook.math.logic.terms import FunctionApplication
from notebook.math.logic.terms import Term as FolTerm
from notebook.math.logic.terms import Variable as FolVariable
from notebook.support.coderefs import collector

from .signature import FolTranslatedSignature, hol_signature_to_fol


if TYPE_CHECKING:
    from collections.abc import Sequence

    from notebook.math.lambda_.hol.expression import HolExpression
    from notebook.math.lambda_.type_context import TypeContext


def logical_constant_to_connective(const: Constant) -> BinaryConnective:
    match const:
        case common.conjunction:
            return BinaryConnective.CONJUNCTION

        case common.disjunction:
            return BinaryConnective.DISJUNCTION

        case common.conditional:
            return BinaryConnective.CONDITIONAL

        case common.biconditional:
            return BinaryConnective.BICONDITIONAL

        case _:
            raise UnreachableException


def logical_constant_to_quantifier(const: Constant) -> Quantifier:
    match const:
        case common.forall:
            return Quantifier.UNIVERSAL

        case common.exists:
            return Quantifier.EXISTENTIAL

        case _:
            raise UnreachableException


def to_fol_application(fol_sym: SignatureSymbol, *args: FolTerm | FolFormula) -> FolTerm | FolFormula:
    if not all(isinstance(arg, FolTerm) for arg in args):
        raise HolTranslationError('The arguments of a function application must be first-order terms')

    args_ = cast('Sequence[FolTerm]', list(args))

    match fol_sym:
        case FunctionSymbol():
            return FunctionApplication(fol_sym, args_)

        case PredicateSymbol():
            return PredicateApplication(fol_sym, args_)

        case _:
            raise HolTranslationError(f'Unrecognized symbol {fol_sym}')


def construct_application(  # noqa: C901
    signature: FolTranslatedSignature,
    context: TypeContext,
    term: TypedTerm,
    *args: FolTerm | FolFormula,
) -> FolTerm | FolFormula:
    match term:
        case TypedApplication():
            return construct_application(
                signature,
                context,
                term.left,
                *args,
                translate_hol_expression(signature, context, term.right),
            )

        case LambdaVariable():
            sym = signature.type_appliers[context[term], len(args)]
            return to_fol_application(sym, translate_hol_expression(signature, context, term), *args)

        case Constant() if isinstance(term.value, NonLogicalConstantSymbol):
            sym = signature.nl_constant_map[term.value, len(args)]
            return to_fol_application(sym, *args)

        case common.verum:
            if len(args) > 0:
                raise HolTranslationError('A verum cannot have arguments')

            return PropConstant(PropConstantSymbol.VERUM)

        case common.falsum:
            if len(args) > 0:
                raise HolTranslationError('A falsum cannot have arguments')

            return PropConstant(PropConstantSymbol.FALSUM)

        case common.negation:
            if len(args) != 1 or not isinstance(args[0], FolFormula):
                raise HolTranslationError('A negation must have exactly one formula as an argument')

            return NegationFormula(args[0])

        case common.conjunction | common.disjunction | common.conditional | common.biconditional:
            if len(args) != 2 or not isinstance(args[0], FolFormula) or not isinstance(args[1], FolFormula):
                raise HolTranslationError('A connective formula must have exactly two formulas as arguments')

            return ConnectiveFormula(
                logical_constant_to_connective(term),
                args[0],
                args[1],
            )

        case common.equality:
            if len(args) != 2 or not isinstance(args[0], FolTerm) or not isinstance(args[1], FolTerm):
                raise HolTranslationError('An equality formula must have exactly two first-order terms as arguments')

            return EqualityFormula(args[0], args[1])

        case Constant():
            raise HolTranslationError(f'Unexpected {term.value.get_kind_string()} {term.value}')

        case _:
            raise HolTranslationError(f'Unexpected λ-term {term}')


@overload
def translate_hol_expression[T](
    signature: FolTranslatedSignature,
    context: TypeContext,
    term: LambdaVariable,
) -> FolVariable: ...
@overload
def translate_hol_expression[T](
    signature: FolTranslatedSignature,
    context: TypeContext,
    term: TypedTerm,
) -> FolTerm | FolFormula: ...
def translate_hol_expression[T](
    signature: FolTranslatedSignature,
    context: TypeContext,
    term: TypedTerm,
) -> FolTerm | FolFormula:
    match term:
        case LambdaVariable():
            return FolVariable(term.identifier)

        case Constant():
            return construct_application(signature, context, term)

        case TypedApplication():
            if term.left == common.forall or term.left == common.exists:
                if TYPE_CHECKING:
                    assert isinstance(term.left, Constant)
                    assert isinstance(term.right, TypedAbstraction)

                translated_var = translate_hol_expression(signature, context, term.right.var)
                translated_body = translate_hol_expression(
                    signature,
                    context.modify(term.right.var, term.right.var_type),
                    term.right.body,
                )

                if not isinstance(translated_body, FolFormula):
                    raise HolTranslationError(f'The body of a quantifier must translate to a formula, not {translated_body}')

                return QuantifierFormula(
                    logical_constant_to_quantifier(term.left),
                    translated_var,
                    ConnectiveFormula(
                        BinaryConnective.CONDITIONAL if term.left == common.forall else BinaryConnective.CONJUNCTION,
                        PredicateApplication(signature.type_predicates[term.right.var_type], [translated_var]),
                        translated_body,
                    ),
                )

            return construct_application(signature, context, term)

        case TypedAbstraction():
            raise HolTranslationError(f'Unexpected raw abstraction {term}')

        case _:
            raise HolTranslationError(f'Unexpected λ-term {term}')


@collector.ref('alg:hol_to_fol/expression')
def hol_expression_to_fol(signature: HolSignature, expression: HolExpression) -> FolTerm | FolFormula:
    if not is_closed_term(expression.term):
        raise HolTranslationError(f'Expected a closed term, but got {expression.term}')

    translated_signature = hol_signature_to_fol(signature, expression)
    return translate_hol_expression(translated_signature, expression.context, expression.term)
