from uuid import UUID
from xmlrpc.server import SimpleXMLRPCServer

from server_services import server_service


server = SimpleXMLRPCServer(('localhost', 8080), allow_none=True)


class ServerMethods:
    def auth(self, username, password):
        user = server_service.get_user(username)
        print("auth user =", user)
        if user is None:
            return "User not found."
        if user.password != password:
            return "Password incorrect."
        return server_service.create_session(user)

    def get_partial_key(self, session_id: UUID, pub_keys) -> int:
        return server_service.get_partial_key(session_id, pub_keys)

    def shutdown(self):
        server.shutdown()


server.register_introspection_functions()
server.register_instance(ServerMethods())
