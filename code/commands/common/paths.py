import pathlib


ROOT_DIR = pathlib.Path().resolve()


while not (ROOT_DIR / 'notebook.tex').exists():
    ROOT_DIR = ROOT_DIR.parent


FIGURES_PATH = ROOT_DIR / 'figures'
TEXT_PATH = ROOT_DIR / 'text'
AUX_PATH = ROOT_DIR / 'aux'
