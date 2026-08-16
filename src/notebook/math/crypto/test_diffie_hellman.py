from notebook.math.rings.modular import Z5

from .diffie_hellman import KeyExchangeUser, exchange_keys


def test_key_exchange() -> None:
    gen = Z5(3)
    a = KeyExchangeUser(gen, secret_key=Z5(1))
    b = KeyExchangeUser(gen, secret_key=Z5(2))

    key_ab = exchange_keys(a, b)
    key_ba = exchange_keys(b, a)

    assert key_ab == key_ba
