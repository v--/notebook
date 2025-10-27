import re


class UrlTemplate:
    secure_default: bool
    template: str
    regex_pattern: re.Pattern[str]

    def __init__(self, template: str, pattern_string: str | None = None, *, secure_default: bool = True) -> None:
        self.secure_default = secure_default
        self.template = template

        if pattern_string is None:
            self.regex_pattern = re.compile(
                'https?://' +
                re.sub(
                    r'\\{(\w+)\\}',
                    r'(?P<\1>.+)',
                    re.escape(template)
                )
            )
        else:
            self.regex_pattern = re.compile(pattern_string)

    def create(self, **kwargs: str) -> str:
        return ('https://' if self.secure_default else 'http://') + self.template.format(**kwargs)

    def extract(self, url: str) -> dict[str, str] | None:
        if match := re.match(self.regex_pattern, url):
            return match.groupdict()

        return None
