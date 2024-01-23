from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Variable:
    name: str

    def __str__(self):
        return self.name


@dataclass
class FunctionTerm:
    name: str
    arguments: list[Term]

    def __str__(self):
        args = ', '.join(str(arg) for arg in self.arguments)
        return f'{self.name}({args})' if len(args) > 0 else self.name


Term = Variable | FunctionTerm
