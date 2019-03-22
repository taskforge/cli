"""Provides a Python implementation of a Taskforge Server client."""

import json
from multiprocessing import Pipe, Process

from autobahn.asyncio.websocket import (WebSocketClientFactory,
                                        WebSocketClientProtocol)


class ClientProtocol(WebSocketClientProtocol):
    """Sends a single message to a server"""

    def onOpen(self):  # pylint: disable=invalid-name
        """Send the message to the server on open."""
        message = self.factory.pipe.recv()
        serialized = json.dumps(message)
        self.sendMessage(serialized.encode('utf-8'))

    def onMessage(self, payload, _isBinary):  # pylint: disable=invalid-name
        """Get the server response."""
        response = json.loads(payload.decode('utf-8'))
        self.factory.pipe.send(response)


class ClientFactory(WebSocketClientFactory):
    """A client protocol factory."""

    protocol = ClientProtocol

    def __init__(self, *args, **kwargs):
        self.pipe = kwargs.pop('pipe')
        self.secret = kwargs.pop('secret', None)
        super().__init__(*args, **kwargs)


class Client:
    """
    Manages the a persistent connection to a server.

    For sending a single message use send_message instead.
    """

    def __init__(self, addr):
        parent_pipe, child_pipe = Pipe()
        self.addr = addr
        if not self.addr.endswith('.sock'):
            split = self.addr.split(':')
            self.host = split[0]
            self.port = split[1]
        self.pipe = parent_pipe
        self.factory = ClientFactory(pipe=child_pipe)
        self.loop = None
        self.proc = None

    def __run_client_connection(self):
        import asyncio

        loop = asyncio.get_event_loop()
        if self.addr.endswith('.sock'):
            coro = loop.create_unix_connection(self.factory, path=self.addr)
        else:
            coro = loop.create_connection(self.factory, '127.0.0.1', 9000)

        try:
            loop.run_until_complete(coro)
            loop.run_forever()
        except Exception as ex:
            raise ex
        finally:
            loop.close()

    def start(self):
        """Start the client connection."""
        self.proc = Process(target=self.__run_client_connection)
        self.proc.start()

    def stop(self):
        """Stop the client connection."""
        if self.loop is not None:
            self.loop.close()

        if self.proc is not None:
            self.proc.terminate()
            self.proc = None

    def send_message(self, message):
        """Send message to server."""
        if self.proc is None:
            self.start()
        self.pipe.send(message)

    def recv_message(self):
        """Get the latest message from the server."""
        if self.proc is None:
            self.start()
        recvd = self.pipe.recv()
        self.stop()
        return recvd
