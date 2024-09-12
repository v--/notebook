from ..common.logging import configure_loguru
from .command import watch


configure_loguru(verbose=False)
watch()
