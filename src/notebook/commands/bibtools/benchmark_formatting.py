import io
import pathlib

import pytest
lazy from pytest_benchmark.fixture import BenchmarkFixture

from notebook.paths import BIB_PATH

from .file import read_entries, write_entries
from .formatting import adjust_entry


@pytest.mark.benchmark(
    group='bib-format',
)
def benchmark_format(benchmark: BenchmarkFixture) -> None:
    with pathlib.Path(BIB_PATH / 'books.bib').open(encoding='utf-8') as file:
        entries = read_entries(file)

    benchmark.pedantic(
        lambda: [adjust_entry(entry, None) for entry in entries],
        warmup_rounds=5,
        rounds=50,
    )


@pytest.mark.benchmark(
    group='bib-write',
)
def benchmark_write(benchmark: BenchmarkFixture) -> None:
    with pathlib.Path(BIB_PATH / 'books.bib').open(encoding='utf-8') as file:
        entries = read_entries(file)

    output = io.StringIO()
    benchmark.pedantic(
        lambda: write_entries(entries, output),
        setup=output.seek(0),
        warmup_rounds=5,
        rounds=50,
    )
