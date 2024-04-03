import re
from mmap import PROT_READ, mmap

import click
from loguru import logger

from ..common.inflection import prefix_cardinal
from ..common.paths import FIGURES_PATH, TEXT_PATH


def check_is_figure_used(figure_name: str) -> bool:
    pattern = re.compile(b'{output/' + figure_name.encode('utf8') + b'}')

    for src_file_path in TEXT_PATH.iterdir():
        with open(src_file_path, 'r') as file:
            file_contents = mmap(file.fileno(), length=0, prot=PROT_READ)
            match = re.search(pattern, file_contents)

            if match:
                return True

    return False


@click.command()
def find_obsolete_figures() -> None:
    total_count = 0
    obsolete_count = 0

    for figure_file_path in FIGURES_PATH.iterdir():
        figure_name = figure_file_path.stem
        total_count += 1

        if not check_is_figure_used(figure_name):
            obsolete_count += 1
            logger.info(f'The figure {repr(figure_name)} is not used.')

    logger.info(f'Processed {prefix_cardinal("figures", total_count)}; {obsolete_count} of them were obsolete.')
