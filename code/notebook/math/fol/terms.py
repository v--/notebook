from typing import NamedTuple


class Variable(NamedTuple):
    name: str

    def __str__(self) -> str:
        return self.name


class FunctionTerm(NamedTuple):
    name: str
    arguments: 'list[Term]'

    def __str__(self) -> str:
        args = ', '.join(str(arg) for arg in self.arguments)
        return f'{self.name}({args})' if len(args) > 0 else self.name


Term = Variable | FunctionTerm
