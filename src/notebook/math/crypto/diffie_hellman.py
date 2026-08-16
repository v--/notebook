from dataclasses import dataclass

from notebook.math.rings.modular import BaseIntModulo
from notebook.support.coderefs import collector


@dataclass
class KeyExchangeUser[Zn: BaseIntModulo]:
    generator: Zn
    secret_key: Zn

    @property
    def public_key(self) -> Zn:
        return self.generator ** self.secret_key


@collector.ref('alg:diffie_hellman_key_exchange')
def exchange_keys[Zn: BaseIntModulo](a: KeyExchangeUser[Zn], b: KeyExchangeUser[Zn]) -> Zn:
    return b.public_key ** a.secret_key
