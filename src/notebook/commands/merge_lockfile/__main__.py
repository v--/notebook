from ..common.logging import configure_loguru
from .command import merge_lockfile


configure_loguru(verbose=False)
merge_lockfile()
