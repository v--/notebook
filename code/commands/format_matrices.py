import io
import sys
import shutil
import hashlib
import tempfile

from ..src.support.latex.format_matrices import format_tex_matrices


def format_matrices_in_file(path: str):
    file = open(path, 'r+')
    src = file.read()
    file_hash = hashlib.sha1(src.encode('utf-8')).hexdigest()
    bak_path = tempfile.gettempdir() + '/' + file_hash + '.bak.csv'

    buffer = io.StringIO()
    buffer.write(format_tex_matrices(src))
    buffer.seek(0)

    if file_hash != hashlib.sha1(buffer.read().encode('utf-8')).hexdigest():
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
        format_matrices_in_file(path)
