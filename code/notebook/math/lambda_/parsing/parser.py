from collections.abc import Iterable, Sequence
from typing import Literal, overload

from ....parsing import IdentifierParserMixin, Parser, ParserError
from ..alphabet import BinaryTypeConnective, TermConnective
from ..assertions import (
    TypeAssertion,
    TypeAssertionSchema,
    VariableTypeAssertion,
    VariableTypeAssertionSchema,
)
from ..signature import EMPTY_SIGNATURE, LambdaSignature
from ..terms import (
    Constant,
    TermPlaceholder,
    TypedAbstraction,
    TypedAbstractionSchema,
    TypedApplication,
    TypedApplicationSchema,
    TypedTerm,
    TypedTermSchema,
    UntypedAbstraction,
    UntypedApplication,
    UntypedTerm,
    Variable,
    VariablePlaceholder,
)
from ..type_system import TypingRule, TypingRulePremise
from ..types import (
    BaseType,
    SimpleConnectiveType,
    SimpleConnectiveTypeSchema,
    SimpleType,
    SimpleTypeSchema,
    TypePlaceholder,
    TypeVariable,
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

    def parse_type_variable(self) -> TypeVariable:
        identifier = self.parse_greek_identifier('GREEK_IDENTIFIER')
        return TypeVariable(identifier)

    def parse_type_placeholder(self) -> TypePlaceholder:
        identifier = self.parse_greek_identifier('GREEK_IDENTIFIER')
        return TypePlaceholder(identifier)

    @overload
    def _parse_connective_type(self, context: LambdaParserContext, *, parse_schema: Literal[False]) -> SimpleConnectiveType: ...
    @overload
    def _parse_connective_type(self, context: LambdaParserContext, *, parse_schema: Literal[True]) -> SimpleConnectiveTypeSchema: ...
    @overload
    def _parse_connective_type(self, context: LambdaParserContext, *, parse_schema: bool) -> SimpleConnectiveType | SimpleConnectiveTypeSchema: ...
    def _parse_connective_type(self, context: LambdaParserContext, *, parse_schema: bool) -> SimpleConnectiveType | SimpleConnectiveTypeSchema:
        head = self.advance_and_peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        left = self.parse_type(parse_schema=parse_schema)
        head = self.peek()

        if not head or head.kind == 'RIGHT_PARENTHESIS':
            raise context.annotate_context_error(f'Binary {'type schemas' if parse_schema else 'types'} must have a second subtype')

        if head.kind == 'BINARY_TYPE_CONNECTIVE':
            connective = BinaryTypeConnective(head.value)
            self.advance()
            right = self.parse_type(parse_schema=parse_schema)
            head = self.peek()

            if not head or head.kind != 'RIGHT_PARENTHESIS':
                raise context.annotate_context_error(f'Unclosed parentheses for binary {'type schema' if parse_schema else 'type'}')

            self.advance()

            if parse_schema:
                assert isinstance(left, SimpleTypeSchema)
                assert isinstance(right, SimpleTypeSchema)
                return SimpleConnectiveTypeSchema(connective, left, right)

            assert isinstance(left, SimpleType)
            assert isinstance(right, SimpleType)
            return SimpleConnectiveType(connective, left, right)

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

                return self.parse_type_variable()

            case 'LEFT_PARENTHESIS':
                context = LambdaParserContext(self)
                return self._parse_connective_type(context, parse_schema=parse_schema)

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
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: Literal[True], typed: Literal[True]) -> TypedAbstractionSchema: ...
    @overload
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: Literal[False], typed: Literal[False]) -> UntypedAbstraction: ...
    @overload
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: Literal[False], typed: Literal[True]) -> TypedAbstraction: ...
    @overload
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: Literal[False], typed: bool) -> UntypedAbstraction | TypedAbstraction: ...
    @overload
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: bool, typed: bool) -> TypedAbstraction | UntypedAbstraction | TypedAbstractionSchema: ...
    def _parse_abstraction(self, context: LambdaParserContext, *, parse_schema: bool, typed: bool) -> TypedAbstraction | UntypedAbstraction | TypedAbstractionSchema:
        if parse_schema and not typed:
            raise ParserError('Untyped schemas are not supported')

        head = self.advance_and_peek(2)

        if not head or head.kind != 'LATIN_IDENTIFIER' or head.value[0].isupper():
            raise context.annotate_context_error(f'Expected a variable name after {TermConnective.LAMBDA}')

        var = self.parse_variable(parse_schema=parse_schema)
        var_type: SimpleType | SimpleTypeSchema | None = None
        head = self.peek()

        if head and head.kind == 'COLON':
            if not typed:
                raise context.annotate_context_error(f'Unexpected type annotation for the abstractor variable in an untyped {'abstraction schema' if parse_schema else 'abstraction'}')

            self.advance()
            var_type = self.parse_type(parse_schema=parse_schema)
        elif typed:
            raise context.annotate_context_error(f'Expected a type annotation for the abstractor variable in a typed {'abstraction schema' if parse_schema else 'abstraction'}')

        head = self.peek()

        if not head or head.kind != 'DOT':
            raise context.annotate_context_error(f'Expected a dot after an {'abstraction variable schema' if parse_schema else 'abstraction variable'}')

        self.advance()
        sub = self.parse_term(parse_schema=parse_schema, typed=typed)
        head = self.peek()

        if not head or head.kind != 'RIGHT_PARENTHESIS':
            raise context.annotate_context_error(f'Unclosed parentheses for {'abstraction schema' if parse_schema else 'abstraction'}')

        self.advance()

        if parse_schema:
            assert isinstance(var, VariablePlaceholder)
            assert isinstance(sub, TypedTermSchema)
            assert isinstance(var_type, SimpleTypeSchema)
            return TypedAbstractionSchema(var, var_type, sub)

        assert isinstance(var, Variable)

        if var_type:
            assert isinstance(var_type, SimpleType)

        if typed:
            assert isinstance(sub, TypedTerm)
            assert isinstance(var_type, SimpleType)
            return TypedAbstraction(var, var_type, sub)

        assert isinstance(sub, UntypedTerm)
        assert var_type is None
        return UntypedAbstraction(var, sub)

    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: Literal[True], typed: Literal[True]) -> TypedApplicationSchema: ...
    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: Literal[False], typed: Literal[False]) -> UntypedApplication: ...
    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: Literal[False], typed: Literal[True]) -> TypedApplication: ...
    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: Literal[False], typed: bool) -> UntypedApplication | TypedApplication: ...
    @overload
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: bool, typed: bool) -> UntypedApplication | TypedApplication | TypedApplicationSchema: ...
    def _parse_application(self, context: LambdaParserContext, *, parse_schema: bool, typed: bool) -> UntypedApplication | TypedApplication | TypedApplicationSchema:
        if parse_schema and not typed:
            raise ParserError('Untyped schemas are not supported')

        self.advance()

        left = self.parse_term(parse_schema=parse_schema, typed=typed)
        head = self.peek()

        if not head or head.kind == 'RIGHT_PARENTHESIS':
            raise context.annotate_context_error(f'{'UntypedApplication schemas' if parse_schema else 'Applications'} must have a second subterm')

        right = self.parse_term(parse_schema=parse_schema, typed=typed)
        head = self.peek()

        if not head or head.kind != 'RIGHT_PARENTHESIS':
            raise context.annotate_context_error(f'Unclosed parentheses for {'application schema' if parse_schema else 'application'}')

        self.advance()

        if parse_schema:
            assert isinstance(left, TypedTermSchema)
            assert isinstance(right, TypedTermSchema)
            return TypedApplicationSchema(left, right)

        if typed:
            assert isinstance(left, TypedTerm)
            assert isinstance(right, TypedTerm)
            return TypedApplication(left, right)

        assert isinstance(left, UntypedTerm)
        assert isinstance(right, UntypedTerm)
        return UntypedApplication(left, right)

    @overload
    def parse_term(self, *, parse_schema: Literal[True], typed: Literal[True]) -> TypedTermSchema: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[False], typed: Literal[False]) -> UntypedTerm: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[False], typed: Literal[True]) -> TypedTerm: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[False], typed: bool) -> UntypedTerm | TypedTerm: ...
    @overload
    def parse_term(self, *, parse_schema: bool, typed: bool) -> UntypedTerm | TypedTerm | TypedTermSchema: ...
    def parse_term(self, *, parse_schema: bool, typed: bool) -> UntypedTerm | TypedTerm | TypedTermSchema:
        if parse_schema and not typed:
            raise ParserError('Untyped schemas are not supported')

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
                        raise context.annotate_context_error(f'{'UntypedApplication schemas' if parse_schema else 'Applications'} must have two terms, while {'Abstractions schemas' if parse_schema else 'abstractions'} must begin with {TermConnective.LAMBDA}')

                    case 'LAMBDA':
                        return self._parse_abstraction(context, parse_schema=parse_schema, typed=typed)

                    case _:
                        return self._parse_application(context, parse_schema=parse_schema, typed=typed)

            case _:
                raise self.annotate_token_error('Unexpected token')

    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[True], variable_assertion: Literal[True]) -> VariableTypeAssertionSchema: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[True], variable_assertion: Literal[False]) -> TypeAssertionSchema: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[False], variable_assertion: Literal[True]) -> VariableTypeAssertion: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[False], variable_assertion: Literal[False]) -> TypeAssertion: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: bool, variable_assertion: bool) -> TypeAssertion | TypeAssertionSchema: ...
    def parse_type_assertion(self, *, parse_schema: bool, variable_assertion: bool) -> TypeAssertion | TypeAssertionSchema:
        head = self.peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        context = LambdaParserContext(self)

        if variable_assertion:
            var = self.parse_variable(parse_schema=parse_schema)
        else:
            term = self.parse_term(parse_schema=parse_schema, typed=True)

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

            assert isinstance(term, TypedTermSchema)
            return TypeAssertionSchema(term, type_)

        assert isinstance(type_, SimpleType)

        if variable_assertion:
            assert isinstance(var, Variable)
            return VariableTypeAssertion(var, type_)

        assert isinstance(term, TypedTerm)
        return TypeAssertion(term, type_)

    def _parse_typing_rule_premise(self, premise_context: LambdaParserContext) -> TypingRulePremise:
        discharge: VariableTypeAssertionSchema | None = None

        if (head := self.peek()) and head.kind == 'LEFT_BRACKET':
            head = self.advance_and_peek()

            if head and head.kind == 'RIGHT_BRACKET':
                raise premise_context.annotate_context_error('Empty discharge assumptions are disallowed')

            discharge = self.parse_type_assertion(parse_schema=True, variable_assertion=True)
            head = self.peek()

            if not head or head.kind == 'RIGHT_BRACKET':
                self.advance()
            else:
                premise_context.close_at_previous_token()
                raise premise_context.annotate_context_error('Unclosed bracket for discharge schema')

        main = self.parse_type_assertion(parse_schema=True, variable_assertion=False)
        return TypingRulePremise(main, discharge)

    def _iter_typing_rule_premise(self, rule_context: LambdaParserContext) -> Iterable[TypingRulePremise]:
        premise_context = LambdaParserContext(self)

        while (head := self.peek()) and head.kind != 'INFERENCE_RULE_SEQUENT':
            premise_context.reset()
            yield self._parse_typing_rule_premise(premise_context)
            head = self.peek()

            if not head or head.kind == 'INFERENCE_RULE_SEQUENT':
                break

            if head.kind == 'COMMA':
                self.advance()
            else:
                raise rule_context.annotate_context_error('Expected either a separator or a sequent symbol')

        if not self.peek():
            raise rule_context.annotate_context_error('Expected a sequent symbol')

    def parse_typing_rule(self, name: str) -> TypingRule:
        if self.peek() is None:
            raise self.annotate_unexpected_end_of_input()

        rule_context = LambdaParserContext(self)
        premises_exp = list(self._iter_typing_rule_premise(rule_context))
        self.advance()
        assertion = self.parse_type_assertion(parse_schema=True, variable_assertion=False)
        return TypingRule(name, premises_exp, assertion)


def parse_variable(source: str) -> Variable:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, source)

    with LambdaParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_variable(parse_schema=False)


def parse_untyped_term(source: str, signature: LambdaSignature = EMPTY_SIGNATURE) -> UntypedTerm:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_term(parse_schema=False, typed=False)


def parse_typed_term(source: str, signature: LambdaSignature = EMPTY_SIGNATURE) -> TypedTerm:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_term(parse_schema=False, typed=True)


def parse_variable_placeholder(source: str) -> VariablePlaceholder:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, source)

    with LambdaParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_variable(parse_schema=True)


def parse_term_placeholder(source: str) -> TermPlaceholder:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, source)

    with LambdaParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_term_placeholder()


def parse_typed_term_schema(source: str, signature: LambdaSignature = EMPTY_SIGNATURE) -> TypedTermSchema:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_term(parse_schema=True, typed=True)


def parse_type(source: str, signature: LambdaSignature = EMPTY_SIGNATURE) -> SimpleType:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_type(parse_schema=False)


def parse_type_variable(source: str) -> TypeVariable:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, source)

    with LambdaParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_type_variable()


def parse_type_placeholder(source: str) -> TypePlaceholder:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, source)

    with LambdaParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_type_placeholder()


def parse_type_schema(source: str, signature: LambdaSignature = EMPTY_SIGNATURE) -> SimpleTypeSchema:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_type(parse_schema=True)


def parse_type_assertion(source: str, signature: LambdaSignature = EMPTY_SIGNATURE) -> TypeAssertion:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_type_assertion(parse_schema=False, variable_assertion=False)


def parse_variable_assertion(source: str, signature: LambdaSignature = EMPTY_SIGNATURE) -> VariableTypeAssertion:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_type_assertion(parse_schema=False, variable_assertion=True)


def parse_typing_rule(name: str, source: str, signature: LambdaSignature = EMPTY_SIGNATURE) -> TypingRule:
    tokens = tokenize_lambda_string(signature, source)

    with LambdaParser(signature, source, tokens) as parser:
        return parser.parse_typing_rule(name)
