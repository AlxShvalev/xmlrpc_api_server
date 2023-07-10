from typing import Dict
from uuid import UUID
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

from server.services import server_service
from settings import settings


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_server = ("/RPC2")


server = SimpleXMLRPCServer(
    (settings.SERVER_HOST, settings.SERVER_PORT),
    requestHandler=RequestHandler,
    allow_none=True,
    logRequests=True
)


class ServerMethods:
    def auth(self, username, password):
        user = server_service.get_user(username, password)
        return server_service.create_session(user)

    def get_pub_keys(self) -> Dict[str, int]:
        return server_service.get_pub_keys()

    def partial_keys_exchange(self, session_id: UUID, client_key: int) -> int:
        return server_service.partial_keys_exchange(session_id, client_key)

    def get_challenge(self, session_id: UUID) -> str:
        return server_service.get_challenge(session_id)

    def get_data(
            self,
            session_id: UUID,
            data_key: str,
            challenge_signature: str
    ) -> str:
        return server_service.get_data(
            session_id,
            data_key,
            challenge_signature
        )

    def shutdown(self):
        server.shutdown()


server.register_introspection_functions()
server.register_instance(ServerMethods())
