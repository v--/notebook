from iso639 import Lang


def create_lang_object(language: str) -> Lang:
    if len(language) == 2:
        return Lang(language)

    return Lang(language.title())


def get_language_name(language: str) -> str:
    return create_lang_object(language).name.lower()


normalize_language_name = get_language_name


def get_language_code(language: str) -> str:
    return create_lang_object(language).pt1
