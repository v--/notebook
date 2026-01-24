from dataclasses import dataclass

from .schemas import TermSchema, VariablePlaceholder


@dataclass(frozen=True)
class TermSchemaSubstitutionSpec:
    src: VariablePlaceholder
    dest: TermSchema

    def __str__(self) -> str:
        return f'{self.src} ↦ {self.dest}'


class EigenSchemaSubstitutionSpec(TermSchemaSubstitutionSpec):
    dest: VariablePlaceholder

    def __str__(self) -> str:
        return f'{self.src} ↦ {self.dest}*'
