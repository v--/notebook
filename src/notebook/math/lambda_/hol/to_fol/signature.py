from typing import TYPE_CHECKING, override

from .....support.coderefs import collector
from .....support.name_collision import get_name_without_collision
from .....support.unicode import itoa_superscripts
from ....logic.signature import (
    FormalLogicSignature,
    FunctionSymbol,
    PredicateSymbol,
    SignatureSymbol,
    SignatureSymbolNotation,
)
from ...types import BaseType, SimpleConnectiveType, SimpleType, TypeVisitor
from ..signature import HolSignature, NonLogicalConstantSymbol
from ..type_features import extract_bound_types, get_type_arity, is_predicate_type


if TYPE_CHECKING:
    from collections.abc import Mapping

    from ..expression import HolExpression


class SymbolNameVisitor(TypeVisitor[str]):
    @override
    def visit_base(self, type_: BaseType) -> str:
        return type_.value.name

    @override
    def visit_connective(self, type_: SimpleConnectiveType) -> str:
        return self.visit(type_.left) + self.visit(type_.right)


def get_symbol_name(type_: SimpleType) -> str:
    return SymbolNameVisitor().visit(type_)


class FolTranslatedSignature(FormalLogicSignature):
    type_predicates: Mapping[SimpleType, PredicateSymbol]
    type_appliers: Mapping[tuple[SimpleType, int], SignatureSymbol]
    nl_constant_map: Mapping[tuple[NonLogicalConstantSymbol, int], SignatureSymbol]

    def __init__(
        self,
        type_predicates: Mapping[SimpleType, PredicateSymbol],
        type_appliers: Mapping[tuple[SimpleType, int], SignatureSymbol],
        nl_constant_map: Mapping[tuple[NonLogicalConstantSymbol, int], SignatureSymbol],
        *symbols: SignatureSymbol,
    ) -> None:
        super().__init__(*symbols)
        self.type_predicates = type_predicates
        self.type_appliers = type_appliers
        self.nl_constant_map = nl_constant_map


@collector.ref('alg:hol_to_fol/signature')
def hol_signature_to_fol(hol_signature: HolSignature, hol_expression: HolExpression) -> FolTranslatedSignature:
    type_predicates = dict[SimpleType, PredicateSymbol]()
    type_appliers = dict[tuple[SimpleType, int], SignatureSymbol]()
    nl_constant_map = dict[tuple[NonLogicalConstantSymbol, int], SignatureSymbol]()
    translated = FolTranslatedSignature(type_predicates, type_appliers, nl_constant_map)

    for type_ in extract_bound_types(hol_expression.term):
        new_name = get_name_without_collision(
            '?' + str(type_),
            {sym.name for sym in translated},
        )

        pred_sym = PredicateSymbol(new_name, 1, SignatureSymbolNotation.PREFIX)
        translated.add_symbol(pred_sym)
        type_predicates[type_] = pred_sym

        is_predicate = is_predicate_type(type_)

        for i in range(get_type_arity(type_) + 1):
            new_name = get_name_without_collision(
                '!' + str(type_) + itoa_superscripts(i),
                {sym.name for sym in translated},
            )

            notation = SignatureSymbolNotation.PREFIX if i > 0 else SignatureSymbolNotation.CONDENSED
            app_sym = PredicateSymbol(new_name, i + 1, notation) if is_predicate else FunctionSymbol(new_name, i + 1, notation)
            translated.add_symbol(app_sym)
            type_appliers[type_, i] = app_sym

    for nl_sym in hol_signature.iter_nonlogical():
        for i in range(get_type_arity(nl_sym.type) + 1):
            new_name = get_name_without_collision(
                nl_sym.name + itoa_superscripts(i),
                {sym.name for sym in translated},
            )

            is_predicate = is_predicate_type(nl_sym.type)
            notation = SignatureSymbolNotation.PREFIX if i > 0 else SignatureSymbolNotation.CONDENSED
            fol_sym = PredicateSymbol(new_name, i, notation) if is_predicate else FunctionSymbol(new_name, i, notation)
            translated.add_symbol(fol_sym)
            nl_constant_map[nl_sym, i] = fol_sym

    return translated
