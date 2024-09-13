import re
from collections import UserString


class RegexEqual(UserString):
    def __eq__(self, pattern: object) -> bool:
        if isinstance(pattern, str | re.Pattern[str]):
            return bool(re.search(pattern, str(self)))

        return NotImplemented
