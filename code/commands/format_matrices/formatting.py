from typing import TextIO

from ..common.formatting import Formatter

from notebook.latex.format_matrices import format_tex_matrices


class MatrixFormatter(Formatter):
    def format(self, src: TextIO, dest: TextIO) -> None:
        dest.write(format_tex_matrices(src.read()))
