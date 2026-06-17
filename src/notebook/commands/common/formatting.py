import hashlib
import io
import logging
import pathlib
import shutil
import tempfile
from typing import NamedTuple, TextIO
lazy from types import TracebackType


logger = logging.getLogger(__name__)


class FormatterContext(NamedTuple):
    src: TextIO
    dest: TextIO


class FormatterContextManager:
    path: pathlib.Path
    context: FormatterContext | None

    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.context = None

    def __enter__(self) -> FormatterContext:
        file = self.path.open('r')
        buffer = io.StringIO()

        self.context = FormatterContext(file, buffer)
        return self.context

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
     ) -> None:
        if self.context is None:
            return

        src, dest = self.context

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
        logger.info(f'Formatting and backing up {self.path} into {bak_path}.')

        src.seek(0)

        with bak_path.open('w') as bak_file:
            shutil.copyfileobj(src, bak_file)

        src.close()
        dest.seek(0)

        with self.path.open('w', encoding='utf-8') as src_w:
            shutil.copyfileobj(dest, src_w)
            src_w.truncate()
