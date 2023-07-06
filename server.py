from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


# Ограничение доступа определенным путям.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = SimpleXMLRPCServer(('localhost', 8080), requestHandler=RequestHandler)


class ServerMethods:
    def auth(self):
        pass


# Создаем сервер
server.register_introspection_functions()
server.register_instance(ServerMethods())

with server:
    server.serve_forever()
