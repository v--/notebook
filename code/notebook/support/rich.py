from typing import Any

from rich.console import Console


console = Console()


def rich_to_text(value: Any):
    with console.capture() as capture:
        console.print(value)

    return capture.get()
