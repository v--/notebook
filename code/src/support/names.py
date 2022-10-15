import re


def new_var_name(prefix: str, context: set[str]):
    if prefix not in context:
        return prefix

    match = re.match(r'(\D+)([1-9]\d*)', prefix)

    if match is None:
        letters = prefix
        n = 1
    else:
        letters, digits = match.groups()
        n = int(digits) + 1

    while letters + str(n) in context:
        n += 1

    return letters + str(n)
