from collections.abc import Collection, Iterable, Sequence

from ....parsing.parser import Parser
from ..phrases import Phrase
from .parser_context import PhraseContext
from .tokenizer import tokenize_text
from .tokens import TextToken


class TextParser(Parser[TextToken]):
    def iter_phrases(self, stop_words: Collection[str]) -> Iterable[Phrase]:
        if self.peek() is None:
            return

        phrase_context = PhraseContext(self)

        while head := self.peek():
            match head.kind:
                case 'WORD':
                    if head.value.lower() in stop_words:
                        if phrase := phrase_context.try_extract_phrase():
                            yield phrase

                        self.advance()

                        if self.peek():
                            phrase_context.reset()
                    else:
                        self.advance()

                case 'WHITESPACE':
                    self.advance()

                case _:
                    if phrase := phrase_context.try_extract_phrase():
                        yield phrase

                    self.advance()

                    if self.peek():
                        phrase_context.reset()

        if phrase := phrase_context.try_extract_phrase():
            yield phrase



def extract_phrases(source: str, stop_words: Collection[str]) -> Sequence[Phrase]:
    tokens = tokenize_text(source)

    with TextParser(source, tokens) as parser:
        return list(parser.iter_phrases(stop_words))
