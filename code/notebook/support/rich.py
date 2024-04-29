from typing import Any

import rich.console
import rich.tree


console = rich.console.Console()


def rich_to_text(value: Any) -> str:  # noqa: ANN401
    with console.capture() as capture:
        console.print(value)

    return capture.get()


class RichTreeMixin:
    def build_rich_tree(self) -> rich.tree.Tree:
        raise NotImplementedError

    def __str__(self) -> str:
        return rich_to_text(self.build_rich_tree())

