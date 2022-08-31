import io
import sys
import shutil
import hashlib
import tempfile
from typing import Iterable


class Block:
    _payload: list[list[str]]

    def __init__(self):
        self._payload = []

    def add_row(self, row: list[str]):
        assert self.n_rows == 0 or self.n_cols == len(row)
        self._payload.append(row)

    def iter_rows(self) -> Iterable[list[str]]:
        return iter(self._payload)

    def iter_cols(self) -> Iterable[list[str]]:
        return map(list, zip(*self._payload))

    @property
    def n_rows(self) -> int:
        return len(self._payload)

    @property
    def n_cols(self) -> int:
        if self.n_rows == 0:
            return 0

        return len(self._payload[0])

    def _iter_col_widths(self) -> Iterable[int]:
        if self.n_cols == 0:
            return

        cols = list(self.iter_cols())
        first_col_indent = min(len(cell) - len(cell.lstrip()) for cell in cols[0])
        first_col_width = max(len(cell.strip()) for cell in cols[0])
        yield first_col_indent + first_col_width

        if self.n_cols == 1:
            return

        for col in cols[1:-1]:
            yield max(len(cell.strip()) for cell in col)

        yield max(len(cell.removesuffix(r'\\').strip()) for cell in cols[-1])

    def get_col_widths(self) -> list[int]:
        return list(self._iter_col_widths())


def extract_blocks_iter(text: str) -> Iterable[Block]:
    lines = text.split('\n')
    current_block = Block()
    current_block.add_row(lines[0].split('&'))

    for line in lines[1:]:
        row = line.split('&') if len(line) > 0 else []

        if len(row) == current_block.n_cols:
            current_block.add_row(row)
        else:
            yield current_block
            current_block = Block()
            current_block.add_row(row)

    if current_block.n_cols > 0:
        yield current_block


def format_tex_matrices(path: str):
    file = open(path, 'r+')
    src = file.read()
    file_hash = hashlib.sha1(src.encode('utf-8')).hexdigest()
    bak_path = tempfile.gettempdir() + '/' + file_hash + '.bak.csv'
    buffer = io.StringIO()

    for block in extract_blocks_iter(src):
        if block.n_cols == 0:
            buffer.write('\n' * block.n_rows)
            continue

        if block.n_cols == 1:  # Non-matrix
            for row in block.iter_rows():
                buffer.write(row[0].rstrip())
                buffer.write('\n')

            continue

        for i, row in enumerate(block.iter_rows()):
            col_widths = block.get_col_widths()

            if col_widths[0] > 0:
                buffer.write(row[0].rstrip().ljust(col_widths[0]))

                if row[0].endswith(' ') and len(set(row)) > 1:  # If not only indent
                    buffer.write(' ')

            for cell, col_width in zip(row[1:-1], col_widths[1:-1]):
                buffer.write('&')

                if col_width > 0:
                    if cell.startswith(' '):
                        buffer.write(' ')

                    buffer.write(cell.strip().ljust(col_width))

                    if cell.endswith(' '):
                        buffer.write(' ')

            buffer.write('&')

            if col_widths[-1] > 0 and row[-1].startswith(' '):
                buffer.write(' ')

            if row[-1].endswith(r'\\'):
                buffer.write(row[-1].removesuffix(r'\\').strip().ljust(col_widths[-1]))
                buffer.write(r' \\')
            elif col_widths[-1] > 0:
                buffer.write(row[-1].strip())

            if i < block.n_rows:
                buffer.write('\n')

    buffer.seek(0)
    if file_hash == hashlib.sha1(buffer.read().encode('utf-8')).hexdigest():
        print(f'No need to format {path}')
    else:
        print(f'Formatting {path} and backing up into {bak_path}')

        file.seek(0)
        with open(bak_path, 'w') as bak_file:
            shutil.copyfileobj(file, bak_file)

        file.seek(0)
        buffer.seek(0)
        shutil.copyfileobj(buffer, file)
        file.truncate()

    file.close()


if __name__ == '__main__':
    for path in sys.argv[1:]:
        format_tex_matrices(path)
