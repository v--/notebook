import re

from .subscripts import atoi_subscripts, itoa_subscripts


def new_var_name(prefix: str, context: set[str]):
    if prefix not in context:
        return prefix

    match = re.match(r'(?P<symbols>^[^₀-₉]*)(?P<digits>₀|[₁-₉][₀-₉]*)$', prefix)

    if match is None:
        letters = prefix
        n = 0
    else:
        letters = match['symbols']
        n = atoi_subscripts(match['digits']) + 1

    while letters + itoa_subscripts(n) in context:
        n += 1

    return letters + itoa_subscripts(n)
