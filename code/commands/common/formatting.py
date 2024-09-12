import hashlib
import io
import pathlib
import shutil
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TextIO

import loguru


@dataclass
class Formatter(ABC):
    logger: 'loguru.Logger'
    path: pathlib.Path

    @abstractmethod
    def format(self, src: TextIO, dest: TextIO) -> None:
        ...

    def process(self) -> bool:
        file = self.path.open('r+')
        old_hash = hashlib.sha1(file.read().encode('utf-8')).hexdigest()
        bak_path = pathlib.Path(tempfile.gettempdir()) / (old_hash + '.bak')

        file.seek(0)

        buffer = io.StringIO()
        self.format(file, buffer)
        buffer.seek(0)

        new_hash = hashlib.sha1(buffer.read().encode('utf-8')).hexdigest()

        if new_hash != old_hash:
            self.logger.info(f'Formatting and backing up into {bak_path}.')

            file.seek(0)
            with bak_path.open('w') as bak_file:
                shutil.copyfileobj(file, bak_file)

            file.seek(0)
            buffer.seek(0)
            shutil.copyfileobj(buffer, file)
            file.truncate()

        file.close()
        return new_hash != old_hash
