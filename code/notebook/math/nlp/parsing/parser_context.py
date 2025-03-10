from ....parsing import ParserContext
from ..phrases import Phrase
from .tokens import TextTokenKind


class PhraseContext(ParserContext[TextTokenKind]):
    def try_extract_phrase(self) -> Phrase | None:
        if self.parser.token_index == self.index_start:
            return None

        self.close_at_previous_token()
        tokens = self.get_context_tokens()
        return Phrase([token.value for token in tokens if token.kind == 'WORD'])
