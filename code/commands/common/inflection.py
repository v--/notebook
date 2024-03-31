def pluralize(word: str, count: int):
    if count == 1:
        return word

    return word + 's'


def prefix_cardinal(word: str, count: int):
    return f'{count} {pluralize(word, count)}'
