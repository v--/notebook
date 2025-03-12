class StringContainer:
    """Similar to a UserString, but with type comparison and without additional methods."""

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash((type(self), self.value))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, StringContainer):
            return type(self) is type(other) and self.value == other.value

        return False
