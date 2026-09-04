import itertools
import math
import random
from dataclasses import dataclass

from notebook.math.arithmetic.divisibility import rem
from notebook.math.arithmetic.gcd import extended_gcd
from notebook.math.arithmetic.primes import are_coprime, is_prime_naive
from notebook.math.crypto.exceptions import DecryptionError
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
    q = p

    while q == p:
        q = rsa_generate_prime()

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 2

    while not are_coprime(e, phi_n):
        e = random.randint(2, phi_n - 1)

    egcd = extended_gcd(e, phi_n)
    return RsaKeyPair(n, e, d=rem(egcd.a, phi_n))


@dataclass
class RsaChunkSize:
    plain: int
    cipher: int


def determine_rsa_chunk_size(keys: RsaKeyPair) -> RsaChunkSize:
    """Determine a chunk size for longer messages.

    We cautiously choose a chunk size so that the numeric values of all plaintext chunks are bounded by n.
    The numeric values of ciphertext chunks are bounded by n, but the chunks may be wider than the plaintext chunks.
    """
    ciphertext_chunk_size = math.ceil(math.log2(keys.n) / 8)

    return RsaChunkSize(
        plain=ciphertext_chunk_size - 1,
        cipher=ciphertext_chunk_size,
    )


@collector.ref('alg:rsa/encryption')
def rsa_encrypt(keys: RsaKeyPair, message: bytes) -> bytes:
    chunk_sizes = determine_rsa_chunk_size(keys)
    result = b''

    for chunk in itertools.batched(message, chunk_sizes.plain, strict=False):
        m = int.from_bytes(chunk)
        encrypted = pow(m, keys.e, mod=keys.n)
        result += encrypted.to_bytes(length=chunk_sizes.cipher)

    return result


@collector.ref('alg:rsa/decryption')
def rsa_decrypt(keys: RsaKeyPair, message: bytes) -> bytes:
    chunk_sizes = determine_rsa_chunk_size(keys)
    result = b''

    for chunk in itertools.batched(message, chunk_sizes.cipher, strict=False):
        k = int.from_bytes(chunk)

        if k >= keys.n:
            raise DecryptionError(f'Chunk value {k} is too large to decrypt')

        decrypted = pow(k, keys.d, mod=keys.n)
        result += decrypted.to_bytes(length=chunk_sizes.plain).lstrip(b'\x00')

    return result
