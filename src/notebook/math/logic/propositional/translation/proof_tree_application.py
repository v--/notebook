from typing import TYPE_CHECKING

from notebook.math.logic.deduction import (
    AssumptionTree,
    MarkedFormula,
    ProofTree,
    RuleApplicationTree,
    apply,
    assume,
    premise_config,
)
from notebook.math.logic.instantiation import AtomicLogicSchemaInstantiation
from notebook.math.logic.propositional.formula_conversion import convert_to_prop_formula
from notebook.support.coderefs import collector

from .base import PropFormulaTranslation
from .formula_application import apply_prop_formula_translation


if TYPE_CHECKING:
    from collections.abc import Mapping

    from notebook.math.logic.formulas import Formula
    from notebook.math.logic.propositional.formulas import PropVariable


# Proof trees use general formulas, so when translating them we must first convert them to propositional formulas and then translate them.
# Quite silly, but our goal is only to demonstrate the correctness of an algorithm.
def convert_and_apply_formula_translation(formula: Formula, translation: PropFormulaTranslation) -> Formula:
    return apply_prop_formula_translation(
        convert_to_prop_formula(formula),
        translation,
    )


@collector.ref('alg:fol_propositional_proof_tree_translation')
def apply_prop_proof_tree_translation(tree: ProofTree, translation: PropFormulaTranslation) -> ProofTree:
    match tree:
        case AssumptionTree():
            return assume(
                convert_and_apply_formula_translation(tree.conclusion, translation),
                tree.marker,
            )

        case RuleApplicationTree():
            return apply(
                tree.rule,
                *(
                    premise_config(
                        tree=apply_prop_proof_tree_translation(premise.tree, translation),
                        attachments=[
                            MarkedFormula(
                                convert_and_apply_formula_translation(attachment.formula, translation),
                                attachment.marker,
                            ) if attachment else None
                            for attachment in premise.attachments
                        ],
                    )
                    for premise in tree.premises
                ),
                instantiation=AtomicLogicSchemaInstantiation(
                    formula_mapping={
                        placeholder: convert_and_apply_formula_translation(formula, translation)
                        for placeholder, formula in tree.instantiation.formula_mapping.items()
                    },
                ),
            )


def translate_prop_proof_tree(tree: ProofTree, mapping: Mapping[PropVariable, Formula]) -> ProofTree:
    return apply_prop_proof_tree_translation(tree, PropFormulaTranslation(mapping))
