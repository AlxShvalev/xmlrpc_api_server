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
    print("Session id:", session_id)
    server_keys = client.get_pub_keys()
    print("Server public keys:", server_keys)
    pub_key1 = server_keys.get("pub_key1")
    pub_key2 = server_keys.get("pub_key2")
    client_dh = DHAlgorithm(pub_key1, pub_key2, secret_key_client)
    client_part_key = client_dh.generate_partial_key()
    server_part_key = client.partial_keys_exchange(session_id, client_part_key)
    print("Server partial key:", server_part_key)
    secret = client_dh.generate_full_key(server_part_key)
    print("Full secret:", secret)
    challenge = client.get_challenge(session_id)
    print("Challenge:", challenge)
    signature = generate_signature(secret, challenge)
    print("Challenge signature:", signature)
    data = client.get_data(session_id, data_key, signature)
    print("Data:", data)
except Exception as e:
    print(e)
