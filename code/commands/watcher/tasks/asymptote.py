import pathlib
import shutil

import loguru

from ...common.paths import AUX_PATH, OUTPUT_PATH
from ..runner import TaskRunner
from ..task import WatcherTask


class AsymptoteTask(WatcherTask):
    src_path: pathlib.Path
    out_buffer: int | None = None

    def __init__(self, base_logger: 'loguru.Logger', src_path: pathlib.Path | str) -> None:
        self.src_path = pathlib.Path(src_path)
        self.base_logger = base_logger
        self.sublogger = base_logger.bind(logger=str(self.src_path))

    def __repr__(self) -> str:
        return f'AsymptoteTask({self.src_path!r})'

    @property
    def aux_pdf_path(self) -> pathlib.Path:
        return AUX_PATH / self.src_path.with_suffix('.pdf').name

    @property
    def build_pdf_path(self) -> pathlib.Path:
        return OUTPUT_PATH / self.src_path.with_suffix('.pdf').name

    @property
    def command(self) -> str:
        return f'asy -quiet -render=5 -outformat=pdf -outname={self.aux_pdf_path.with_suffix('')} {self.src_path}'

    async def post_process(self, runner: TaskRunner) -> None:  # noqa: ARG002
        shutil.copyfile(self.aux_pdf_path, self.build_pdf_path)
