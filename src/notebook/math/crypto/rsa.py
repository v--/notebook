import itertools
import math
import random
from dataclasses import dataclass

from notebook.math.arithmetic.gcd import extended_gcd
from notebook.math.arithmetic.primes import are_coprime, is_prime_naive
from notebook.math.crypto.exceptions import DecryptionError, EncryptionError
from notebook.support.coderefs import collector


@dataclass
class RsaKeyPair:
    n: int
    e: int
    d: int


def rsa_generate_prime(min_value: int = 300, max_value: int = 600) -> int:
    """Generates primes specifically for RSA.

    The default min and max values are chosen empirically to prevent flaky tests.
    """
    p = 1

    while not is_prime_naive(p):
        p = random.randint(min_value, max_value)

    return p


@collector.ref('alg:rsa/keys')
def generate_rsa_key_pair() -> RsaKeyPair:
    p = rsa_generate_prime()
    q = rsa_generate_prime()
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 2

    while not are_coprime(e, phi_n):
        e = random.randint(2, phi_n)

    egcd = extended_gcd(e, phi_n)
    return RsaKeyPair(n, e, d=egcd.a)


@collector.ref('alg:rsa/encryption')
def rsa_encrypt(keys: RsaKeyPair, message: bytes) -> bytes:
    """Encrypt a message given an RSA key pair.

    We cautiously choose a chunk size so that the numeric values of all plaintext chunks are bounded by n.
    The numeric values of ciphertext chunks are bounded by n, but may be wider than the chunk size, so we use a wider
    chunk size for ciphertext.
    """
    chunk_size = math.ceil(math.log2(keys.n) / 8) - 1
    result = b''

    if chunk_size == 0:
        raise EncryptionError('Expected chunk size is tool small')

    for chunk in itertools.batched(message, chunk_size, strict=False):
        m = int.from_bytes(chunk)
        encrypted = pow(m, keys.e, mod=keys.n)
        # The numeric value of ciphertext chunks is bounded by n, but may not fit the cautiously chosen chunk_size
        result += encrypted.to_bytes(length=chunk_size + 1)

    return result


@collector.ref('alg:rsa/decryption')
def rsa_decrypt(keys: RsaKeyPair, message: bytes) -> bytes:
    """Decrypt a message given an RSA key pair.

    See the notes about chunk size in the encryption function.
    """
    chunk_size = math.ceil(math.log2(keys.n) / 8) - 1
    result = b''

    if chunk_size == 0:
        raise EncryptionError('Expected chunk size cannot be zero')

    for chunk in itertools.batched(message, chunk_size + 1, strict=False):
        k = int.from_bytes(chunk)

        if k >= keys.n:
            raise DecryptionError(f'Chunk value {k} is too large to decrypt')

        decrypted = pow(k, keys.d, mod=keys.n)
        result += decrypted.to_bytes(length=chunk_size).lstrip(b'\x00')

    return result
