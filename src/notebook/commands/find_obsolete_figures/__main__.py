from ..common.logging import configure_loguru
from .command import find_obsolete_figures


configure_loguru(verbose=False)
find_obsolete_figures()
