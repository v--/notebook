from typing import Literal, TypeVar, overload


N = TypeVar('N', int, float, complex)
M = TypeVar('M', int, float, complex)
F = TypeVar('F', float, complex)


@overload
def field_of(dtype: type[int]) -> type[float]: ...
@overload
def field_of(dtype: type[float]) -> type[float]: ...
@overload
def field_of(dtype: type[complex]) -> type[complex]: ...
def field_of(dtype: type[N]) -> type:
    if dtype is int:
        return float

    return dtype


@overload
def is_dtype_convertible(a: type[int], b: type[int]) -> Literal[True]: ...
@overload
def is_dtype_convertible(a: type[int], b: type[float]) -> Literal[True]: ...
@overload
def is_dtype_convertible(a: type[int], b: type[complex]) -> Literal[True]: ...
@overload
def is_dtype_convertible(a: type[float], b: type[int]) -> Literal[False]: ...
@overload
def is_dtype_convertible(a: type[float], b: type[float]) -> Literal[True]: ...
@overload
def is_dtype_convertible(a: type[float], b: type[complex]) -> Literal[True]: ...
@overload
def is_dtype_convertible(a: type[complex], b: type[int]) -> Literal[False]: ...
@overload
def is_dtype_convertible(a: type[complex], b: type[float]) -> Literal[False]: ...
@overload
def is_dtype_convertible(a: type[complex], b: type[complex]) -> Literal[True]: ...
def is_dtype_convertible(a: type[N], b: type[M]) -> bool:
    return issubclass(a, b)
