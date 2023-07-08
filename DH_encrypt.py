class DHEncrypt:
    def __init__(self, pub_key1: int, pub_key2: int, secret_key: int) -> None:
        self.pub_key1 = pub_key1
        self.pub_key2 = pub_key2
        self.secret_key = secret_key
        self.full_key = None

    def generate_partial_key(self) -> int:
        partial_key = self.pub_key1 ** self.secret_key
        return partial_key % self.pub_key2

    def generate_full_key(self, partial_key_client: int) -> int:
        full_key = partial_key_client ** self.secret_key
        full_key = full_key % self.pub_key2
        self.full_key = full_key
        return full_key
