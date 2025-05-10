from typing import cast, overload


@overload
def typesup[T](value: None) -> None: ...
@overload
def typesup[T](value: T | None) -> T: ...
def typesup[T](value: T | None) -> T:
    return cast('T', value)
