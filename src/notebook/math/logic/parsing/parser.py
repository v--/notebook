from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Literal, cast, overload

from ....parsing import GreekIdentifier, IdentifierParserMixin, Parser
from ....support.substitution import ImproperSubstitutionSymbol
from ..alphabet import BinaryConnective, PropConstant, Quantifier, UnaryPrefix
from ..deduction import (
    Marker,
    NaturalDeductionPremise,
    NaturalDeductionRule,
)
from ..formulas import (
    ConnectiveFormula,
    ConnectiveFormulaSchema,
    ConstantFormula,
    EqualityFormula,
    EqualityFormulaSchema,
    Formula,
    FormulaPlaceholder,
    FormulaSchema,
    FormulaSchemaSubstitutionSpec,
    FormulaWithSubstitution,
    NegationFormula,
    NegationFormulaSchema,
    PredicateApplication,
    PredicateApplicationSchema,
    QuantifierFormula,
    QuantifierFormulaSchema,
)
from ..propositional import PROPOSITIONAL_SIGNATURE
from ..signature import (
    EMPTY_SIGNATURE,
    FormalLogicSignature,
    FunctionSymbol,
    PredicateSymbol,
    SignatureSymbol,
)
from ..terms import (
    EigenvariableSchemaSubstitutionSpec,
    FunctionApplication,
    FunctionApplicationSchema,
    Term,
    TermPlaceholder,
    TermSchema,
    TermSchemaSubstitutionSpec,
    TermSubstitutionSpec,
    Variable,
    VariablePlaceholder,
)
from .parser_context import LogicParserContext
from .tokenizer import tokenize_formal_logic_string
from .tokens import LogicToken, LogicTokenKind


@dataclass
class UndeterminedPlaceholder:
    identifier: GreekIdentifier


class FormalLogicParser(IdentifierParserMixin[LogicTokenKind, LogicToken], Parser[LogicToken]):
    signature: FormalLogicSignature

    def __init__(self, signature: FormalLogicSignature, source: str, tokens: Sequence[LogicToken]) -> None:
        super().__init__(source, tokens)
        self.signature = signature

    def _parse_undetermined_placeholder(self) -> UndeterminedPlaceholder:
        identifier = self.parse_greek_identifier('GREEK_IDENTIFIER')
        return UndeterminedPlaceholder(identifier)

    def parse_term_placeholder(self) -> TermPlaceholder:
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
    def _iter_prefix_notation_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: Literal[False]) -> Iterable[Term]: ...
    @overload
    def _iter_prefix_notation_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: Literal[True]) -> Iterable[TermSchema]: ...
    @overload
    def _iter_prefix_notation_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: bool) -> Iterable[Term] | Iterable[TermSchema]: ...
    def _iter_prefix_notation_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: bool) -> Iterable[Term] | Iterable[TermSchema]:
        head = self.peek()

        if not head or head.kind != 'LEFT_PARENTHESIS':
            raise context.annotate_context_error(f'Expected a parenthesized argument list for the {symbol.get_kind_string()} {symbol}')

        head = self.advance_and_peek()

        if head and head.kind == 'RIGHT_PARENTHESIS':
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
    def _iter_condensed_notation_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: Literal[False]) -> Iterable[Term]: ...
    @overload
    def _iter_condensed_notation_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: Literal[True]) -> Iterable[TermSchema]: ...
    @overload
    def _iter_condensed_notation_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: bool) -> Iterable[Term] | Iterable[TermSchema]: ...
    def _iter_condensed_notation_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: bool) -> Iterable[Term] | Iterable[TermSchema]:
        head = self.peek()

        if head and head.kind == 'LEFT_PARENTHESIS':
            raise context.annotate_context_error(f'Parentheses are disallowed for the symbol {symbol} that uses condensed notation')

        for _ in range(symbol.arity):
            head = self.peek()

            if not head:
                raise context.annotate_context_error(f'Insufficient arguments for the symbol {symbol} of arity {symbol.arity}')

            if head.kind == 'RIGHT_PARENTHESIS':
                raise context.annotate_context_error(f'Parentheses are disallowed for the symbol {symbol} that uses condensed notation')

            yield self.parse_term(parse_schema=parse_schema)

    @overload
    def _parse_application_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: Literal[False]) -> Sequence[Term]: ...
    @overload
    def _parse_application_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: Literal[True]) -> Sequence[TermSchema]: ...
    @overload
    def _parse_application_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: bool) -> Sequence[Term] | Sequence[TermSchema]: ...
    def _parse_application_args(self, context: LogicParserContext, symbol: SignatureSymbol, *, parse_schema: bool) -> Sequence[Term] | Sequence[TermSchema]:
        # A narrower type leads to duplicated code
        arguments = list[Term | TermSchema]()

        match symbol.notation:
            case 'INFIX':
                raise context.annotate_token_error(f'Expected a prefix proper symbol, but got {symbol}')

            case 'PREFIX':
                self.advance()
                arguments = list(self._iter_prefix_notation_args(context, symbol, parse_schema=parse_schema))

            case 'CONDENSED':
                self.advance()
                arguments = list(self._iter_condensed_notation_args(context, symbol, parse_schema=parse_schema))

        if symbol.arity != len(arguments):
            raise context.annotate_context_error(f'Expected {symbol.arity} arguments for the {symbol.get_kind_string()} {symbol}, but got {len(arguments)}')

        return cast(Sequence[TermSchema] | Sequence[Term], arguments)

    def _parse_constant_formula(self) -> ConstantFormula:
        head = self.peek_unsafe()
        self.advance()
        return ConstantFormula(
            PropConstant(head.value)
        )

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
    def _parse_parenthesized(self, context: LogicParserContext, *, parse_schema: Literal[False]) -> FunctionApplication | ConnectiveFormula | EqualityFormula | PredicateApplication: ...
    @overload
    def _parse_parenthesized(self, context: LogicParserContext, *, parse_schema: Literal[True]) -> FunctionApplicationSchema | ConnectiveFormulaSchema | EqualityFormulaSchema | PredicateApplicationSchema: ...
    @overload
    def _parse_parenthesized(self, context: LogicParserContext, *, parse_schema: bool) -> FunctionApplication | ConnectiveFormula | EqualityFormula | PredicateApplication | FunctionApplicationSchema | ConnectiveFormulaSchema | EqualityFormulaSchema | PredicateApplicationSchema: ...
    def _parse_parenthesized(self, context: LogicParserContext, *, parse_schema: bool) -> FunctionApplication | ConnectiveFormula | EqualityFormula | PredicateApplication | FunctionApplicationSchema | ConnectiveFormulaSchema | EqualityFormulaSchema | PredicateApplicationSchema:  # noqa: C901,PLR0915
        left_context = LogicParserContext(self)
        left = self._parse(left_context, parse_schema=parse_schema)
        left_context.close_at_previous_token()
        head = self.peek()
        right: Term | Formula | TermSchema | FormulaSchema

        if not head:
            raise context.annotate_context_error(f'Parenthesized {'expression schema' if parse_schema else 'expression'} must have a propositional connective, infix proper symbol or equality after the first subexpression')

        match head.kind:
            case 'BINARY_CONNECTIVE':
                if isinstance(left, UndeterminedPlaceholder):
                    left = FormulaPlaceholder(left.identifier)

                if not isinstance(left, Formula | FormulaSchema):
                    raise left_context.annotate_context_error(f'The first argument of a connective {'formula schema' if parse_schema else 'formula'} must itself be a {'formula schema' if parse_schema else 'formula'}')

                connective = BinaryConnective(head.value)
                head = self.advance_and_peek()

                if not head or head.kind == 'RIGHT_PARENTHESIS':
                    raise context.annotate_context_error(f'Binary connective {'formula schemas' if parse_schema else 'formulas'} must have a second subformula')

                right = self.parse_formula(parse_schema=parse_schema)
                head = self.peek()

                if not head or head.kind != 'RIGHT_PARENTHESIS':
                    raise context.annotate_context_error(f'Binary connective {'formula schemas' if parse_schema else 'formulas'} must have a closing parenthesis')

                self.advance()

                if parse_schema:
                    assert isinstance(left, FormulaSchema)
                    assert isinstance(right, FormulaSchema)
                    return ConnectiveFormulaSchema(connective, left, right)

                assert isinstance(left, Formula)
                assert isinstance(right, Formula)
                return ConnectiveFormula(connective, left, right)

            case 'EQUALITY':
                if isinstance(left, UndeterminedPlaceholder):
                    left = TermPlaceholder(left.identifier)

                if not isinstance(left, Term | TermSchema):
                    raise left_context.annotate_context_error(f'The first argument of an equality {'formula schema' if parse_schema else 'formula'} must be a {'term schema' if parse_schema else 'term'}')

                head = self.advance_and_peek()

                if not head or head.kind == 'RIGHT_PARENTHESIS':
                    raise context.annotate_context_error(f'Equality {'formula schemas' if parse_schema else 'formulas'} must have a second term')

                right = self.parse_term(parse_schema=parse_schema)
                head = self.peek()

                if not head or head.kind != 'RIGHT_PARENTHESIS':
                    raise context.annotate_context_error(f'Equality {'formula schemas' if parse_schema else 'formulas'} must have a closing parenthesis')

                self.advance()

                if parse_schema:
                    assert isinstance(left, TermSchema)
                    assert isinstance(right, TermSchema)
                    return EqualityFormulaSchema(left, right)

                assert isinstance(left, Term)
                assert isinstance(right, Term)
                return EqualityFormula(left, right)

            case 'SIGNATURE_SYMBOL':
                if isinstance(left, UndeterminedPlaceholder):
                    left = TermPlaceholder(left.identifier)

                if not isinstance(left, Term | TermSchema):
                    raise left_context.annotate_context_error(f'The first argument of an infix {'application schema' if parse_schema else 'application'} must be a {'term schema' if parse_schema else 'term'}')

                symbol = self.signature[head.value]

                if symbol and symbol.notation != 'INFIX':
                    raise context.annotate_token_error(f'Expected an infix proper symbol, but got {symbol}')

                head = self.advance_and_peek()

                if not head or head.kind == 'RIGHT_PARENTHESIS':
                    raise context.annotate_context_error(f'Infix {'application schemas' if parse_schema else 'applications'} must have a second term')

                right = self.parse_term(parse_schema=parse_schema)
                head = self.peek()

                if not head or head.kind != 'RIGHT_PARENTHESIS':
                    raise context.annotate_context_error(f'Infix {'expression schemas' if parse_schema else 'applications'} must have a closing parenthesis')

                self.advance()

                if parse_schema:
                    assert isinstance(left, TermSchema)
                    assert isinstance(right, TermSchema)

                    match symbol:
                        case PredicateSymbol():
                            return PredicateApplicationSchema(symbol, [left, right])

                        case FunctionSymbol():
                            return FunctionApplicationSchema(symbol, [left, right])

                assert isinstance(left, Term)
                assert isinstance(right, Term)

                match symbol:
                    case PredicateSymbol():
                        return PredicateApplication(symbol, [left, right])

                    case FunctionSymbol():
                        return FunctionApplication(symbol, [left, right])

            case _:
                raise context.annotate_token_error(f'The symbol {head.value!r} is not an infix operator')

    @overload
    def _parse(self, context: LogicParserContext, *, parse_schema: Literal[False]) -> Term | Formula: ...
    @overload
    def _parse(self, context: LogicParserContext, *, parse_schema: Literal[True]) -> TermSchema | FormulaSchema | UndeterminedPlaceholder: ...
    @overload
    def _parse(self, context: LogicParserContext, *, parse_schema: bool) -> Term | Formula | TermSchema | FormulaSchema | UndeterminedPlaceholder: ...
    def _parse(self, context: LogicParserContext, *, parse_schema: bool) -> Term | Formula | TermSchema | FormulaSchema | UndeterminedPlaceholder:
        head = self.peek()

        if not head:
            raise self.annotate_unexpected_end_of_input()

        match head.kind:
            case 'SIGNATURE_SYMBOL':
                symbol = self.signature[head.value]

                match symbol:
                    case PredicateSymbol():
                        if parse_schema:
                            return PredicateApplicationSchema(symbol, self._parse_application_args(context, symbol, parse_schema=True))

                        return PredicateApplication(symbol, self._parse_application_args(context, symbol, parse_schema=False))

                    case FunctionSymbol():
                        if parse_schema:
                            return FunctionApplicationSchema(symbol, self._parse_application_args(context, symbol, parse_schema=True))

                        return FunctionApplication(symbol, self._parse_application_args(context, symbol, parse_schema=False))

            case 'LATIN_IDENTIFIER':
                return self.parse_variable(parse_schema=parse_schema)

            case 'GREEK_IDENTIFIER':
                if not parse_schema:
                    raise self.annotate_token_error('Placeholders are only allowed in schemas')

                return self._parse_undetermined_placeholder()

            case 'LEFT_PARENTHESIS':
                self.advance()
                return self._parse_parenthesized(context, parse_schema=parse_schema)

            case 'PROP_CONSTANT':
                return self._parse_constant_formula()

            case 'QUANTIFIER':
                return self._parse_quantifier_formula(context, parse_schema=parse_schema)

            case 'UNARY_CONNECTIVE' if head.value == UnaryPrefix.NEGATION.value:
                return self._parse_negation_formula(parse_schema=parse_schema)

            case _:
                raise self.annotate_token_error('Unexpected token')

    @overload
    def parse_term(self, *, parse_schema: Literal[False]) -> Term: ...
    @overload
    def parse_term(self, *, parse_schema: Literal[True]) -> TermSchema: ...
    @overload
    def parse_term(self, *, parse_schema: bool) -> Term | TermSchema: ...
    def parse_term(self, *, parse_schema: bool) -> Term | TermSchema:
        if not self.peek():
            raise self.annotate_unexpected_end_of_input()

        context = LogicParserContext(self)
        result = self._parse(context, parse_schema=parse_schema)

        if isinstance(result, UndeterminedPlaceholder):
            return TermPlaceholder(result.identifier)

        if isinstance(result, Formula | FormulaSchema):
            raise context.annotate_context_error(f'Encountered a {'formula schema' if parse_schema else 'formula'} where a {'term schema' if parse_schema else 'term'} was expected')

        return result


    @overload
    def parse_formula(self, *, parse_schema: Literal[False]) -> Formula: ...
    @overload
    def parse_formula(self, *, parse_schema: Literal[True]) -> FormulaSchema: ...
    @overload
    def parse_formula(self, *, parse_schema: bool) -> Formula | FormulaSchema: ...
    def parse_formula(self, *, parse_schema: bool) -> Formula | FormulaSchema:
        if not self.peek():
            raise self.annotate_unexpected_end_of_input()

        context = LogicParserContext(self)
        result = self._parse(context, parse_schema=parse_schema)

        if isinstance(result, UndeterminedPlaceholder):
            return FormulaPlaceholder(result.identifier)

        if isinstance(result, Term | TermSchema):
            raise context.annotate_context_error(f'Encountered a {'term schema' if parse_schema else 'term'} where a {'formula schema' if parse_schema else 'formula'} was expected')

        return result

    @overload
    def parse_term_substitution_spec(self, *, parse_schema: Literal[False]) -> TermSubstitutionSpec: ...
    @overload
    def parse_term_substitution_spec(self, *, parse_schema: Literal[True]) -> TermSchemaSubstitutionSpec | EigenvariableSchemaSubstitutionSpec: ...
    @overload
    def parse_term_substitution_spec(self, *, parse_schema: bool) -> TermSubstitutionSpec | TermSchemaSubstitutionSpec | EigenvariableSchemaSubstitutionSpec: ...
    def parse_term_substitution_spec(self, *, parse_schema: bool) -> TermSubstitutionSpec | TermSchemaSubstitutionSpec | EigenvariableSchemaSubstitutionSpec:
        context = LogicParserContext(self)
        src = self.parse_variable(parse_schema=parse_schema)
        head = self.peek()

        if not head or head.kind != 'SUBSTITUTION_CONNECTIVE':
            raise context.annotate_context_error(f'Expected {ImproperSubstitutionSymbol.CONNECTIVE} after the variable in a substitution')

        self.advance()
        dest = self.parse_term(parse_schema=parse_schema)
        head = self.peek()

        if head and head.kind == 'ASTERISK':
            if not parse_schema:
                raise context.annotate_token_error('Can only place an eigenvariable marker on a schema')

            assert isinstance(src, VariablePlaceholder)

            if not isinstance(dest, VariablePlaceholder):
                raise context.annotate_token_error('Cannot place an eigenvariable marker on a more general term')

            self.advance()
            return EigenvariableSchemaSubstitutionSpec(src, dest)

        if parse_schema:
            assert isinstance(src, VariablePlaceholder)
            assert isinstance(dest, TermSchema)
            return TermSchemaSubstitutionSpec(src, dest)

        assert isinstance(src, Variable)
        assert isinstance(dest, Term)
        return TermSubstitutionSpec(src, dest)

    @overload
    def parse_formula_with_substitution(self, *, parse_schema: Literal[False]) -> FormulaWithSubstitution: ...
    @overload
    def parse_formula_with_substitution(self, *, parse_schema: Literal[True]) -> FormulaSchemaSubstitutionSpec: ...
    @overload
    def parse_formula_with_substitution(self, *, parse_schema: bool) -> FormulaWithSubstitution | FormulaSchemaSubstitutionSpec: ...
    def parse_formula_with_substitution(self, *, parse_schema: bool) -> FormulaWithSubstitution | FormulaSchemaSubstitutionSpec:
        context = LogicParserContext(self)
        formula = self.parse_formula(parse_schema=parse_schema)

        if (head := self.peek()) and head.kind == 'LEFT_BRACKET':
            self.advance()
            sub = self.parse_term_substitution_spec(parse_schema=parse_schema)

            if (head := self.peek()) and head.kind == 'RIGHT_BRACKET':
                self.advance()

                if parse_schema:
                    assert isinstance(formula, FormulaSchema)
                    assert isinstance(sub, TermSchemaSubstitutionSpec | EigenvariableSchemaSubstitutionSpec)
                    return FormulaSchemaSubstitutionSpec(formula, sub)

                assert isinstance(formula, Formula)
                assert isinstance(sub, TermSubstitutionSpec)
                return FormulaWithSubstitution(formula, sub)

            context.close_at_previous_token()
            raise context.annotate_context_error('Unclosed brackets for substitution specification')

        if parse_schema:
            assert isinstance(formula, FormulaSchema)
            return FormulaSchemaSubstitutionSpec(formula)

        assert isinstance(formula, Formula)
        return FormulaWithSubstitution(formula)

    def _parse_natural_deduction_premise(self, premise_context: LogicParserContext) -> NaturalDeductionPremise:
        discharge: FormulaSchemaSubstitutionSpec | None = None

        if (head := self.peek()) and head.kind == 'LEFT_BRACKET':
            head = self.advance_and_peek()

            if head and head.kind == 'RIGHT_BRACKET':
                raise premise_context.annotate_context_error('Empty discharge assumptions are disallowed')

            discharge = self.parse_formula_with_substitution(parse_schema=True)
            head = self.peek()

            if not head or head.kind == 'RIGHT_BRACKET':
                self.advance()
            else:
                premise_context.close_at_previous_token()
                raise premise_context.annotate_context_error('Unclosed brackets for discharge schemas')

        main = self.parse_formula_with_substitution(parse_schema=True)
        return NaturalDeductionPremise(main, discharge)

    def _iter_natural_deduction_premises(self, rule_context: LogicParserContext) -> Iterable[NaturalDeductionPremise]:
        premise_context = LogicParserContext(self)

        while (head := self.peek()) and head.kind != 'RULE_SEQUENT':
            premise_context.reset()
            yield self._parse_natural_deduction_premise(premise_context)
            head = self.peek()

            if not head or head.kind == 'RULE_SEQUENT':
                break

            if head.kind == 'COMMA':
                self.advance()
            else:
                raise rule_context.annotate_context_error('Expected either a separator or a sequent symbol')

        if not self.peek():
            raise rule_context.annotate_context_error('Expected a sequent symbol')

    def parse_natural_deduction_rule(self, name: str) -> NaturalDeductionRule:
        if self.peek() is None:
            raise self.annotate_unexpected_end_of_input()

        rule_context = LogicParserContext(self)
        premises = list(self._iter_natural_deduction_premises(rule_context))
        self.advance()
        return NaturalDeductionRule(name, premises, self.parse_formula_with_substitution(parse_schema=True))


def parse_variable(source: str) -> Variable:
    tokens = tokenize_formal_logic_string(EMPTY_SIGNATURE, source)

    with FormalLogicParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_variable(parse_schema=False)


def parse_variable_placeholder(source: str) -> VariablePlaceholder:
    tokens = tokenize_formal_logic_string(EMPTY_SIGNATURE, source)

    with FormalLogicParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_variable(parse_schema=True)


def parse_term(source: str, signature: FormalLogicSignature = EMPTY_SIGNATURE) -> Term:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_term(parse_schema=False)


def parse_term_placeholder(source: str, signature: FormalLogicSignature = EMPTY_SIGNATURE) -> TermPlaceholder:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_term_placeholder()


def parse_term_schema(source: str, signature: FormalLogicSignature = EMPTY_SIGNATURE) -> TermSchema:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_term(parse_schema=True)


def parse_formula(source: str, signature: FormalLogicSignature = EMPTY_SIGNATURE) -> Formula:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_formula(parse_schema=False)


def parse_propositional_formula(source: str) -> Formula:
    return parse_formula(source, PROPOSITIONAL_SIGNATURE)


def parse_formula_schema(source: str, signature: FormalLogicSignature = EMPTY_SIGNATURE) -> FormulaSchema:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_formula(parse_schema=True)


def parse_term_substitution_spec(source: str, signature: FormalLogicSignature = EMPTY_SIGNATURE) -> TermSubstitutionSpec:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_term_substitution_spec(parse_schema=False)


def parse_term_schema_substitution_spec(source: str, signature: FormalLogicSignature = EMPTY_SIGNATURE) -> TermSchemaSubstitutionSpec | EigenvariableSchemaSubstitutionSpec:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_term_substitution_spec(parse_schema=True)


def parse_formula_with_substitution(source: str, signature: FormalLogicSignature = EMPTY_SIGNATURE) -> FormulaWithSubstitution:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_formula_with_substitution(parse_schema=False)


def parse_formula_schema_with_substitution(source: str, signature: FormalLogicSignature = EMPTY_SIGNATURE) -> FormulaSchemaSubstitutionSpec:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_formula_with_substitution(parse_schema=True)


def parse_formula_placeholder(source: str, signature: FormalLogicSignature = EMPTY_SIGNATURE) -> FormulaPlaceholder:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_formula_placeholder()


def parse_marker(source: str) -> Marker:
    tokens = tokenize_formal_logic_string(EMPTY_SIGNATURE, source)

    with FormalLogicParser(EMPTY_SIGNATURE, source, tokens) as parser:
        return parser.parse_marker()


def parse_natural_deduction_rule(name: str, source: str, signature: FormalLogicSignature = EMPTY_SIGNATURE) -> NaturalDeductionRule:
    tokens = tokenize_formal_logic_string(signature, source)

    with FormalLogicParser(signature, source, tokens) as parser:
        return parser.parse_natural_deduction_rule(name)
