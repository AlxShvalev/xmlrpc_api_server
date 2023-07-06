from xmlrpc.server import SimpleXMLRPCServer


server = SimpleXMLRPCServer(('localhost', 8080))


class ServerMethods:
    def auth(self, message):
        return message


server.register_introspection_functions()
server.register_instance(ServerMethods())

with server:
    server.serve_forever()
