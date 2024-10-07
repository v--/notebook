from collections.abc import Sequence


class VerbatimString:
    value: str

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return '{' + self.value + '}'

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VerbatimString):
            return NotImplemented

        return self.value == other.value

    def strip(self) -> 'VerbatimString':
        return self

    lstrip = rstrip = strip

    def isspace(self) -> bool:
        return self.value.isspace()


class CompositeString:
    segments: 'Sequence[BibString]'

    def __init__(self, segments: 'Sequence[BibString]') -> None:
        self.segments = segments

    def __str__(self) -> str:
        return ''.join(map(str, self.segments))

    def __hash__(self) -> int:
        return hash(tuple(self.segments))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CompositeString):
            return NotImplemented

        return self.segments == other.segments

    def strip(self) -> 'CompositeString':
        return self

    lstrip = rstrip = strip

    def isspace(self) -> bool:
        return all(sub.isspace() for sub in self.segments)


BibString = str | VerbatimString | CompositeString


class CompositeStringBuilder:
    segments: list[BibString]
    buffer: str

    def __init__(self) -> None:
        self.reset()

    def append(self, string: str) -> None:
        self.buffer += string

    def reset(self) -> None:
        self.buffer = ''
        self.segments = []

    def flush(self, *, verbatim: bool) -> None:
        if len(self.buffer) > 0:
            self.segments.append(VerbatimString(self.buffer) if verbatim else self.buffer)
            self.buffer = ''

    def is_empty(self) -> bool:
        return len(self.segments) == 0

    def get_value(self) -> BibString:
        match len(self.segments):
            case 0:
                return ''

            case 1:
                return self.segments[0]

            case _:
                return CompositeString(self.segments)
