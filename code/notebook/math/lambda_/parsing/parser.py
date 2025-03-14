from collections.abc import Iterable, Sequence
from typing import Literal, overload

from ....parsing import IdentifierParserMixin, Parser
from ..alphabet import BinaryTypeConnective, TermConnective
from ..assertions import (
    ExplicitTypeAssertion,
    ExplicitTypeAssertionSchema,
    GradualTypeAssertion,
    GradualTypeAssertionSchema,
    ImplicitTypeAssertion,
    ImplicitTypeAssertionSchema,
    VariableTypeAssertion,
    VariableTypeAssertionSchema,
)
from ..signature import EMPTY_SIGNATURE, LambdaSignature
from ..terms import (
    Constant,
    MixedAbstraction,
    MixedAbstractionSchema,
    MixedApplication,
    MixedApplicationSchema,
    MixedTerm,
    MixedTermSchema,
    TermPlaceholder,
    TypedAbstraction,
    TypedAbstractionSchema,
    TypedApplication,
    TypedApplicationSchema,
    TypedTerm,
    TypedTermSchema,
    UntypedAbstraction,
    UntypedAbstractionSchema,
    UntypedApplication,
    UntypedApplicationSchema,
    UntypedTerm,
    UntypedTermSchema,
    Variable,
    VariablePlaceholder,
)
from ..types import (
    BaseType,
    SimpleConnectiveType,
    SimpleConnectiveTypeSchema,
    SimpleType,
    SimpleTypeSchema,
    TypePlaceholder,
)
from ..typing import (
    ExplicitTypingRule,
    ExplicitTypingRulePremise,
    GradualTypingRule,
    GradualTypingRulePremise,
    ImplicitTypingRule,
    ImplicitTypingRulePremise,
    TypingStyle,
)
from .parser_context import LambdaParserContext
from .tokenizer import tokenize_lambda_string
from .tokens import LambdaToken, LambdaTokenKind


class LambdaParser(IdentifierParserMixin[LambdaTokenKind, LambdaToken], Parser[LambdaToken]):
    signature: LambdaSignature

    def __init__(self, signature: LambdaSignature, source: str, tokens: Sequence[LambdaToken]) -> None:
        super().__init__(source, tokens)
        self.signature = signature

    def _parse_base_type(self) -> BaseType:
        head = self.peek_unsafe()
        self.advance()
        return BaseType(head.value)

    def parse_type_placeholder(self) -> TypePlaceholder:
        identifier = self.parse_greek_identifier('GREEK_IDENTIFIER')
        return TypePlaceholder(identifier)

    @overload
    def _parse_arrow_type(self, context: LambdaParserContext, *, parse_schema: Literal[False]) -> SimpleConnectiveType: ...
    @overload
    def _parse_arrow_type(self, context: LambdaParserContext, *, parse_schema: Literal[True]) -> SimpleConnectiveTypeSchema: ...
    @overload
    def _parse_arrow_type(self, context: LambdaParserContext, *, parse_schema: bool) -> SimpleConnectiveType | SimpleConnectiveTypeSchema: ...
    def _parse_arrow_type(self, context: LambdaParserContext, *, parse_schema: bool) -> SimpleConnectiveType | SimpleConnectiveTypeSchema:
        head = self.advance_and_peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        a = self.parse_type(parse_schema=parse_schema)
        head = self.peek()

        if not head or head.kind == 'RIGHT_PARENTHESIS':
            raise context.annotate_context_error(f'Binary {'type schemas' if parse_schema else 'types'} must have a second subtype')

        if head.kind == 'BINARY_TYPE_CONNECTIVE':
            connective = BinaryTypeConnective(head.value)
            self.advance()
            b = self.parse_type(parse_schema=parse_schema)
            head = self.peek()

            if not head or head.kind != 'RIGHT_PARENTHESIS':
                raise context.annotate_context_error(f'Unclosed parentheses for binary {'type schema' if parse_schema else 'type'}')

            self.advance()

            if parse_schema:
                assert isinstance(a, SimpleTypeSchema)
                assert isinstance(b, SimpleTypeSchema)
                return SimpleConnectiveTypeSchema(connective, a, b)

            assert isinstance(a, SimpleType)
            assert isinstance(b, SimpleType)
            return SimpleConnectiveType(connective, a, b)

        raise context.annotate_context_error('Binary types must have a connective after the first subtype')

    @overload
    def parse_type(self, *, parse_schema: Literal[False]) -> SimpleType: ...
    @overload
    def parse_type(self, *, parse_schema: Literal[True]) -> SimpleTypeSchema: ...
    @overload
    def parse_type(self, *, parse_schema: bool) -> SimpleType | SimpleTypeSchema: ...
    def parse_type(self, *, parse_schema: bool) -> SimpleType | SimpleTypeSchema:
        head = self.peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        match head.kind:
            case 'SIGNATURE_SYMBOL':
                symbol = self.signature.get_symbol(head.value)

                if symbol.kind == 'CONSTANT_TERM':
                    raise self.annotate_token_error('Unexpected constant term symbol while parsing type')

                return self._parse_base_type()

            case 'GREEK_IDENTIFIER':
                if parse_schema:
                    return self.parse_type_placeholder()

                raise self.annotate_token_error('Type placeholders are only allowed in schemas')

            case 'LEFT_PARENTHESIS':
                context = LambdaParserContext(self)
                return self._parse_arrow_type(context, parse_schema=parse_schema)

            case _:
                raise self.annotate_token_error('Unexpected token')

    def _parse_constant(self) -> Constant:
        head = self.peek_unsafe()
        self.advance()
        return Constant(head.value)

    def parse_term_placeholder(self) -> TermPlaceholder:
        identifier = self.parse_latin_identifier('LATIN_IDENTIFIER')

        if identifier.value.islower():
            raise self.annotate_token_error('Expected a capital Latin identifier')

        return TermPlaceholder(identifier)

    @overload
    def parse_variable(self, *, parse_schema: Literal[True]) -> VariablePlaceholder: ...
    @overload
    def parse_variable(self, *, parse_schema: Literal[False]) -> Variable: ...
    @overload
    def parse_variable(self, *, parse_schema: bool) -> VariablePlaceholder | Variable: ...
    def parse_variable(self, *, parse_schema: bool) -> VariablePlaceholder | Variable:
        identifier = self.parse_latin_identifier('LATIN_IDENTIFIER')

        if parse_schema:
            return VariablePlaceholder(identifier)

        return Variable(identifier)

    @overload
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: Literal[True], typing: Literal[TypingStyle.IMPLICIT]) -> UntypedAbstractionSchema: ...
    @overload
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: Literal[True], typing: Literal[TypingStyle.EXPLICIT]) -> TypedAbstractionSchema: ...
    @overload
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: Literal[True], typing: TypingStyle) -> MixedAbstractionSchema: ...
    @overload
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: Literal[False], typing: Literal[TypingStyle.IMPLICIT]) -> UntypedAbstraction: ...
    @overload
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: Literal[False], typing: Literal[TypingStyle.EXPLICIT]) -> TypedAbstraction: ...
    @overload
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: Literal[False], typing: TypingStyle) -> MixedAbstraction: ...
    @overload
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: bool, typing: TypingStyle) -> MixedAbstraction | MixedAbstractionSchema: ...
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: bool, typing: TypingStyle) -> MixedAbstraction | MixedAbstractionSchema:  # noqa: C901
        head = self.advance_and_peek(2)

        if not head or head.kind != 'LATIN_IDENTIFIER' or head.value[0].isupper():
            raise context.annotate_context_error(f'Expected a variable name after {TermConnective.LAMBDA}')

        var = self.parse_variable(parse_schema=parse_schema)
        var_type: SimpleType | SimpleTypeSchema | None = None
        head = self.peek()

        if head and head.kind == 'COLON':
            if TypingStyle.EXPLICIT not in typing:
                raise context.annotate_context_error(f'Unexpected type annotation for the abstractor variable in an untyped {'abstraction schema' if parse_schema else 'abstraction'}')

            self.advance()
            var_type = self.parse_type(parse_schema=parse_schema)
        elif TypingStyle.IMPLICIT not in typing:
            raise context.annotate_context_error(f'Expected a type annotation for the abstractor variable in a typed {'abstraction schema' if parse_schema else 'abstraction'}')

        head = self.peek()

        if not head or head.kind != 'DOT':
            raise context.annotate_context_error(f'Expected a dot after an {'abstraction variable schema' if parse_schema else 'abstraction variable'}')

        self.advance()
        sub = self.parse_term(parse_schema=parse_schema, typing=typing)
        head = self.peek()

        if not head or head.kind != 'RIGHT_PARENTHESIS':
            raise context.annotate_context_error(f'Unclosed parentheses for {'abstraction schema' if parse_schema else 'abstraction'}')

        self.advance()

        if parse_schema:
            assert isinstance(var, VariablePlaceholder)

            match typing:
                case TypingStyle.GRADUAL:
                    assert isinstance(sub, MixedTermSchema)

                    if var_type:
                        assert isinstance(var_type, SimpleTypeSchema)
                        return MixedAbstractionSchema(var, sub, var_type)

                    return MixedAbstractionSchema(var, sub)

                case TypingStyle.IMPLICIT:
                    assert isinstance(sub, UntypedTermSchema)
                    assert var_type is None
                    return UntypedAbstractionSchema(var, sub)

                case TypingStyle.EXPLICIT:
                    assert isinstance(sub, TypedTermSchema)
                    assert isinstance(var_type, SimpleTypeSchema)
                    return TypedAbstractionSchema(var, sub, var_type)

        assert isinstance(var, Variable)

        if var_type:
            assert isinstance(var_type, SimpleType)

        match typing:
            case TypingStyle.GRADUAL:
                assert isinstance(sub, MixedTerm)

                if var_type:
                    assert isinstance(var_type, SimpleType)
                    return MixedAbstraction(var, sub, var_type)

                return MixedAbstraction(var, sub)

            case TypingStyle.IMPLICIT:
                assert isinstance(sub, UntypedTerm)
                assert var_type is None
                return UntypedAbstraction(var, sub)

            case TypingStyle.EXPLICIT:
                assert isinstance(sub, TypedTerm)
                assert isinstance(var_type, SimpleType)
                return TypedAbstraction(var, sub, var_type)

    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: Literal[True], typing: Literal[TypingStyle.IMPLICIT]) -> UntypedApplicationSchema: ...
    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: Literal[True], typing: Literal[TypingStyle.EXPLICIT]) -> TypedApplicationSchema: ...
    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: Literal[True], typing: TypingStyle) -> MixedApplicationSchema: ...
    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: Literal[False], typing: Literal[TypingStyle.IMPLICIT]) -> UntypedApplication: ...
    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: Literal[False], typing: Literal[TypingStyle.EXPLICIT]) -> TypedApplication: ...
    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: Literal[False], typing: TypingStyle) -> MixedApplication: ...
    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: bool, typing: TypingStyle) -> MixedApplication | MixedApplicationSchema: ...
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: bool, typing: TypingStyle) -> MixedApplication | MixedApplicationSchema:
        self.advance()

        a = self.parse_term(parse_schema=parse_schema, typing=typing)
        head = self.peek()

        if not head or head.kind == 'RIGHT_PARENTHESIS':
            raise context.annotate_context_error(f'{'MixedApplication schemas' if parse_schema else 'Applications'} must have a second subterm')

        b = self.parse_term(parse_schema=parse_schema, typing=typing)
        head = self.peek()

        if not head or head.kind != 'RIGHT_PARENTHESIS':
            raise context.annotate_context_error(f'Unclosed parentheses for {'application schema' if parse_schema else 'application'}')

        self.advance()

        if parse_schema:
            match typing:
                case TypingStyle.GRADUAL:
                    assert isinstance(a, MixedTermSchema)
                    assert isinstance(b, MixedTermSchema)
                    return MixedApplicationSchema(a, b)

                case TypingStyle.IMPLICIT:
                    assert isinstance(a, UntypedTermSchema)
                    assert isinstance(b, UntypedTermSchema)
                    return UntypedApplicationSchema(a, b)

                case TypingStyle.EXPLICIT:
                    assert isinstance(a, TypedTermSchema)
                    assert isinstance(b, TypedTermSchema)
                    return TypedApplicationSchema(a, b)

        match typing:
            case TypingStyle.GRADUAL:
                assert isinstance(a, MixedTerm)
                assert isinstance(b, MixedTerm)
                return MixedApplication(a, b)

            case TypingStyle.IMPLICIT:
                assert isinstance(a, UntypedTerm)
                assert isinstance(b, UntypedTerm)
                return UntypedApplication(a, b)

            case TypingStyle.EXPLICIT:
                assert isinstance(a, TypedTerm)
                assert isinstance(b, TypedTerm)
                return TypedApplication(a, b)

    @overload
    def parse_term(self, *, parse_schema: Literal[True], typing: Literal[TypingStyle.IMPLICIT]) -> UntypedTermSchema: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[True], typing: Literal[TypingStyle.EXPLICIT]) -> TypedTermSchema: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[True], typing: TypingStyle) -> MixedTermSchema: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[False], typing: Literal[TypingStyle.IMPLICIT]) -> UntypedTerm: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[False], typing: Literal[TypingStyle.EXPLICIT]) -> TypedTerm: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[False], typing: TypingStyle) -> MixedTerm: ...
    @overload
    def parse_term(self, *, parse_schema: bool, typing: TypingStyle) -> MixedTerm | MixedTermSchema: ...
    def parse_term(self, *, parse_schema: bool, typing: TypingStyle) -> MixedTerm | MixedTermSchema:
        head = self.peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        match head.kind:
            case 'SIGNATURE_SYMBOL':
                symbol = self.signature.get_symbol(head.value)

                if symbol.kind == 'BASE_TYPE':
                    raise self.annotate_token_error('Unexpected base type symbol while parsing term')

                return self._parse_constant()

            case 'LATIN_IDENTIFIER':
                if head.value[0].islower():
                    return self.parse_variable(parse_schema=parse_schema)

                if parse_schema:
                    return self.parse_term_placeholder()

                raise self.annotate_token_error('Term placeholders are only allowed in schemas')

            case 'LEFT_PARENTHESIS':
                try:
                    _, next_head = self.peek_multiple(2)
                except ValueError:
                    raise self.annotate_unexpected_end_of_input() from None

                context = LambdaParserContext(self)

                match next_head.kind:
                    case 'RIGHT_PARENTHESIS':
                        self.advance()
                        raise context.annotate_context_error(f'{'MixedApplication schemas' if parse_schema else 'Applications'} must have two terms, while {'Abstractions schemas' if parse_schema else 'abstractions'} must begin with {TermConnective.LAMBDA}')

                    case 'LAMBDA':
                        return self._parse_abstraction(context, parse_schema=parse_schema, typing=typing)

                    case _:
                        return self._parse_application(context, parse_schema=parse_schema, typing=typing)

            case _:
                raise self.annotate_token_error('Unexpected token')

    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[True], variable_assertion: Literal[False], typing: Literal[TypingStyle.IMPLICIT]) -> ImplicitTypeAssertionSchema: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[True], variable_assertion: Literal[False], typing: Literal[TypingStyle.EXPLICIT]) -> ExplicitTypeAssertionSchema: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[True], variable_assertion: Literal[False], typing: TypingStyle) -> GradualTypeAssertionSchema: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[False], variable_assertion: Literal[False], typing: Literal[TypingStyle.IMPLICIT]) -> ImplicitTypeAssertion: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[False], variable_assertion: Literal[False], typing: Literal[TypingStyle.EXPLICIT]) -> ExplicitTypeAssertion: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[False], variable_assertion: Literal[False], typing: TypingStyle) -> GradualTypeAssertion: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[False], variable_assertion: Literal[True]) -> VariableTypeAssertion: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[True], variable_assertion: Literal[True]) -> VariableTypeAssertionSchema: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: bool, variable_assertion: bool, typing: TypingStyle) -> GradualTypeAssertion | GradualTypeAssertionSchema: ...
    def parse_type_assertion(self, *, parse_schema: bool, variable_assertion: bool, typing: TypingStyle = TypingStyle.GRADUAL) -> GradualTypeAssertion | GradualTypeAssertionSchema:
        head = self.peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        context = LambdaParserContext(self)

        if variable_assertion:
            var = self.parse_variable(parse_schema=parse_schema)
        else:
            term = self.parse_term(parse_schema=parse_schema, typing=typing)

        if (head := self.peek()) and head.kind == 'COLON':
            self.advance()
        else:
            raise context.annotate_context_error('Expected a colon after the term in a type specification')

        type_ = self.parse_type(parse_schema=parse_schema)

        if parse_schema:
            assert isinstance(type_, SimpleTypeSchema)

            if variable_assertion:
                assert isinstance(var, VariablePlaceholder)
                return VariableTypeAssertionSchema(var, type_)

            match typing:
                case TypingStyle.GRADUAL:
                    assert isinstance(term, MixedTermSchema)
                    return GradualTypeAssertionSchema(term, type_)

                case TypingStyle.IMPLICIT:
                    assert isinstance(term, UntypedTermSchema)
                    return ImplicitTypeAssertionSchema(term, type_)

                case TypingStyle.EXPLICIT:
                    assert isinstance(term, TypedTermSchema)
                    return ExplicitTypeAssertionSchema(term, type_)

        assert isinstance(type_, SimpleType)

        if variable_assertion:
            assert isinstance(var, Variable)
            return VariableTypeAssertion(var, type_)

        match typing:
            case TypingStyle.GRADUAL:
                assert isinstance(term, MixedTerm)
                return GradualTypeAssertion(term, type_)

            case TypingStyle.IMPLICIT:
                assert isinstance(term, UntypedTerm)
                return ImplicitTypeAssertion(term, type_)

            case TypingStyle.EXPLICIT:
                assert isinstance(term, TypedTerm)
                return ExplicitTypeAssertion(term, type_)

    @overload
    def _parse_typing_rule_premise(self, premise_context: LambdaParserContext, typing: Literal[TypingStyle.IMPLICIT]) -> ImplicitTypingRulePremise: ...
    @overload
    def _parse_typing_rule_premise(self, premise_context: LambdaParserContext, typing: Literal[TypingStyle.EXPLICIT]) -> ExplicitTypingRulePremise: ...
    @overload
    def _parse_typing_rule_premise(self, premise_context: LambdaParserContext, typing: TypingStyle) -> GradualTypingRulePremise: ...
    def _parse_typing_rule_premise(self, premise_context: LambdaParserContext, typing: TypingStyle) -> GradualTypingRulePremise:
        discharge: GradualTypeAssertionSchema | None = None

        if (head := self.peek()) and head.kind == 'LEFT_BRACKET':
            head = self.advance_and_peek()

            if head and head.kind == 'RIGHT_BRACKET':
                raise premise_context.annotate_context_error('Empty discharge assumptions are disallowed')

            discharge = self.parse_type_assertion(parse_schema=True, variable_assertion=False, typing=typing)
            head = self.peek()

            if not head or head.kind == 'RIGHT_BRACKET':
                self.advance()
            else:
                premise_context.close_at_previous_token()
                raise premise_context.annotate_context_error('Unclosed bracket for discharge schema')

        main = self.parse_type_assertion(parse_schema=True, variable_assertion=False, typing=typing)

        match typing:
            case TypingStyle.GRADUAL:
                return GradualTypingRulePremise(main, discharge)

            case TypingStyle.IMPLICIT:
                assert isinstance(main, ImplicitTypeAssertionSchema)

                if discharge is None:
                    return ImplicitTypingRulePremise(main, discharge=None)

                assert isinstance(discharge, ImplicitTypeAssertionSchema)
                return ImplicitTypingRulePremise(main, discharge)

            case TypingStyle.EXPLICIT:
                assert isinstance(main, ExplicitTypeAssertionSchema)

                if discharge is None:
                    return ExplicitTypingRulePremise(main, discharge=None)

                assert isinstance(discharge, ExplicitTypeAssertionSchema)
                return ExplicitTypingRulePremise(main, discharge)


    @overload
    def _iter_typing_rule_premise(self, rule_context: LambdaParserContext, typing: Literal[TypingStyle.IMPLICIT]) -> Iterable[ImplicitTypingRulePremise]: ...
    @overload
    def _iter_typing_rule_premise(self, rule_context: LambdaParserContext, typing: Literal[TypingStyle.EXPLICIT]) -> Iterable[ExplicitTypingRulePremise]: ...
    @overload
    def _iter_typing_rule_premise(self, rule_context: LambdaParserContext, typing: TypingStyle) -> Iterable[GradualTypingRulePremise]: ...
    def _iter_typing_rule_premise(self, rule_context: LambdaParserContext, typing: TypingStyle) -> Iterable[GradualTypingRulePremise]:
        premise_context = LambdaParserContext(self)

        while (head := self.peek()) and head.kind != 'INFERENCE_RULE_SEQUENT':
            premise_context.reset()
            yield self._parse_typing_rule_premise(premise_context, typing=typing)
            head = self.peek()

            if not head or head.kind == 'INFERENCE_RULE_SEQUENT':
                break

            if head.kind == 'COMMA':
                self.advance()
            else:
                raise rule_context.annotate_context_error('Expected either a separator or a sequent symbol')

        if not self.peek():
            raise rule_context.annotate_context_error('Expected a sequent symbol')

    @overload
    def parse_typing_rule(self, typing: Literal[TypingStyle.IMPLICIT]) -> ImplicitTypingRule: ...
    @overload
    def parse_typing_rule(self, typing: Literal[TypingStyle.EXPLICIT]) -> ExplicitTypingRule: ...
    @overload
    def parse_typing_rule(self, typing: TypingStyle) -> GradualTypingRule: ...
    def parse_typing_rule(self, typing: TypingStyle) -> GradualTypingRule:
        if self.peek() is None:
            raise self.annotate_unexpected_end_of_input()

        rule_context = LambdaParserContext(self)

        match typing:
            case TypingStyle.GRADUAL:
                premises = list(self._iter_typing_rule_premise(rule_context, typing=TypingStyle.GRADUAL))
                self.advance()
                assertion = self.parse_type_assertion(parse_schema=True, variable_assertion=False, typing=TypingStyle.GRADUAL)
                return GradualTypingRule(premises, assertion)

            case TypingStyle.IMPLICIT:
                premises_imp = list(self._iter_typing_rule_premise(rule_context, typing=TypingStyle.IMPLICIT))
                self.advance()
                assertion = self.parse_type_assertion(parse_schema=True, variable_assertion=False, typing=TypingStyle.IMPLICIT)
                return ImplicitTypingRule(premises_imp, assertion)

            case TypingStyle.EXPLICIT:
                premises_exp = list(self._iter_typing_rule_premise(rule_context, typing=TypingStyle.EXPLICIT))
                self.advance()
                assertion = self.parse_type_assertion(parse_schema=True, variable_assertion=False, typing=TypingStyle.EXPLICIT)
                return ExplicitTypingRule(premises_exp, assertion)


def parse_variable(source: str) -> Variable:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, source)

    with LambdaParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_variable(parse_schema=False)


@overload
def parse_term(signature: LambdaSignature, source: str, typing: Literal[TypingStyle.IMPLICIT]) -> UntypedTerm: ...
@overload
def parse_term(signature: LambdaSignature, source: str, typing: Literal[TypingStyle.EXPLICIT]) -> TypedTerm: ...
@overload
def parse_term(signature: LambdaSignature, source: str, typing: TypingStyle) -> MixedTerm: ...
def parse_term(signature: LambdaSignature, source: str, typing: TypingStyle) -> MixedTerm:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_term(parse_schema=False, typing=typing)


def parse_pure_term(source: str) -> UntypedTerm:
    return parse_term(EMPTY_SIGNATURE, source, TypingStyle.IMPLICIT)


def parse_variable_placeholder(source: str) -> VariablePlaceholder:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, source)

    with LambdaParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_variable(parse_schema=True)


def parse_term_placeholder(source: str) -> TermPlaceholder:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, source)

    with LambdaParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_term_placeholder()


@overload
def parse_term_schema(signature: LambdaSignature, source: str, typing: Literal[TypingStyle.IMPLICIT]) -> UntypedTermSchema: ...
@overload
def parse_term_schema(signature: LambdaSignature, source: str, typing: Literal[TypingStyle.EXPLICIT]) -> TypedTermSchema: ...
@overload
def parse_term_schema(signature: LambdaSignature, source: str, typing: TypingStyle) -> MixedTermSchema: ...
def parse_term_schema(signature: LambdaSignature, source: str, typing: TypingStyle) -> MixedTermSchema:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_term(parse_schema=True, typing=typing)


@overload
def parse_pure_term_schema(source: str, typing: Literal[TypingStyle.IMPLICIT]) -> UntypedTermSchema: ...
@overload
def parse_pure_term_schema(source: str, typing: Literal[TypingStyle.EXPLICIT]) -> TypedTermSchema: ...
@overload
def parse_pure_term_schema(source: str, typing: TypingStyle) -> MixedTermSchema: ...
def parse_pure_term_schema(source: str, typing: TypingStyle) -> MixedTermSchema:
    return parse_term_schema(EMPTY_SIGNATURE, source, typing=typing)


def parse_type(signature: LambdaSignature, source: str) -> SimpleType:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_type(parse_schema=False)


def parse_type_placeholder(source: str) -> TypePlaceholder:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, source)

    with LambdaParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_type_placeholder()


def parse_type_schema(signature: LambdaSignature, source: str) -> SimpleTypeSchema:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_type(parse_schema=True)


@overload
def parse_type_assertion(signature: LambdaSignature, source: str, typing: Literal[TypingStyle.IMPLICIT]) -> ImplicitTypeAssertion: ...
@overload
def parse_type_assertion(signature: LambdaSignature, source: str, typing: Literal[TypingStyle.EXPLICIT]) -> ExplicitTypeAssertion: ...
@overload
def parse_type_assertion(signature: LambdaSignature, source: str, typing: TypingStyle) -> GradualTypeAssertion: ...
def parse_type_assertion(signature: LambdaSignature, source: str, typing: TypingStyle) -> GradualTypeAssertion:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_type_assertion(parse_schema=False, variable_assertion=False, typing=typing)


def parse_variable_assertion(signature: LambdaSignature, source: str) -> VariableTypeAssertion:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_type_assertion(parse_schema=False, variable_assertion=True)


@overload
def parse_typing_rule(signature: LambdaSignature, source: str, typing: Literal[TypingStyle.IMPLICIT]) -> ImplicitTypingRule: ...
@overload
def parse_typing_rule(signature: LambdaSignature, source: str, typing: Literal[TypingStyle.EXPLICIT]) -> ExplicitTypingRule: ...
@overload
def parse_typing_rule(signature: LambdaSignature, source: str, typing: TypingStyle) -> GradualTypingRule: ...
def parse_typing_rule(signature: LambdaSignature, source: str, typing: TypingStyle) -> GradualTypingRule:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_typing_rule(typing=typing)
