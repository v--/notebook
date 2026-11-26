from typing import override

from notebook.math.lambda_.terms import UntypedAbstraction, UntypedApplication, UntypedTerm
from notebook.math.lambda_.variables import get_free_variables

from .strategies import Reduction


class EtaReduction(Reduction):
    @override
    def try_contract_redex(self, term: UntypedTerm) -> UntypedTerm | None:
        if (
            isinstance(term, UntypedAbstraction) and
            isinstance(term.body, UntypedApplication) and
            term.var not in get_free_variables(term.body.left) and
            term.var == term.body.right
        ):
            return term.body.left

        return None
