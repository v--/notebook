from dataclasses import dataclass, field
from typing import Generic, Sequence, TypeVar

from ...exceptions import NotebookCodeError


class ParserError(NotebookCodeError):
    pass


T = TypeVar('T')


@dataclass
class Parser(Generic[T]):
    seq: Sequence[T]
    index: int = field(default=0, init=False)

    def reset(self):
        self.index = 0

    def is_at_end(self):
        return self.index == len(self.seq)

    def advance(self, count: int = 1):
        assert 0 <= self.index + count <= len(self.seq)
        self.index += count

    def peek(self):
        if self.is_at_end():
            raise self.error('Unexpected end of input')

        return self.seq[self.index]

    def peek_multiple(self, count: int):
        return self.seq[self.index: self.index + count]

    def parse(self):
        raise NotImplementedError()

    def assert_exhausted(self):
        if not self.is_at_end():
            raise self.error('Finished parsing but there is still input left')

    # May God forgive me for this function
    def _iter_error_message(self, message: str, precede: int, succeed: int): # noqa: C901
        yield message
        yield '\n'

        min_seq_index = 0
        mid_seq_index = -1
        max_seq_index = -1
        min_str_index = 0

        for i in range(len(self.seq)):
            if '\n' in str(self.seq[i]):
                if i < self.index - precede:
                    min_seq_index = i + 1

                if i >= self.index and mid_seq_index == -1:
                    mid_seq_index = i - 1

                if i >= self.index + succeed and max_seq_index == -1:
                    max_seq_index = i - 1

        if mid_seq_index == -1:
            mid_seq_index = len(self.seq) - 1

        if max_seq_index == -1:
            max_seq_index = len(self.seq) - 1

        for i in range(min_seq_index, mid_seq_index + 1):
            value = str(self.seq[i])
            yield value

            if i < self.index:
                if '\n' in value:
                    min_str_index = len(value[value.rfind('\n') + 1:])
                elif i < self.index:
                    min_str_index += len(value)

        if self.index < len(self.seq):
            marked_value = str(self.seq[self.index])

            if '\n' in marked_value:
                if marked_value.endswith('\n'):
                    yield marked_value[:-1] + '↵'
                else:
                    yield marked_value
        else:
            yield '⌁'

        yield '\n'
        yield ' ' * min_str_index
        yield '↑' * (len(str(self.seq[self.index])) if self.index < len(self.seq) else 1)
        yield '\n'

        for i in range(mid_seq_index + 1, max_seq_index + 1):
            value = str(self.seq[i])

            if i == mid_seq_index + 1 and value.startswith('\n'):
                yield value[1:]
            else:
                yield value

    def get_error_message(self, message: str, precede: int, succeed: int):
        return ''.join(self._iter_error_message(message, precede, succeed))

    def error(self, message: str, precede: int = 5, succeed: int = 5):
        return ParserError(self.get_error_message(message, precede, succeed))
