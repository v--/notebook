import pathlib
from typing import TYPE_CHECKING

import pytest

from .tokenizer import BibTokenizer


if TYPE_CHECKING:
    from pytest_benchmark.fixture import BenchmarkFixture


BIB_ROOT = pathlib.Path(__file__).parent.parent.parent.parent.parent / 'bibliography'


@pytest.mark.benchmark(
    group='bib-tokenizer',
)
def benchmark_tokenizer(benchmark: BenchmarkFixture) -> None:
    source = (BIB_ROOT / 'books.bib').read_text(encoding='utf-8')
    tokenizer = BibTokenizer(source)

    benchmark.pedantic(
        lambda: list(tokenizer.iter_tokens()),
        setup=tokenizer.reset,
        warmup_rounds=5,
        rounds=50,
    )
