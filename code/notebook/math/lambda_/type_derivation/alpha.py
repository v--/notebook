from notebook.exceptions import UnreachableException

from ..assertions import VariableTypeAssertion
from ..terms import (
    TypedAbstraction,
    TypedApplication,
    TypedTerm,
)
from ..type_systems import ARROW_ELIM_RULE_EXPLICIT, ARROW_INTRO_RULE_EXPLICIT
from ..variables import get_free_variables
from .exceptions import TypeDerivationError
from .substitution import substitute
from .tree import AssumptionTree, RuleApplicationTree, TypeDerivationTree, apply, assume, premise


class NotAlphaEquivalent(BaseException):
    pass


def transform_derivation_impl(tree: TypeDerivationTree, equivalent_term: TypedTerm) -> TypeDerivationTree:
    if isinstance(tree, AssumptionTree):
        if tree.conclusion.term != equivalent_term:
            raise NotAlphaEquivalent

        return tree

    if isinstance(tree, RuleApplicationTree):
        if tree.rule == ARROW_ELIM_RULE_EXPLICIT:
            if not isinstance(equivalent_term, TypedApplication):
                raise NotAlphaEquivalent

            return apply(
                ARROW_ELIM_RULE_EXPLICIT,
                transform_derivation_impl(tree.premises[0].tree, equivalent_term.a),
                transform_derivation_impl(tree.premises[1].tree, equivalent_term.b)
            )

        if tree.rule == ARROW_INTRO_RULE_EXPLICIT:
            term = tree.conclusion.term
            subtree = tree.premises[0].tree
            assert isinstance(term, TypedAbstraction)

            if not isinstance(equivalent_term, TypedAbstraction) or term.var_type != equivalent_term.var_type:
                raise NotAlphaEquivalent

            assertion = VariableTypeAssertion(equivalent_term.var, term.var_type)

            if term.var == equivalent_term.var:
                adjusted_subtree = subtree
            else:
                if equivalent_term.var in get_free_variables(term.sub):
                    raise NotAlphaEquivalent

                adjusted_subtree = substitute(
                    subtree,
                    {term.var: assume(assertion)}
                )

            return apply(
                ARROW_INTRO_RULE_EXPLICIT,
                premise(
                    discharge=assertion,
                    tree=transform_derivation_impl(
                        adjusted_subtree,
                        equivalent_term.sub
                    )
                )
            )

    raise UnreachableException


# This is alg:typed_alpha_conversion in the monograph
def transform_derivation(tree: TypeDerivationTree, equivalent_term: TypedTerm) -> TypeDerivationTree:
    try:
        return transform_derivation_impl(tree, equivalent_term)
    except NotAlphaEquivalent:
        raise TypeDerivationError(f'The terms {tree.conclusion.term} and {equivalent_term} are not α-equivalent') from None
