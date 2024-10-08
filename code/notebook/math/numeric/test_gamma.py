import math
import random

import pytest

from ...support.pytest import pytest_parametrize_lists, repeat5
from .gamma import stirling, stirling_mu


@pytest_parametrize_lists(x=repeat5(random.uniform, 0.1, 10))
def test_stirling(x: int) -> None:
    assert stirling(x) == pytest.approx(math.gamma(x), rel=math.exp(1 / (12 * x)))


@pytest_parametrize_lists(x=repeat5(random.uniform, 0.1, 10))
def test_stirling_mu(x: int, mu_terms: int = 100_000) -> None:
    mu = stirling_mu(x, terms=mu_terms)
    assert 0 < mu < 1 / (12 * x)
    assert stirling(x) * math.exp(mu) == pytest.approx(math.gamma(x))
