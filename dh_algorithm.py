from typing import Dict

from settings import settings


class DHAlgorithm:
    def __init__(self, pub_key1: int, pub_key2: int, secret_key: int) -> None:
        self.pub_key1 = pub_key1
        self.pub_key2 = pub_key2
        self.secret_key = secret_key
        self.partial_key = None

    def generate_partial_key(self) -> int:
        if self.partial_key is None:
            partial_key = self.pub_key1 ** self.secret_key
            self.partial_key = partial_key % self.pub_key2
        return self.partial_key

    @property
    def server_keys(self) -> Dict[str, int]:
        return {
            "pub_key1": self.pub_key1,
            "pub_key2": self.pub_key2,
            "part_key": self.partial_key
        }

    def generate_full_key(self, partial_key_client: int) -> int:
        full_key = partial_key_client ** self.secret_key
        full_key = full_key % self.pub_key2
        return full_key


diffie_hellman = DHAlgorithm(
    settings.PUBLIC_KEY1,
    settings.PUBLIC_KEY2,
    settings.DH_SECRET_KEY
)
