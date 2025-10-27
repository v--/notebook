from textwrap import dedent

from .format_matrices import format_tex_matrices


def test_empty_matrix() -> None:
    string = dedent(r'''
        \begin{pmatrix}
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_simple_formatted() -> None:
    string = dedent(r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_simple_unformatted() -> None:
    string = dedent(r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == dedent(r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1
        \end{pmatrix}
        '''[1:]
    )


def test_formatted_with_space_in_cells() -> None:
    string = dedent(r'''
        \begin{pmatrix}[option]
          1     1 & 0     0 \\
          0     0 & 1     1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_formatted_with_option() -> None:
    string = dedent(r'''
        \begin{pmatrix}[option]
          1 & 0 \\
          0 & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_formatted_with_multiline_option() -> None:
    string = dedent(r'''
        \begin{pmatrix}
          [
            option
          ]
          1 & 0 \\
          0 & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_misaligned_initial_columns() -> None:
    string = dedent(r'''
        \begin{pmatrix}
        1 & 0 \\
            0 & 1 \\
                1 & 0
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == dedent(r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1 \\
          1 & 0
        \end{pmatrix}
        '''[1:]
    )


def test_formatted_with_blank_initial_cell() -> None:
    string = dedent(r'''
        \begin{pmatrix}
          1 & 0 \\
            & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_formatted_with_blank_final_cell() -> None:
    string = dedent(r'''
        \begin{pmatrix}
          1 &   \\
          0 & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_newline_command_unformatted() -> None:
    string = dedent(r'''
        \begin{pmatrix}
          1 & 0    \\
          0 & 1   \\
          0 & 0
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == dedent(r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1 \\
          0 & 0
        \end{pmatrix}
        '''[1:]
    )


def test_empty_column() -> None:
    string = dedent(r'''
        \begin{pmatrix}
          1 &  & 0 \\
          0 &  & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == dedent(r'''
        \begin{pmatrix}
          1 && 0 \\
          0 && 1
        \end{pmatrix}
        '''[1:]
    )


def test_empty_first_column() -> None:
    string = dedent(r'''
        \begin{pmatrix}
          & 0 \\
          & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_empty_final_column() -> None:
    string = dedent(r'''
        \begin{pmatrix}
          1 & \\
          0 &
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_nested_unformatted() -> None:
    string = dedent(r'''
        \begin{equation}
          \begin{aligned}
            1  & 0 \\
            0 & 1
          \end{aligned}
        \end{equation}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == dedent(r'''
        \begin{equation}
          \begin{aligned}
            1 & 0 \\
            0 & 1
          \end{aligned}
        \end{equation}
        '''[1:]
    )
