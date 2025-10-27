import pathlib


ROOT_PATH = pathlib.Path().cwd()


while not (ROOT_PATH / 'notebook.tex').exists():
    ROOT_PATH = ROOT_PATH.parent


FIGURES_PATH = ROOT_PATH / 'figures'
TEXT_PATH = ROOT_PATH / 'text'
AUX_PATH = ROOT_PATH / 'aux'
OUTPUT_PATH = ROOT_PATH / 'output'
BIB_PATH = ROOT_PATH / 'bibliography'
