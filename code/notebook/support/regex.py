import re
from collections import UserString


# This is made specifically for usage with match-case
class RegexEqual(UserString):
    def __eq__(self, pattern: object) -> bool:
        if isinstance(pattern, str | re.Pattern[str]):
            return bool(re.search(pattern, str(self)))

        return NotImplemented
