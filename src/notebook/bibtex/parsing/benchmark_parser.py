import pathlib

import pytest
lazy from pytest_benchmark.fixture import BenchmarkFixture

from .parser import BibParser
from .tokenizer import tokenize_bibtex


BIB_ROOT = pathlib.Path(__file__).parent.parent.parent.parent.parent / 'bibliography'


@pytest.mark.benchmark(
    group='bib-parser',
)
def benchmark_parser(benchmark: BenchmarkFixture) -> None:
    source = (BIB_ROOT / 'books.bib').read_text(encoding='utf-8')
    tokens = tokenize_bibtex(source)
    parser = BibParser(source, tokens)

    benchmark.pedantic(
        lambda: list(parser.iter_entries()),
        setup=parser.reset,
        warmup_rounds=5,
        rounds=50,
    )
