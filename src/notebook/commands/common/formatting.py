import hashlib
import io
import pathlib
import shutil
import tempfile
from typing import TYPE_CHECKING, NamedTuple, TextIO

import loguru


if TYPE_CHECKING:
    from types import TracebackType


class FormatterContext(NamedTuple):
    src: TextIO
    dest: TextIO
    logger: loguru.Logger


class FormatterContextManager:
    path: pathlib.Path
    context: FormatterContext | None

    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.context = None

    def __enter__(self) -> FormatterContext:
        logger = loguru.logger.bind(logger=self.path.as_posix())

        file = self.path.open('r')
        buffer = io.StringIO()

        self.context = FormatterContext(file, buffer, logger)
        return self.context

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
     ) -> None:
        if self.context is None:
            return

        src, dest, logger = self.context

        if exc_value is not None:
            src.close()
            return

        src.seek(0)
        dest.seek(0)

        old_hash = hashlib.blake2b(src.read().encode('utf-8'), digest_size=4).hexdigest()
        new_hash = hashlib.blake2b(dest.read().encode('utf-8'), digest_size=4).hexdigest()

        if new_hash == old_hash:
            return

        bak_path = pathlib.Path(tempfile.gettempdir()) / (old_hash + '.bak')
        logger.info(f'Formatting and backing up into {bak_path.as_posix()}.')

        src.seek(0)

        with bak_path.open('w') as bak_file:
            shutil.copyfileobj(src, bak_file)

        src.close()
        dest.seek(0)

        with self.path.open('w', encoding='utf-8') as src_w:
            shutil.copyfileobj(dest, src_w)
            src_w.truncate()
