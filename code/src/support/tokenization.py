from dataclasses import dataclass, field


@dataclass
class Tokenizer:
    string: str
    index: int = field(default=0, init=False)

    def reset(self):
        self.index = 0

    def is_at_end(self):
        return self.index == len(self.string)

    def advance(self):
        assert 0 <= self.index < len(self.string)
        self.index += 1

    def peek(self, count: int = 1):
        assert 0 <= self.index < len(self.string)
        return self.string[self.index: self.index + count]

    def tokenize(self):
        raise NotImplementedError()
