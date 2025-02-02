from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal, overload

from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.mixins.inference_rules import InferenceRuleParserMixin
from ....parsing.mixins.whitespace import WhitespaceParserMixin
from ....parsing.parser import Parser
from ....support.inference.rules import InferenceRuleConnective
from ....support.unicode import Capitalization, is_latin_string
from ..alphabet import BinaryTypeConnective, TermConnective, TypeAssertionConnective
from ..assertions import TypeAssertion, TypeAssertionSchema, VariableTypeAssertion, VariableTypeAssertionSchema
from ..signature import EMPTY_SIGNATURE, LambdaSignature
from ..terms import (
    Abstraction,
    AbstractionSchema,
    AnnotatedConstant,
    Application,
    ApplicationSchema,
    Constant,
    PlainConstant,
    Term,
    TermPlaceholder,
    TermSchema,
    TypedAbstraction,
    TypedApplication,
    TypedTerm,
    UntypedAbstraction,
    UntypedApplication,
    UntypedTerm,
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
from ..typing_rules import TypingRule, TypingRulePremise
from .tokenizer import tokenize_lambda_string
from .tokens import BaseTypeToken, ConstantTermToken, LambdaToken, MiscToken


@dataclass
class LambdaParser(InferenceRuleParserMixin[LambdaToken], WhitespaceParserMixin[LambdaToken], Parser[LambdaToken]):
    signature: LambdaSignature

    def parse_base_type(self) -> BaseType:
        head = self.peek()
        assert isinstance(head, BaseTypeToken)
        self.advance()
        return BaseType(str(head))

    def parse_type_placeholder(self) -> TypePlaceholder:
        head = self.peek()
        assert isinstance(head, GreekIdentifier)
        self.advance()
        return TypePlaceholder(head)

    @overload
    def parse_arrow_type(self, *, parse_schema: Literal[False]) -> SimpleConnectiveType: ...
    @overload
    def parse_arrow_type(self, *, parse_schema: Literal[True]) -> SimpleConnectiveTypeSchema: ...
    @overload
    def parse_arrow_type(self, *, parse_schema: bool) -> SimpleConnectiveType | SimpleConnectiveTypeSchema: ...
    def parse_arrow_type(self, *, parse_schema: bool) -> SimpleConnectiveType | SimpleConnectiveTypeSchema:
        assert self.peek() == MiscToken.left_parenthesis
        start_i = self.index
        self.advance()

        a = self.parse_type(parse_schema=parse_schema)
        self.skip_spaces()

        if self.is_at_end() or self.peek() == MiscToken.right_parenthesis:
            raise self.error(f'{'Binary type schemas' if parse_schema else 'Binary types'} must have a second subtype', i_first_token=start_i)

        if isinstance(connective := self.peek(), BinaryTypeConnective):
            self.advance_and_skip_spaces()

            b = self.parse_type(parse_schema=parse_schema)

            if self.is_at_end() or self.peek() != MiscToken.right_parenthesis:
                raise self.error(f'Unclosed parentheses for {'binary type schema' if parse_schema else 'binary type'}', i_first_token=start_i)

            self.advance()

            if parse_schema:
                assert isinstance(a, SimpleTypeSchema)
                assert isinstance(b, SimpleTypeSchema)
                return SimpleConnectiveTypeSchema(connective, a, b)

            assert isinstance(a, SimpleType)
            assert isinstance(b, SimpleType)
            return SimpleConnectiveType(connective, a, b)

        raise self.error('Binary types must have a connective after the first subtype', i_first_token=start_i)

    @overload
    def parse_type(self, *, parse_schema: Literal[False]) -> SimpleType: ...
    @overload
    def parse_type(self, *, parse_schema: Literal[True]) -> SimpleTypeSchema: ...
    @overload
    def parse_type(self, *, parse_schema: bool) -> SimpleType | SimpleTypeSchema: ...
    def parse_type(self, *, parse_schema: bool) -> SimpleType | SimpleTypeSchema:
        if isinstance(self.peek(), BaseTypeToken):
            return self.parse_base_type()

        if isinstance(self.peek(), GreekIdentifier):
            if parse_schema:
                return self.parse_type_placeholder()

            raise self.error('Type placeholders are only allowed in schemas')

        if self.peek() == MiscToken.left_parenthesis:
            return self.parse_arrow_type(parse_schema=parse_schema)

        raise self.error('Unexpected token')

    @overload
    def parse_constant(self, *, only_untyped: Literal[False] = False, only_typed: Literal[False] = False) -> AnnotatedConstant | PlainConstant: ...
    @overload
    def parse_constant(self, *, only_untyped: Literal[True], only_typed: Literal[False] = False) -> PlainConstant: ...
    @overload
    def parse_constant(self, *, only_untyped: Literal[False] = False, only_typed: Literal[True]) -> AnnotatedConstant: ...
    @overload
    def parse_constant(self, *, only_untyped: bool, only_typed: bool) -> Constant: ...
    def parse_constant(self, *, only_untyped: bool = False, only_typed: bool = False) -> Constant:
        head = self.peek()
        assert isinstance(head, ConstantTermToken)
        self.advance()

        if not self.is_at_end() and self.peek() == TypeAssertionConnective.colon:
            if only_untyped:
                raise self.error('Unexpected type annotation for an untyped constant')

            self.advance_and_skip_spaces()
            type_ = self.parse_type(parse_schema=False)
            return AnnotatedConstant(str(head), type_)

        if only_typed:
            raise self.error('Expected a type annotation for a typed constant')

        return PlainConstant(str(head))

    def parse_term_placeholder(self) -> TermPlaceholder:
        head = self.peek()
        assert isinstance(head, LatinIdentifier)
        assert is_latin_string(head.value, Capitalization.upper)
        self.advance()
        return TermPlaceholder(head)

    @overload
    def parse_variable(self, *, parse_schema: Literal[True]) -> VariablePlaceholder: ...
    @overload
    def parse_variable(self, *, parse_schema: Literal[False]) -> Variable: ...
    @overload
    def parse_variable(self, *, parse_schema: bool) -> VariablePlaceholder | Variable: ...
    def parse_variable(self, *, parse_schema: bool) -> VariablePlaceholder | Variable:
        head = self.peek()
        assert isinstance(head, LatinIdentifier)
        assert is_latin_string(head.value, Capitalization.lower)
        self.advance()

        if parse_schema:
            return VariablePlaceholder(head)

        return Variable(head)

    @overload
    def parse_abstraction(self, *, parse_schema: Literal[True]) -> AbstractionSchema: ...
    @overload
    def parse_abstraction(self, *, parse_schema: Literal[False], only_untyped: Literal[False] = False, only_typed: Literal[False] = False) -> Abstraction: ...
    @overload
    def parse_abstraction(self, *, parse_schema: Literal[False], only_untyped: Literal[True], only_typed: Literal[False] = False) -> UntypedAbstraction: ...
    @overload
    def parse_abstraction(self, *, parse_schema: Literal[False], only_untyped: Literal[False] = False, only_typed: Literal[True]) -> TypedAbstraction: ...
    @overload
    def parse_abstraction(self, *, parse_schema: bool, only_untyped: bool, only_typed: bool) -> Abstraction | AbstractionSchema: ...
    def parse_abstraction(self, *, parse_schema: bool, only_untyped: bool = False, only_typed: bool = False) -> Abstraction | AbstractionSchema:
        assert self.peek_multiple(2) == [MiscToken.left_parenthesis, TermConnective.l]
        start_i = self.index
        self.advance(2)

        if self.is_at_end() or not isinstance(self.peek(), LatinIdentifier):
            raise self.error(f'Expected a variable name after {TermConnective.l}', i_first_token=start_i)

        var = self.parse_variable(parse_schema=parse_schema)
        var_type: SimpleType | SimpleTypeSchema | None = None

        if not self.is_at_end() and self.peek() == TypeAssertionConnective.colon:
            if only_untyped:
                raise self.error('Unexpected type annotation for the abstractor variable in an untyped abstraction')

            self.advance_and_skip_spaces()
            var_type = self.parse_type(parse_schema=parse_schema)
        elif only_typed:
            raise self.error('Expected a type annotation for the abstractor variable in a typed abstraction')

        if self.is_at_end() or self.peek() != MiscToken.dot:
            raise self.error('Expected a dot after an abstraction variable', i_first_token=start_i)

        self.advance()

        sub = self.parse_term(parse_schema=parse_schema, only_typed=only_typed, only_untyped=only_untyped)

        if self.is_at_end() or self.peek() != MiscToken.right_parenthesis:
            raise self.error('Unclosed parentheses for abstraction', i_first_token=start_i)

        self.advance()

        if parse_schema:
            assert isinstance(sub, TermSchema)
            assert isinstance(var, VariablePlaceholder)

            if var_type:
                assert isinstance(var_type, SimpleTypeSchema)

            return AbstractionSchema(sub, var, var_type)

        assert isinstance(var, Variable)

        if var_type:
            assert isinstance(var_type, SimpleType)

        if only_typed:
            assert isinstance(sub, TypedTerm)
            assert var_type is not None
            return TypedAbstraction(var, sub, var_type)

        if only_untyped:
            assert isinstance(sub, UntypedTerm)
            assert var_type is None
            return UntypedAbstraction(var, sub, var_type)

        assert isinstance(sub, Term)
        return Abstraction(var, sub, var_type)

    @overload
    def parse_application(self, *, parse_schema: Literal[True]) -> ApplicationSchema: ...
    @overload
    def parse_application(self, *, parse_schema: Literal[False], only_untyped: Literal[False] = False, only_typed: Literal[False] = False) -> Application: ...
    @overload
    def parse_application(self, *, parse_schema: Literal[False], only_untyped: Literal[True], only_typed: Literal[False] = False) -> UntypedApplication: ...
    @overload
    def parse_application(self, *, parse_schema: Literal[False], only_untyped: Literal[False] = False, only_typed: Literal[True]) -> TypedApplication: ...
    @overload
    def parse_application(self, *, parse_schema: bool, only_untyped: bool, only_typed: bool) -> Application | ApplicationSchema: ...
    def parse_application(self, *, parse_schema: bool, only_untyped: bool = False, only_typed: bool = False) -> Application | ApplicationSchema:
        assert self.peek() == MiscToken.left_parenthesis
        start_i = self.index
        self.advance()

        a = self.parse_term(parse_schema=parse_schema, only_typed=only_typed, only_untyped=only_untyped)

        if self.is_at_end() or self.peek() == MiscToken.right_parenthesis:
            raise self.error(f'{'Application schemas' if parse_schema else 'Applications'} must have a second subterm', i_first_token=start_i)

        b = self.parse_term(parse_schema=parse_schema, only_typed=only_typed, only_untyped=only_untyped)

        if self.is_at_end() or self.peek() != MiscToken.right_parenthesis:
            raise self.error(f'Unclosed parentheses for {'application schema' if parse_schema else 'application'}', i_first_token=start_i)

        self.advance()

        if parse_schema:
            assert isinstance(a, TermSchema)
            assert isinstance(b, TermSchema)
            return ApplicationSchema(a, b)

        if only_untyped:
            assert isinstance(a, UntypedTerm)
            assert isinstance(b, UntypedTerm)
            return UntypedApplication(a, b)

        if only_typed:
            assert isinstance(a, TypedTerm)
            assert isinstance(b, TypedTerm)
            return TypedApplication(a, b)

        assert isinstance(a, Term)
        assert isinstance(b, Term)
        return Application(a, b)

    @overload
    def parse_term(self, *, parse_schema: Literal[True]) -> TermSchema: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[False], only_untyped: Literal[False] = False, only_typed: Literal[False] = False) -> Term: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[False], only_untyped: Literal[True], only_typed: Literal[False] = False) -> UntypedTerm: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[False], only_untyped: Literal[False] = False, only_typed: Literal[True]) -> TypedTerm: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[False], only_untyped: bool, only_typed: bool) -> Term: ...
    @overload
    def parse_term(self, *, parse_schema: bool, only_untyped: bool, only_typed: bool) -> Term | TermSchema: ...
    def parse_term(self, *, parse_schema: bool, only_untyped: bool = False, only_typed: bool = False) -> Term | TermSchema:
        if isinstance(self.peek(), ConstantTermToken):
            return self.parse_constant(only_typed=only_typed, only_untyped=only_untyped)

        if isinstance(head := self.peek(), LatinIdentifier):
            if is_latin_string(head.value, Capitalization.lower):
                return self.parse_variable(parse_schema=parse_schema)

            if parse_schema:
                return self.parse_term_placeholder()

            raise self.error('Term placeholders are only allowed in schemas')

        if self.peek_multiple(2) == [MiscToken.left_parenthesis, MiscToken.right_parenthesis]:
            raise self.error(f'{'Application schemas' if parse_schema else 'Applications'} must have two terms, while abstractions must begin with λ', i_last_token=self.index + 1)

        if self.peek_multiple(2) == [MiscToken.left_parenthesis, TermConnective.l]:
            return self.parse_abstraction(parse_schema=parse_schema, only_typed=only_typed, only_untyped=only_untyped)

        if self.peek() == MiscToken.left_parenthesis:
            return self.parse_application(parse_schema=parse_schema, only_typed=only_typed, only_untyped=only_untyped)

        raise self.error('Unexpected token')

    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[False], variable_assertion: Literal[True]) -> VariableTypeAssertion: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[True], variable_assertion: Literal[True]) -> VariableTypeAssertionSchema: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[False], variable_assertion: Literal[False]) -> TypeAssertion: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: Literal[True], variable_assertion: Literal[False]) -> TypeAssertionSchema: ...
    @overload
    def parse_type_assertion(self, *, parse_schema: bool, variable_assertion: bool) -> TypeAssertion | TypeAssertionSchema: ...
    def parse_type_assertion(self, *, parse_schema: bool, variable_assertion: bool) -> TypeAssertion | TypeAssertionSchema:
        start_i = self.index

        if variable_assertion:
            var = self.parse_variable(parse_schema=parse_schema)
        else:
            term = self.parse_term(parse_schema=parse_schema, only_typed=False, only_untyped=False)

        if self.peek() == TypeAssertionConnective.colon:
            self.advance_and_skip_spaces()
        else:
            raise self.error('Expected a colon after the term in a type specification', i_first_token=start_i)

        type_ = self.parse_type(parse_schema=parse_schema)

        if parse_schema:
            assert isinstance(type_, SimpleTypeSchema)

            if variable_assertion:
                assert isinstance(var, VariablePlaceholder)
                return VariableTypeAssertionSchema(var, type_)

            assert isinstance(term, TermSchema)
            return TypeAssertionSchema(term, type_)

        assert isinstance(type_, SimpleType)

        if variable_assertion:
            assert isinstance(var, Variable)
            return VariableTypeAssertion(var, type_)

        assert isinstance(term, Term)
        return TypeAssertion(term, type_)

    def parse_variable_assertion(self) -> VariableTypeAssertion:
        start_i = self.index
        var = self.parse_variable(parse_schema=False)

        if self.peek() == TypeAssertionConnective.colon:
            self.advance_and_skip_spaces()
        else:
            raise self.error('Expected a colon after the variable in a variable type specification', i_first_token=start_i)

        type_ = self.parse_type(parse_schema=False)

        return VariableTypeAssertion(var, type_)

    def parse_typing_rule_premise(self) -> TypingRulePremise:
        discharge: TypeAssertionSchema | None = None
        start = self.index

        if self.peek() == MiscToken.left_bracket:
            self.advance()

            discharge = self.parse_type_assertion(parse_schema=True, variable_assertion=False)

            if self.peek() == MiscToken.right_bracket:
                self.advance_and_skip_spaces()
            else:
                raise self.error('Unclosed bracket for discharge schema', i_first_token=start)

        main = self.parse_type_assertion(parse_schema=True, variable_assertion=False)
        self.skip_spaces()
        return TypingRulePremise(main, discharge)

    def iter_typing_rule_premise(self) -> Iterable[TypingRulePremise]:
        for _ in self.iter_parse_premise_positions(InferenceRuleConnective.sequent, MiscToken.comma):
            self.skip_spaces()
            yield self.parse_typing_rule_premise()

    def parse_typing_rule(self) -> TypingRule:
        name = self.parse_rule_name(MiscToken.left_parenthesis, MiscToken.right_parenthesis)
        self.advance_and_skip_spaces()
        premises = list(self.iter_typing_rule_premise())
        self.advance_and_skip_spaces()
        return TypingRule(name, premises, self.parse_type_assertion(parse_schema=True, variable_assertion=False))

    parse = parse_term


def parse_variable(string: str) -> Variable:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, string)

    with LambdaParser(tokens, EMPTY_SIGNATURE) as parser:
        return parser.parse_variable(parse_schema=False)


@overload
def parse_term(signature: LambdaSignature, string: str, *, only_untyped: Literal[False] = False, only_typed: Literal[False] = False) -> Term: ...
@overload
def parse_term(signature: LambdaSignature, string: str, *, only_untyped: Literal[True], only_typed: Literal[False] = False) -> UntypedTerm: ...
@overload
def parse_term(signature: LambdaSignature, string: str, *, only_untyped: Literal[False] = False, only_typed: Literal[True]) -> TypedTerm: ...
@overload
def parse_term(signature: LambdaSignature, string: str, *, only_untyped: bool = False, only_typed: bool = False) -> Term: ...
def parse_term(signature: LambdaSignature, string: str, *, only_untyped: bool = False, only_typed: bool = False) -> Term:
    tokens = tokenize_lambda_string(signature, string)

    with LambdaParser(tokens, signature) as parser:
        return parser.parse_term(parse_schema=False, only_untyped=only_untyped, only_typed=only_typed)


def parse_pure_term(string: str) -> UntypedTerm:
    return parse_term(EMPTY_SIGNATURE, string, only_untyped=True)


def parse_variable_placeholder(string: str) -> VariablePlaceholder:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, string)

    with LambdaParser(tokens, EMPTY_SIGNATURE) as parser:
        return parser.parse_variable(parse_schema=True)


def parse_term_placeholder(string: str) -> TermPlaceholder:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, string)

    with LambdaParser(tokens, EMPTY_SIGNATURE) as parser:
        return parser.parse_term_placeholder()


def parse_pure_term_schema(string: str) -> TermSchema:
    return parse_term_schema(EMPTY_SIGNATURE, string)


def parse_term_schema(signature: LambdaSignature, string: str) -> TermSchema:
    tokens = tokenize_lambda_string(signature, string)

    with LambdaParser(tokens, signature) as parser:
        return parser.parse_term(parse_schema=True)


def parse_type(signature: LambdaSignature, string: str) -> SimpleType:
    tokens = tokenize_lambda_string(signature, string)

    with LambdaParser(tokens, signature) as parser:
        return parser.parse_type(parse_schema=False)


def parse_type_placeholder(string: str) -> TypePlaceholder:
    tokens = tokenize_lambda_string(EMPTY_SIGNATURE, string)

    with LambdaParser(tokens, EMPTY_SIGNATURE) as parser:
        return parser.parse_type_placeholder()


def parse_type_schema(signature: LambdaSignature, string: str) -> SimpleTypeSchema:
    tokens = tokenize_lambda_string(signature, string)

    with LambdaParser(tokens, signature) as parser:
        return parser.parse_type(parse_schema=True)


def parse_type_assertion(signature: LambdaSignature, string: str) -> TypeAssertion:
    tokens = tokenize_lambda_string(signature, string)

    with LambdaParser(tokens, signature) as parser:
        return parser.parse_type_assertion(parse_schema=False, variable_assertion=False)


def parse_variable_assertion(signature: LambdaSignature, string: str) -> VariableTypeAssertion:
    tokens = tokenize_lambda_string(signature, string)

    with LambdaParser(tokens, signature) as parser:
        return parser.parse_type_assertion(parse_schema=False, variable_assertion=True)


def parse_typing_rule(signature: LambdaSignature, string: str) -> TypingRule:
    tokens = tokenize_lambda_string(signature, string)

    with LambdaParser(tokens, signature) as parser:
        return parser.parse_typing_rule()


def parse_pure_typing_rule(string: str) -> TypingRule:
    return parse_typing_rule(EMPTY_SIGNATURE, string)
