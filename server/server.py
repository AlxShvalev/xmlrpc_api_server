from typing import Dict
from uuid import UUID
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

from server.services import server_service
from settings import settings


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)


server = SimpleXMLRPCServer(
    (settings.SERVER_HOST, settings.SERVER_PORT),
    requestHandler=RequestHandler
)


class ServerMethods:
    """Class for routing XML-RPC server."""

    def auth(self, username, password):
        """Request for user authorization.
        If authorization success, create session for user and return session id.
        """
        user = server_service.get_user(username, password)
        return server_service.create_session(user)

    def get_pub_keys(self) -> Dict[str, int]:
        """Request for getint server public keys."""
        return server_service.get_pub_keys()

    def partial_keys_exchange(self, session_id: UUID, client_key: int) -> int:
        """Receive client partial key and return server partial key."""
        return server_service.partial_keys_exchange(session_id, client_key)

    def get_challenge(self, session_id: UUID) -> str:
        """Request for generation challenge."""
        return server_service.get_challenge(session_id)

    def get_data(
            self,
            session_id: UUID,
            data_key: str,
            challenge_signature: str
    ) -> str:
        """Request for getting data from db."""
        return server_service.get_data(
            session_id,
            data_key,
            challenge_signature
        )

    def shutdown(self):
        server.shutdown()


server.register_introspection_functions()
server.register_instance(ServerMethods())
