from typing import Dict

from settings import settings


class DHAlgorithm:
    """Class for Diffie-Hellman key exchange algorythm realize."""

    def __init__(self, pub_key1: int, pub_key2: int, secret_key: int) -> None:
        self.pub_key1 = pub_key1
        self.pub_key2 = pub_key2
        self.secret_key = secret_key
        self.partial_key = None

    def generate_partial_key(self) -> int:
        """If server partial key is None, generate it, then return it"""
        if self.partial_key is None:
            partial_key = self.pub_key1 ** self.secret_key
            self.partial_key = partial_key % self.pub_key2
        return self.partial_key

    @property
    def public_keys(self) -> Dict[str, int]:
        """Return server public key."""
        return {
            "pub_key1": self.pub_key1,
            "pub_key2": self.pub_key2,
        }

    def generate_full_key(self, partial_key_client: int) -> int:
        """Generate full secret key by client partial key."""
        full_key = partial_key_client ** self.secret_key
        return full_key % self.pub_key2


dh_server = DHAlgorithm(
    settings.PUBLIC_KEY1,
    settings.PUBLIC_KEY2,
    settings.DH_SECRET_KEY
)
