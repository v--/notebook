from collections.abc import Sequence
from typing import cast

from .exceptions import FormalLogicError
from .formulas import EqualityFormula
from .substitution import AtomicLogicSubstitution, apply_substitution_to_formula
from .terms import FunctionApplication, Term, Variable
from .variables import get_term_variables


class UnificationError(FormalLogicError):
    pass


def unify(system: Sequence[EqualityFormula]) -> AtomicLogicSubstitution:
    current_system = list(system)
    next_system = current_system
    perform_operations = len(system) > 0

    while perform_operations:
        for i, eq in enumerate(current_system):
            # Delete
            if eq.left == eq.right:
                next_system = current_system[:i] + current_system[i + 1:]

                if len(next_system) == 0:
                    perform_operations = False

                break

            # Decompose
            if (
                isinstance(eq.left, FunctionApplication) and
                isinstance(eq.right, FunctionApplication) and
                eq.left.symbol == eq.right.symbol
            ):
                next_system = [
                    *current_system[:i],
                    *(EqualityFormula(l, r) for l, r in zip(eq.left.arguments, eq.right.arguments, strict=True)),
                    *current_system[i + 1:]
                ]

                break

            # Orient
            if not isinstance(eq.left, Variable) and isinstance(eq.right, Variable):
                next_system = [*current_system[:i], EqualityFormula(eq.right, eq.left), *current_system[i + 1:]]
                break

            # Eliminate
            if (
                isinstance(eq.left, Variable) and
                eq.left not in get_term_variables(eq.right) and
                any(eq.left == e.left or eq.left in get_term_variables(e.right) for e in current_system if e != eq)
            ):
                sub = AtomicLogicSubstitution(variable_mapping={eq.left: eq.right})
                next_system = cast(list[EqualityFormula], [
                    *(apply_substitution_to_formula(e, sub) for e in current_system[:i]),
                    eq,
                    *(apply_substitution_to_formula(e, sub) for e in current_system[i + 1:]),
                ])
                break

            # Deduplicate
            if (j := min((k for k in range(i + 1, len(current_system)) if current_system[k] == eq), default=None)):
                next_system = [
                    *current_system[:i],
                    eq,
                    *current_system[i + 1:j],
                    *current_system[j + 1:]
                ]
                break
        else:
            perform_operations = False

        current_system = next_system

    variable_mapping = dict[Variable, Term]()

    for i, eq in enumerate(current_system):
        if not isinstance(eq.left, Variable) or eq.left in get_term_variables(eq.right):
            raise UnificationError(f'Cannot unify the equation {eq}')

        for j, e in enumerate(current_system):
            if i != j and (eq.left == e.left or eq.left in get_term_variables(e.right)):
                raise UnificationError(f'Cannot unify the equations {eq} and {e}')

        variable_mapping[eq.left] = eq.right

    return AtomicLogicSubstitution(variable_mapping=variable_mapping)
