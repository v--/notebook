from notebook.math.lambda_.parsing import parse_untyped_term
from notebook.math.lambda_.untyped.alpha import are_terms_alpha_equivalent
from notebook.math.lambda_.untyped.reduction.api import fully_reduce_term
from notebook.math.lambda_.untyped.reduction.exceptions import ReductionError
lazy from notebook.math.lambda_.terms.terms import UntypedApplication, UntypedTerm


# ruff: disable[multiple-spaces-after-operator]
true =  parse_untyped_term('(λt.(λf.t))')
false = parse_untyped_term('(λt.(λf.f))')

not_ =    parse_untyped_term('(λa.(λt.(λf.((af)t))))')
and_ =    parse_untyped_term('(λa.(λb.(λt.(λf.((a((bt)f))((bf)f))))))')
or_ =     parse_untyped_term('(λa.(λb.(λt.(λf.((a((bt)t))((bt)f))))))')
implies = parse_untyped_term('(λa.(λb.(λt.(λf.((a((bt)f))((bt)t))))))')
iff =     parse_untyped_term('(λa.(λb.(λt.(λf.((a((bt)f))((bf)t))))))')
# ruff: enable[multiple-spaces-after-operator]


def is_term_truthy(term: UntypedTerm) -> bool:
    return are_terms_alpha_equivalent(term, true)


def is_term_falsy(term: UntypedTerm) -> bool:
    return are_terms_alpha_equivalent(term, false)


def apply_boolean_function(term: UntypedTerm, *args: bool) -> bool:
    app = term

    for arg in args:
        app = UntypedApplication(app, true if arg else false)

    result = fully_reduce_term(app)

    if is_term_truthy(result):
        return True

    if is_term_falsy(result):
        return False

    raise ReductionError(f'Not a valid logical term: {term}')
