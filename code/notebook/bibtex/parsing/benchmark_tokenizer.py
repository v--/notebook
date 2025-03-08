import pathlib

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from .tokenizer import BibTokenizer


BIB_ROOT = pathlib.Path(__file__).parent.parent.parent.parent.parent / 'bibliography'


@pytest.mark.benchmark(
    group='bib-tokenizer'
)
def test_tokenizer(benchmark: BenchmarkFixture) -> None:
    with open(BIB_ROOT / 'books.bib') as file:
        source = file.read()
        tokenizer = BibTokenizer(source)

    benchmark.pedantic(
        lambda: list(tokenizer.iter_tokens()),
        setup=tokenizer.reset,
        warmup_rounds=5,
        rounds=50
    )
