"""
Usage: task client

Run a taskforge server
"""


def run(_args):
    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory()
    factory.protocol = MyClientProtocol

    addr = get_unix_socket()
    print('addr', addr)
    reactor.connectUNIX(addr, factory)
    reactor.run()
