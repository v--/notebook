from collections.abc import Iterable, Sequence
from typing import Literal, cast, overload

from ....parsing import IdentifierParserMixin, Parser
from ..alphabet import BinaryConnective, PropConstant, Quantifier, UnaryConnective
from ..deduction import Marker, NaturalDeductionPremise, NaturalDeductionRule
from ..formulas import (
    ConnectiveFormula,
    ConnectiveFormulaSchema,
    ConstantFormula,
    EqualityFormula,
    EqualityFormulaSchema,
    ExtendedFormulaSchema,
    Formula,
    FormulaPlaceholder,
    FormulaSchema,
    NegationFormula,
    NegationFormulaSchema,
    PredicateFormula,
    PredicateFormulaSchema,
    QuantifierFormula,
    QuantifierFormulaSchema,
    SubstitutionSchema,
)
from ..propositional import PROPOSITIONAL_SIGNATURE
from ..signature import EMPTY_SIGNATURE, FormalLogicSignature
from ..terms import (
    ExtendedTermSchema,
    FunctionTerm,
    FunctionTermSchema,
    StarredTermSchema,
    Term,
    TermPlaceholder,
    TermSchema,
    Variable,
    VariablePlaceholder,
)
from .parser_context import LogicParserContext
from .tokenizer import tokenize_formal_logic_string
from .tokens import LogicToken, LogicTokenKind


class FormalLogicParser(IdentifierParserMixin[LogicTokenKind, LogicToken], Parser[LogicToken]):
    signature: FormalLogicSignature

    def __init__(self, signature: FormalLogicSignature, source: str, tokens: Sequence[LogicToken]) -> None:
        super().__init__(source, tokens)
        self.signature = signature

    def _parse_term_placeholder(self) -> TermPlaceholder:
        identifier = self.parse_greek_identifier('GREEK_IDENTIFIER')
        return TermPlaceholder(identifier)

    def parse_formula_placeholder(self) -> FormulaPlaceholder:
        identifier = self.parse_greek_identifier('GREEK_IDENTIFIER')
        return FormulaPlaceholder(identifier)

    def parse_marker(self) -> Marker:
        identifier = self.parse_latin_identifier('LATIN_IDENTIFIER')
        return Marker(identifier)

    @overload
    def parse_variable(self, *, parse_schema: Literal[False]) -> Variable: ...
    @overload
    def parse_variable(self, *, parse_schema: Literal[True]) -> VariablePlaceholder: ...
    @overload
    def parse_variable(self, *, parse_schema: bool) -> Variable | VariablePlaceholder: ...
    def parse_variable(self, *, parse_schema: bool) -> Variable | VariablePlaceholder:
        identifier = self.parse_latin_identifier('LATIN_IDENTIFIER')

        if parse_schema:
            return VariablePlaceholder(identifier)

        return Variable(identifier)

    @overload
    def _parse_args(self, context: LogicParserContext, arity: int, *, parse_schema: Literal[False]) -> Iterable[Term]: ...
    @overload
    def _parse_args(self, context: LogicParserContext, arity: int, *, parse_schema: Literal[True]) -> Iterable[TermSchema]: ...
    @overload
    def _parse_args(self, context: LogicParserContext, arity: int, *, parse_schema: bool) -> Iterable[Term] | Iterable[TermSchema]: ...
    def _parse_args(self, context: LogicParserContext, arity: int, *, parse_schema: bool) -> Iterable[Term] | Iterable[TermSchema]:
        if (head := self.advance_and_peek()) and head.kind == 'RIGHT_PARENTHESIS':
            if arity == 0:
                raise context.annotate_context_error('Avoid the argument list at all when zero arguments are expected')

            raise context.annotate_context_error('Empty argument lists are disallowed')

        while True:
            head = self.peek()

            if not head:
                raise context.annotate_context_error('Unclosed argument list')

            if head.kind == 'RIGHT_PARENTHESIS':
                raise context.annotate_context_error('Unexpected closing parenthesis for argument list')

            yield self.parse_term(parse_schema=parse_schema)

            head = self.peek()

            if not head:
                raise context.annotate_context_error('Unclosed argument list')

            match head.kind:
                case 'COMMA':
                    self.advance()

                case 'RIGHT_PARENTHESIS':
                    self.advance()
                    return

                case _:
                    raise self.annotate_token_error('Unexpected token')

    @overload
    def _parse_function_like(self, context: LogicParserContext, arity: int, *, parse_schema: Literal[False]) -> tuple[str, Sequence[Term]]: ...
    @overload
    def _parse_function_like(self, context: LogicParserContext, arity: int, *, parse_schema: Literal[True]) -> tuple[str, Sequence[TermSchema]]: ...
    @overload
    def _parse_function_like(self, context: LogicParserContext, arity: int, *, parse_schema: bool) -> tuple[str, Sequence[Term]] | tuple[str, Sequence[TermSchema]]: ...
    def _parse_function_like(self, context: LogicParserContext, arity: int, *, parse_schema: bool) -> tuple[str, Sequence[Term]] | tuple[str, Sequence[TermSchema]]:
        name = self.peek_unsafe().value
        self.advance()

        # A narrower type leads to duplicated code
        arguments = list[Term | TermSchema]()

        if (head := self.peek()) and head.kind == 'LEFT_PARENTHESIS':
            arguments = list(self._parse_args(context,arity, parse_schema=parse_schema))

            if arity != len(arguments):
                raise context.annotate_context_error(f'Expected {arity} arguments for {name} but got {len(arguments)}')

        return cast(
            tuple[str, Sequence[Term]] | tuple[str, Sequence[TermSchema]],
            (name, arguments)
        )

    @overload
    def parse_term(self, *, parse_schema: Literal[False]) -> Term: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[True]) -> TermSchema: ...
    @overload
    def parse_term(self, *, parse_schema: bool) -> Term | TermSchema: ...
    def parse_term(self, *, parse_schema: bool) -> Term | TermSchema:
        head = self.peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        match head.kind:
            case 'SIGNATURE_SYMBOL':
                symbol = self.signature.get_symbol(head.value)

                if symbol.kind == 'PREDICATE':
                    raise self.annotate_token_error(f'Unexpected predicate symbol while parsing {'term schema' if parse_schema else 'term'}')

                context = LogicParserContext(self)

                if parse_schema:
                    return FunctionTermSchema(*self._parse_function_like(context, symbol.arity, parse_schema=True))

                return FunctionTerm(*self._parse_function_like(context, symbol.arity, parse_schema=False))

            case 'LATIN_IDENTIFIER':
                return self.parse_variable(parse_schema=parse_schema)

            case 'GREEK_IDENTIFIER':
                return self._parse_term_placeholder()

            case _:
                raise self.annotate_token_error('Unexpected token')

    def parse_extended_term_schema(self) -> ExtendedTermSchema:
        base_schema = self.parse_term(parse_schema=True)
        head = self.peek()

        if not head or head.kind != 'STAR':
            return base_schema

        self.advance()
        return StarredTermSchema(base_schema)

    def _parse_constant_formula(self) -> ConstantFormula:
        head = self.peek_unsafe()
        self.advance()
        return ConstantFormula(
            PropConstant(head.value)
        )

    @overload
    def _parse_binary_formula(self, context: LogicParserContext, *, parse_schema: Literal[False]) -> EqualityFormula | ConnectiveFormula: ...
    @overload
    def _parse_binary_formula(self, context: LogicParserContext, *, parse_schema: Literal[True]) -> EqualityFormulaSchema | ConnectiveFormulaSchema: ...
    @overload
    def _parse_binary_formula(self, context: LogicParserContext, *, parse_schema: bool) -> EqualityFormula | EqualityFormulaSchema | ConnectiveFormula | ConnectiveFormulaSchema: ...
    def _parse_binary_formula(self, context: LogicParserContext, *, parse_schema: bool) -> EqualityFormula | EqualityFormulaSchema | ConnectiveFormula | ConnectiveFormulaSchema:
        head = self.advance_and_peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        a_context = LogicParserContext(self)
        a_term: Term | TermSchema | None = None
        a_form: Formula | FormulaSchema | None = None

        if head.kind == 'LATIN_IDENTIFIER' or (head.kind == 'SIGNATURE_SYMBOL' and self.signature.get_symbol(head.value).kind == 'FUNCTION'):
            a_term = self.parse_term(parse_schema=parse_schema)
        else:
            a_form = self.parse_formula(parse_schema=parse_schema)

        a_context.close_at_previous_token()
        head = self.peek()

        if head and head.kind == 'EQUALITY':
            if a_term is None:
                raise a_context.annotate_context_error(f'The left side of an equality {'formula schema' if parse_schema else 'formula'} must be a term')

            head = self.advance_and_peek()

            if not head:
                raise context.annotate_context_error(f'Unclosed parentheses for equality {'formula schema' if parse_schema else 'formula'}')

            if head.kind == 'RIGHT_PARENTHESIS':
                raise context.annotate_context_error(f'Equality {'formula schemas' if parse_schema else 'formulas'} must have a second term')

            b_term = self.parse_term(parse_schema=parse_schema)

            if (head := self.peek()) and head.kind == 'RIGHT_PARENTHESIS':
                self.advance()

                if parse_schema:
                    assert isinstance(a_term, TermSchema)
                    assert isinstance(b_term, TermSchema)
                    return EqualityFormulaSchema(a_term, b_term)

                assert isinstance(a_term, Term)
                assert isinstance(b_term, Term)
                return EqualityFormula(a_term, b_term)

            context.close_at_previous_token()
            raise context.annotate_context_error(f'Unclosed parentheses for equality {'formula schema' if parse_schema else 'formula'}')

        if head and head.kind == 'BINARY_CONNECTIVE':
            connective = BinaryConnective(head.value)

            if a_form is None:
                raise a_context.annotate_context_error(f'The left side of a binary {'formula schema' if parse_schema else 'formula'} must be a {'formula schema' if parse_schema else 'formula'}')

            head = self.advance_and_peek()

            if not head:
                raise context.annotate_context_error(f'Unclosed parentheses for binary {'formula schema' if parse_schema else 'formula'}')

            if head.kind == 'RIGHT_PARENTHESIS':
                raise context.annotate_context_error(f'Binary {'formula schemas' if parse_schema else 'formulas'} must have a second subformula')

            b_form = self.parse_formula(parse_schema=parse_schema)

            if (head := self.peek()) and head.kind == 'RIGHT_PARENTHESIS':
                self.advance()

                if parse_schema:
                    assert isinstance(a_form, FormulaSchema)
                    assert isinstance(b_form, FormulaSchema)
                    return ConnectiveFormulaSchema(connective, a_form, b_form)

                assert isinstance(a_form, Formula)
                assert isinstance(b_form, Formula)
                return ConnectiveFormula(connective, a_form, b_form)

            context.close_at_previous_token()
            raise context.annotate_context_error(f'Unclosed parentheses for binary {'formula schema' if parse_schema else 'formula'}')

        raise context.annotate_context_error(f'Binary {'formula schema' if parse_schema else 'formula'} must have a connective after the first subformula')

    @overload
    def _parse_negation_formula(self, *, parse_schema: Literal[False]) -> NegationFormula: ...
    @overload
    def _parse_negation_formula(self, *, parse_schema: Literal[True]) -> NegationFormulaSchema: ...
    @overload
    def _parse_negation_formula(self, *, parse_schema: bool) -> NegationFormula | NegationFormulaSchema: ...
    def _parse_negation_formula(self, *, parse_schema: bool) -> NegationFormula | NegationFormulaSchema:
        self.advance()

        if parse_schema:
            return NegationFormulaSchema(self.parse_formula(parse_schema=True))

        return NegationFormula(self.parse_formula(parse_schema=False))

    @overload
    def _parse_quantifier_formula(self, context: LogicParserContext, *, parse_schema: Literal[False]) -> QuantifierFormula: ...
    @overload
    def _parse_quantifier_formula(self, context: LogicParserContext, *, parse_schema: Literal[True]) -> QuantifierFormulaSchema: ...
    @overload
    def _parse_quantifier_formula(self, context: LogicParserContext, *, parse_schema: bool) -> QuantifierFormula | QuantifierFormulaSchema: ...
    def _parse_quantifier_formula(self, context: LogicParserContext, *, parse_schema: bool) -> QuantifierFormula | QuantifierFormulaSchema:
        q = Quantifier(self.peek_unsafe().value)
        head = self.advance_and_peek()

        if not head or head.kind != 'LATIN_IDENTIFIER':
            raise context.annotate_context_error('Expected a variable after the quantifier')

        var = self.parse_variable(parse_schema=parse_schema)
        head = self.peek()

        if head and head.kind == 'DOT':
            self.advance()
        else:
            context.close_at_previous_token()
            raise context.annotate_context_error('Expected dot after variable')

        if parse_schema:
            assert isinstance(var, VariablePlaceholder)
            return QuantifierFormulaSchema(q, var, self.parse_formula(parse_schema=True))

        assert isinstance(var, Variable)
        return QuantifierFormula(q, var, self.parse_formula(parse_schema=False))

    @overload
    def parse_formula(self, *, parse_schema: Literal[False]) -> Formula: ...
    @overload
    def parse_formula(self, *, parse_schema: Literal[True]) -> FormulaSchema: ...
    @overload
    def parse_formula(self, *, parse_schema: bool) -> Formula | FormulaSchema: ...
    def parse_formula(self, *, parse_schema: bool) -> Formula | FormulaSchema:
        head = self.peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        match head.kind:
            case 'LEFT_PARENTHESIS':
                context = LogicParserContext(self)
                return self._parse_binary_formula(context, parse_schema=parse_schema)

            case 'PROP_CONSTANT':
                return self._parse_constant_formula()

            case 'QUANTIFIER':
                context = LogicParserContext(self)
                return self._parse_quantifier_formula(context, parse_schema=parse_schema)

            case 'UNARY_CONNECTIVE' if head.value == UnaryConnective.NEGATION.value:
                return self._parse_negation_formula(parse_schema=parse_schema)

            case 'SIGNATURE_SYMBOL':
                symbol = self.signature.get_symbol(head.value)

                if symbol.kind == 'FUNCTION':
                    raise self.annotate_token_error(f'Unexpected function symbol while parsing {'term schema' if parse_schema else 'term'}')

                context = LogicParserContext(self)

                if parse_schema:
                    return PredicateFormulaSchema(*self._parse_function_like(context, symbol.arity, parse_schema=True))

                return PredicateFormula(*self._parse_function_like(context, symbol.arity, parse_schema=False))

            case 'GREEK_IDENTIFIER':
                if parse_schema:
                    return self.parse_formula_placeholder()

                raise self.annotate_token_error('Formula placeholders are only allowed in schemas')

            case _:
                raise self.annotate_token_error('Unexpected token')

    def parse_extended_schema(self) -> ExtendedFormulaSchema:
        base_schema = self.parse_formula(parse_schema=True)
        head = self.peek()

        if not head or head.kind != 'LEFT_BRACKET':
            return base_schema

        context = LogicParserContext(self)
        self.advance()
        var = self.parse_variable(parse_schema=True)
        head = self.peek()

        if not head or head.kind != 'SUBSTITUTION_ARROW':
            raise context.annotate_context_error('Expected an arrow in a substitution specification')

        head = self.advance_and_peek()
        dest = self.parse_extended_term_schema()
        head = self.peek()

        if not head or head.kind != 'RIGHT_BRACKET':
            raise context.annotate_context_error('Unclosed substitution specification')

        self.advance()
        return SubstitutionSchema(base_schema, var=var, dest=dest)

    def _parse_natural_deduction_premise(self, premise_context: LogicParserContext) -> NaturalDeductionPremise:
        discharge: FormulaSchema | None = None

        if (head := self.peek()) and head.kind == 'LEFT_BRACKET':
            head = self.advance_and_peek()

            if head and head.kind == 'RIGHT_BRACKET':
                raise premise_context.annotate_context_error('Empty discharge assumptions are disallowed')

            discharge = self.parse_formula(parse_schema=True)
            head = self.peek()

            if not head or head.kind == 'RIGHT_BRACKET':
                self.advance()
            else:
                premise_context.close_at_previous_token()
                raise premise_context.annotate_context_error('Unclosed brackets for discharge schemas')

        main = self.parse_formula(parse_schema=True)
        return NaturalDeductionPremise(main, discharge)

    def _iter_natural_deduction_premises(self, rule_context: LogicParserContext) -> Iterable[NaturalDeductionPremise]:
        premise_context = LogicParserContext(self)

        while (head := self.peek()) and head.kind != 'INFERENCE_RULE_SEQUENT':
            premise_context.reset()
            yield self._parse_natural_deduction_premise(premise_context)
            head = self.peek()

            if not head or head.kind == 'INFERENCE_RULE_SEQUENT':
                break

            if head.kind == 'COMMA':
                self.advance()
            else:
                raise rule_context.annotate_context_error('Expected either a separator or a sequent symbol')

        if not self.peek():
            raise rule_context.annotate_context_error('Expected a sequent symbol')

    def parse_natural_deduction_rule(self) -> NaturalDeductionRule:
        if self.peek() is None:
            raise self.annotate_unexpected_end_of_input()

        rule_context = LogicParserContext(self)
        premises = list(self._iter_natural_deduction_premises(rule_context))
        self.advance()
        return NaturalDeductionRule(premises, self.parse_formula(parse_schema=True))


def parse_variable(source: str) -> Variable:
    tokens = tokenize_formal_logic_string(EMPTY_SIGNATURE, source)

    with FormalLogicParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_variable(parse_schema=False)


def parse_term(signature: FormalLogicSignature, source: str) -> Term:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_term(parse_schema=False)


def parse_formula(signature: FormalLogicSignature, source: str) -> Formula:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_formula(parse_schema=False)


def parse_propositional_formula(source: str) -> Formula:
    return parse_formula(PROPOSITIONAL_SIGNATURE, source)


def parse_formula_schema(signature: FormalLogicSignature, source: str) -> ExtendedFormulaSchema:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_extended_schema()


def parse_formula_placeholder(source: str) -> FormulaPlaceholder:
    tokens = tokenize_formal_logic_string(EMPTY_SIGNATURE, source)

    with FormalLogicParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_formula_placeholder()


def parse_signatureless_formula_schema(source: str) -> ExtendedFormulaSchema:
    return parse_formula_schema(EMPTY_SIGNATURE, source)


def parse_marker(source: str) -> Marker:
    tokens = tokenize_formal_logic_string(EMPTY_SIGNATURE, source)

    with FormalLogicParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_marker()


def parse_natural_deduction_rule(signature: FormalLogicSignature, source: str) -> NaturalDeductionRule:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_natural_deduction_rule()


def parse_signatureless_natural_deduction_rule(source: str) -> NaturalDeductionRule:
    return parse_natural_deduction_rule(EMPTY_SIGNATURE, source)
