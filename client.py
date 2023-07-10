from xmlrpc.client import ServerProxy

from dh_algorithm import DHAlgorithm
from settings import settings
from server.services import generate_signature

secret_key_client = 23

data_key = "key"

url = f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/RPC2"

client = ServerProxy(url)
try:
    session_id = client.auth("username", "password")
    print(session_id)
    keys = client.get_keys()
    pub_key1 = keys.get("pub_key1")
    pub_key2 = keys.get("pub_key2")
    server_part_key = keys.get("part_key")
    client_encrypt = DHAlgorithm(pub_key1, pub_key2, secret_key_client)
    client_part_key = client_encrypt.generate_partial_key()
    client.generate_secret(session_id, client_part_key)
    secret = client_encrypt.generate_full_key(server_part_key)
    print(secret)
    challenge = client.get_challenge(session_id)
    print(challenge)
    signature = generate_signature(secret, challenge)
    print(signature)
    data = client.get_data(session_id, data_key, signature)
    print(data)
except Exception as e:
    print(e)
