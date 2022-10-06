from __future__ import annotations

from dataclasses import dataclass, field

from loguru import logger

from .grammar import Grammar, GrammarRule, NonTerminal, Terminal
from .chomsky import is_context_free
from .parse_tree import ParseTree


@dataclass
class EarleyItem:
    rule: GrammarRule
    rule_index: int
    origin_index: int
    step: int

    def __hash__(self) -> int:
        return hash(self.rule) ^ hash(self.rule_index) ^ hash(self.origin_index) ^ hash(self.step)

    def is_at_end(self):
        return self.rule_index == len(self.rule.dest)

    def peek(self):
        assert self.rule_index < len(self.rule.dest)
        return self.rule.dest[self.rule_index]


@dataclass
class EarleyParser:
    string: str
    grammar: Grammar
    items: list[EarleyItem] = field(default_factory=list)
    source_map: dict[EarleyItem, EarleyItem] = field(default_factory=dict)

    def __post_init__(self):
        assert is_context_free(self.grammar), 'Earley parsing requires the grammar to be context-free'
        self.tree = ParseTree(self.grammar.start)

    def _item_to_str_iter(self, item: EarleyItem):
        yield (
            '⋅' * item.origin_index +
            self.string[item.origin_index: item.step] +
            '⋅' * (len(self.string) - item.step)
        )

        yield '   '
        yield str(item.rule.src[0])
        yield '→'

        for i in range(len(item.rule.dest) + 1):
            if i == item.rule_index:
                yield '•'
            else:
                yield str(item.rule.dest[i - 1 if i >= item.rule_index else i])

    def item_to_str(self, item: EarleyItem):
        return f' '.join(self._item_to_str_iter(item))

    def iter_items(self, i: int):
        for item in self.items:
            if item.step == i:
                yield item

    def iter_final_items(self):
        for item in self.items:
            if item.rule.src == [self.grammar.start] and item.is_at_end() and item.origin_index == 0 and item.step == len(self.string):
                yield item

    def add_item(self, by: str, item: EarleyItem, source: EarleyItem | None):
        by_str = by + ':'

        if item not in self.items:
            logger.debug(f'Added by {by_str:15} {self.item_to_str(item)}')

            if source is not None:
                self.source_map[item] = source

            self.items.append(item)

    def init(self):
        for rule in self.grammar.schema.rules:
            if rule.src == [self.grammar.start]:
                self.add_item(
                    'initializer',
                    EarleyItem(rule, 0, 0, 0),
                    None
                )

    def predictor_step(self, item: EarleyItem, step: int):
        for rule in self.grammar.schema.rules:
            if rule.src == [item.peek()]:
                self.add_item(
                    'predictor',
                    EarleyItem(rule, 0, step, step),
                    None
                )

    def completer_step(self, item: EarleyItem, step: int):
        for source in self.iter_items(item.origin_index):
            if not source.is_at_end() and item.rule.src == [source.peek()]:
                self.add_item(
                    'completer',
                    EarleyItem(source.rule, source.rule_index + 1, source.origin_index, step),
                    item
                )

    def scanner_step(self, item: EarleyItem, step: int):
        if item.step >= len(self.string):
            return

        rule_sym = item.peek()

        if isinstance(rule_sym, Terminal) and rule_sym.value == self.string[item.step]:
            self.add_item(
                'scanner',
                EarleyItem(item.rule, item.rule_index + 1, item.origin_index, step + 1),
                item
            )

    def epsilon_step(self, item: EarleyItem, step: int):
        self.add_item(
            'epsilon',
            EarleyItem(item.rule, item.rule_index + 1, item.origin_index, step),
            item
        )

    def build_table(self):
        logger.debug(f'Processing {self.string}')
        self.init()

        for step in range(len(self.string) + 1):
            logger.debug(f'Moving to step {step}')

            for item in self.iter_items(step):  # New items get added during iteration
                if item.is_at_end():
                    self.completer_step(item, step)
                elif item.rule.is_epsilon:
                    self.epsilon_step(item, step)
                elif isinstance(item.peek(), NonTerminal):
                    self.predictor_step(item, step)
                elif isinstance(item.peek(), Terminal):
                    self.scanner_step(item, step)
