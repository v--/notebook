import itertools
from typing import TYPE_CHECKING

from ..exceptions import UnreachableException
from .unicode import atoi_subscripts, is_numeric_subscript_char, itoa_subscripts


if TYPE_CHECKING:
    from collections.abc import Collection


def get_name_without_collision(base_name: str, context: Collection[str] = {}, *, always_add_suffix: bool = False) -> str:
    """Generate a variation of a base name that is not in a given context.

    This function is loosely related to `notebook.parsing.new_latin_identifier`,
    but it is fundamentally different as it works on arbitrary strings without a fixed grammar.
    """
    if base_name not in context and not always_add_suffix:
        return base_name

    numeric_subscript = ''.join(itertools.takewhile(is_numeric_subscript_char, reversed(base_name)))
    subscript_size = len(numeric_subscript)

    index: int = 0

    if subscript_size > 0:
        index = atoi_subscripts(numeric_subscript)

        if base_name[-subscript_size - 1] == '₋':
            index *= -1
            name_base = base_name[:-subscript_size - 1]
        else:
            name_base = base_name[:-subscript_size]
    else:
        name_base = base_name

    for i in itertools.count(start=index + 1):
        candidate = name_base + itoa_subscripts(i)

        if candidate not in context:
            return candidate

    raise UnreachableException
