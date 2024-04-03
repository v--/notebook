from typing import Literal, TypeVar, overload

from .matrix import Matrix


N = TypeVar('N', int, float, complex)
M = TypeVar('M', int, float, complex)


@overload
def field_of(dtype: type[int]) -> type[float]: ...
@overload
def field_of(dtype: type[float]) -> type[float]: ...
@overload
def field_of(dtype: type[complex]) -> type[complex]: ...
def field_of(dtype: type[N]) -> type:
    if dtype == int:
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


@overload
def convert_dtype(src: Matrix[int], dtype: type[int]) -> Matrix[int]: ...
@overload
def convert_dtype(src: Matrix[int], dtype: type[float]) -> Matrix[float]: ...
@overload
def convert_dtype(src: Matrix[int], dtype: type[complex]) -> Matrix[complex]: ...
@overload
def convert_dtype(src: Matrix[float], dtype: type[float]) -> Matrix[float]: ...
@overload
def convert_dtype(src: Matrix[float], dtype: type[complex]) -> Matrix[complex]: ...
@overload
def convert_dtype(src: Matrix[complex], dtype: type[complex]) -> Matrix[complex]: ...
def convert_dtype(src: Matrix[N], dtype: type[M]) -> Matrix[M]:
    return Matrix([
        [dtype(cell) for cell in row] # type: ignore[arg-type, call-overload]
        for row in src.get_rows()
    ])
