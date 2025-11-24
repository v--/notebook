import unicodedata


TRANSLATION_TABLE = str.maketrans({
    '\\':  '_',
    '/': '_',
    ':': '_',
    '|': '_',
    '?': '_',
    '"': ''
})


def escape_file_name(string: str) -> str:
    return unicodedata.normalize('NFC', string.translate(TRANSLATION_TABLE))
