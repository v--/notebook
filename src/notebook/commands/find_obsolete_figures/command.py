import logging
import re
from mmap import PROT_READ, mmap

import click
from rich.logging import RichHandler

from notebook.commands.common.inflection import prefix_cardinal
from notebook.paths import FIGURES_PATH, TEXT_PATH


logger = logging.getLogger(__name__)


def check_is_figure_used(figure_name: str) -> bool:
    pattern = re.compile(b'{output/' + figure_name.encode('utf8') + b'}')

    for src_file_path in TEXT_PATH.iterdir():
        with src_file_path.open() as file:
            file_contents = mmap(file.fileno(), length=0, prot=PROT_READ)
            match = re.search(pattern, file_contents)

            if match:
                return True

    return False


@click.command()
def find_obsolete_figures() -> None:
    logger.setLevel(logging.INFO)
    logger.addHandler(RichHandler())

    total_count = 0
    obsolete_count = 0

    for figure_file_path in FIGURES_PATH.iterdir():
        total_count += 1

        if not check_is_figure_used(figure_file_path.stem):
            obsolete_count += 1
            logger.info(f'Figure {figure_file_path.name!r} is not used.')

    logger.info(f'Processed {prefix_cardinal("figures", total_count)}; {obsolete_count} of them {'was' if obsolete_count == 1 else 'were'} obsolete.')
