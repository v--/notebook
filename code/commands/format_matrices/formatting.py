from typing import TextIO

from notebook.latex.format_matrices import format_tex_matrices

from ..common.formatting import Formatter


class MatrixFormatter(Formatter):
    def format(self, src: TextIO, dest: TextIO) -> None:
        dest.write(format_tex_matrices(src.read()))
