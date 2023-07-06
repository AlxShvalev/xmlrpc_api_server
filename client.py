import xmlrpc.client


with xmlrpc.client.ServerProxy("http://localhost:8080") as proxy:
    print(proxy.listMethods())
    print(proxy.pow(2, 3))
