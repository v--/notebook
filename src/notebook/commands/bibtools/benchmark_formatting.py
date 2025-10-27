import io

import loguru
import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from ...paths import BIB_PATH
from .formatting import adjust_entry, read_entries, write_entries


@pytest.mark.benchmark(
    group='bib-format'
)
def benchmark_format(benchmark: BenchmarkFixture) -> None:
    with open(BIB_PATH / 'books.bib') as file:
        entries = read_entries(file)

    benchmark.pedantic(
        lambda: [adjust_entry(entry, None, loguru.logger) for entry in entries],
        warmup_rounds=5,
        rounds=50
    )


@pytest.mark.benchmark(
    group='bib-write'
)
def benchmark_write(benchmark: BenchmarkFixture) -> None:
    with open(BIB_PATH / 'books.bib') as file:
        entries = read_entries(file)

    output = io.StringIO()
    benchmark.pedantic(
        lambda: write_entries(entries, output),
        setup=output.seek(0),
        warmup_rounds=5,
        rounds=50
    )
