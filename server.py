from xmlrpc.server import SimpleXMLRPCServer

from db.services import get_user


server = SimpleXMLRPCServer(('localhost', 8080))


class ServerMethods:
    def auth(self, username, password):
        user = get_user(username)
        if user is None:
            return "User not found."
        if user.password != password:
            return "Password incorrect."
        return user.username, user.password

    def shutdown(self):
        server.shutdown()


server.register_introspection_functions()
server.register_instance(ServerMethods())
