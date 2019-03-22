"""
Usage: task client

Test a taskforge server connection.
"""


def run(_args):
    """Add the client test command to the parser."""
    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory()
    factory.protocol = MyClientProtocol

    addr = get_unix_socket()
    print('addr', addr)
    reactor.connectUNIX(addr, factory)
    reactor.run()
