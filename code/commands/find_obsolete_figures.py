import pathlib
import re
from mmap import PROT_READ, mmap


BASE_PATH = pathlib.Path('.').resolve()
FIGURES_PATH = BASE_PATH / 'figures'
SRC_PATH = BASE_PATH / 'text'


def check_is_figure_used(figure_name: str):
    pattern = re.compile(b'{output/' + figure_name.encode('utf8') + b'}')

    for src_file_path in SRC_PATH.iterdir():
        with open(src_file_path, 'r') as file:
            file_contents = mmap(file.fileno(), length=0, prot=PROT_READ)
            match = re.search(pattern, file_contents)

            if match:
                return True

    return False


def find_obsolete_figures():
    for figure_file_path in FIGURES_PATH.iterdir():
        figure_name = figure_file_path.stem

        if not check_is_figure_used(figure_name):
            print(f'The figure {repr(figure_name)} is not used')


if __name__ == '__main__':
    find_obsolete_figures()
