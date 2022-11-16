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
        arg_list = ', '.join(str(arg) for arg in self.arguments)
        return f'{self.name}({arg_list})'


Term = Variable | FunctionTerm
