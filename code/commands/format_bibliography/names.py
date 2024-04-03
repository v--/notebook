# Simplified transliteration based on
# https://www.mid.ru/ru/activity/legislation_documents/reglaments/1441771/
CYR_TO_LAT_TABLE = str.maketrans({
    'a': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': 'a',  # This is supposed to be "ie", but "a" is more appropriate for Bulgarian and "ъ" is rarely used in Russian names
    'ы': 'y',
    'ь': None,
    'э': 'e',
    'ю': 'iu',
    'я': 'ya',  # This is supposed to be "ia", but "ya" is more widely accepted
    # Custom
    'і': 'i'
})


def latinize_cyrillic_name(name: str) -> str:
    return name \
        .lower() \
        .replace('ий', 'iy') \
        .replace('ей', 'еy') \
        .translate(CYR_TO_LAT_TABLE) \
        .title()
