from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TextIO
import os
import hashlib
import pathlib
import io
import shutil
import tempfile

from loguru import logger


@dataclass
class Formatter(ABC):
    path: str | pathlib.Path

    @abstractmethod
    def format(self, src: TextIO, dest: TextIO) -> None:
        ...

    def process(self) -> bool:
        file = open(self.path, 'r+')
        old_hash = hashlib.sha1(file.read().encode('utf-8')).hexdigest()
        bak_path = os.path.join(tempfile.gettempdir(), old_hash + '.bak')

        file.seek(0)

        buffer = io.StringIO()
        self.format(file, buffer)
        buffer.seek(0)

        new_hash = hashlib.sha1(buffer.read().encode('utf-8')).hexdigest()

        if new_hash != old_hash:
            logger.info(f'Formatting {self.path} and backing up into {bak_path}.')

            file.seek(0)
            with open(bak_path, 'w') as bak_file:
                shutil.copyfileobj(file, bak_file)

            file.seek(0)
            buffer.seek(0)
            shutil.copyfileobj(buffer, file)
            file.truncate()

        file.close()
        return new_hash != old_hash
