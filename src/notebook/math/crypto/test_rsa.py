from notebook.math.arithmetic.divisibility import rem
from notebook.math.arithmetic.primes import totient
from notebook.math.crypto.rsa import RsaKeyPair, generate_rsa_key_pair, rsa_decrypt, rsa_encrypt
from notebook.support.pytest import pytest_parametrize_lists, repeat5


def test_rsa_generate_key_pair() -> None:
    keys = generate_rsa_key_pair()
    assert rem(keys.d * keys.e, totient(keys.n)) == 1


@pytest_parametrize_lists(
    keys=repeat5(generate_rsa_key_pair),
)
def test_rsa_encryption(keys: RsaKeyPair) -> None:
    plaintext = b'plaintext'
    print(keys)
    ciphertext = rsa_encrypt(keys, plaintext)
    decrypted = rsa_decrypt(keys, ciphertext)
    assert plaintext == decrypted
