from .format_matrices import format_tex_matrices


def test_simple_formatted():
    string = r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1
        \end{pmatrix}
    '''
    formatted = format_tex_matrices(string)
    assert formatted == string


def test_simple_unformatted():
    string = r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1
        \end{pmatrix}
    '''
    formatted = format_tex_matrices(string)
    assert formatted == r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1
        \end{pmatrix}
    '''


def test_formatted_with_arg():
    string = r'''
        \begin{pmatrix}[arg]
          1 & 0 \\
          0 & 1
        \end{pmatrix}
    '''
    formatted = format_tex_matrices(string)
    assert formatted == string


def test_formatted_with_blank_initial_cell():
    string = r'''
        \begin{pmatrix}
          1 & 0 \\
            & 1
        \end{pmatrix}
    '''
    formatted = format_tex_matrices(string)
    assert formatted == string


def test_formatted_with_blank_final_cell():
    string = r'''
        \begin{pmatrix}
          1 &   \\
          0 & 1
        \end{pmatrix}
    '''
    formatted = format_tex_matrices(string)
    assert formatted == string


def test_newline_command_unformatted():
    string = r'''
        \begin{pmatrix}
          1 & 0    \\
          0 & 1   \\
          0 & 0
        \end{pmatrix}
    '''
    formatted = format_tex_matrices(string)
    assert formatted == r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1 \\
          0 & 0
        \end{pmatrix}
    '''


def test_empty_column():
    string = r'''
        \begin{pmatrix}
          1 &  & 0 \\
          0 &  & 1
        \end{pmatrix}
    '''
    formatted = format_tex_matrices(string)
    assert formatted == r'''
        \begin{pmatrix}
          1 && 0 \\
          0 && 1
        \end{pmatrix}
    '''


def test_empty_first_column():
    string = r'''
        \begin{pmatrix}
          & 0 \\
          & 1
        \end{pmatrix}
    '''
    formatted = format_tex_matrices(string)
    assert formatted == string


def test_empty_final_column():
    string = r'''
        \begin{pmatrix}
          1 & \\
          0 &
        \end{pmatrix}
    '''
    formatted = format_tex_matrices(string)
    assert formatted == string


def xtest_nested_unformatted():
    string = r'''
        \begin{equation}
          \begin{aligned}
            1  & 0 \\
            0 & 1
          \end{aligned}
        \end{equation}
    '''
    formatted = format_tex_matrices(string)
    assert formatted == r'''
        \begin{equation}
          \begin{aligned}
            1 & 0 \\
            0 & 1
          \end{aligned}
        \end{equation}
    '''
