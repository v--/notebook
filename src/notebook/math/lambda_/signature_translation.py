from dataclasses import dataclass, field
from typing import TYPE_CHECKING, override

from ...support.coderefs import collector
from .terms import Constant, TypedAbstraction, TypedApplication, TypedTerm, TypedTermVisitor, Variable
from .types import BaseType, SimpleConnectiveType, SimpleType, TypeVariable, TypeVisitor


if TYPE_CHECKING:
    from .signature import SignatureMorphism


@dataclass
class TypeTranslationVisitor(TypeVisitor[SimpleType]):
    translation: SignatureMorphism

    @override
    def visit_base(self, type_: BaseType) -> BaseType:
        return BaseType(self.translation(type_.value))

    @override
    def visit_variable(self, type_: TypeVariable) -> TypeVariable:
        return type_

    @override
    def visit_connective(self, type_: SimpleConnectiveType) -> SimpleConnectiveType:
        return SimpleConnectiveType(
            type_.conn,
            self.visit(type_.left),
            self.visit(type_.right),
        )


@collector.ref('alg:fol_formula_signature_translation')
def translate_type(translation: SignatureMorphism, type_: SimpleType) -> SimpleType:
    return TypeTranslationVisitor(translation).visit(type_)


@dataclass
class TermTranslationVisitor(TypedTermVisitor[TypedTerm]):
    translation: SignatureMorphism
    type_visitor: TypeTranslationVisitor = field(init=False)

    def __post_init__(self) -> None:
        self.type_visitor = TypeTranslationVisitor(self.translation)

    @override
    def visit_constant(self, term: Constant) -> Constant:
        return Constant(self.translation(term.value))

    @override
    def visit_variable(self, term: Variable) -> Variable:
        return term

    @override
    def visit_application(self, term: TypedApplication) -> TypedApplication:
        return TypedApplication(
            self.visit(term.left),
            self.visit(term.right),
        )

    @override
    def visit_abstraction(self, term: TypedAbstraction) -> TypedAbstraction:
        return TypedAbstraction(
            term.var,
            self.type_visitor.visit(term.var_type),
            self.visit(term.body),
        )


@collector.ref('alg:fol_term_signature_translation')
def translate_term(translation: SignatureMorphism, term: TypedTerm) -> TypedTerm:
    return TermTranslationVisitor(translation).visit(term)
