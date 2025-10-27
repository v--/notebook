from collections.abc import Collection
from dataclasses import dataclass

from ....parsing.identifiers import LatinIdentifier, new_latin_identifier


@dataclass(frozen=True)
class Marker:
    identifier: LatinIdentifier

    def __str__(self) -> str:
        return str(self.identifier)


def new_marker(context: Collection[Marker]) -> Marker:
    return Marker(new_latin_identifier({var.identifier for var in context}))
