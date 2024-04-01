from textwrap import dedent

from .format_matrices import format_tex_matrices


def test_empty_matrix():
    string = dedent(r'''
        \begin{pmatrix}
        \end{pmatrix}
        '''
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_simple_formatted():
    string = dedent(r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1
        \end{pmatrix}
        '''
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_simple_unformatted():
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


def test_formatted_with_space_in_cells():
    string = dedent(r'''
        \begin{pmatrix}[option]
          1     1 & 0     0 \\
          0     0 & 1     1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_formatted_with_option():
    string = dedent(r'''
        \begin{pmatrix}[option]
          1 & 0 \\
          0 & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_formatted_with_multiline_option():
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


def test_misaligned_initial_columns():
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


def test_formatted_with_blank_initial_cell():
    string = dedent(r'''
        \begin{pmatrix}
          1 & 0 \\
            & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_formatted_with_blank_final_cell():
    string = dedent(r'''
        \begin{pmatrix}
          1 &   \\
          0 & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_newline_command_unformatted():
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


def test_empty_column():
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


def test_empty_first_column():
    string = dedent(r'''
        \begin{pmatrix}
          & 0 \\
          & 1
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_empty_final_column():
    string = dedent(r'''
        \begin{pmatrix}
          1 & \\
          0 &
        \end{pmatrix}
        '''[1:]
    )

    formatted = format_tex_matrices(string)
    assert formatted == string


def test_nested_unformatted():
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
