"""Provides the Taskforge Server implementation."""

# We have to match the API that Twisted protocol expects. This means we will
# have classes which have methods that do not use self. So, we disable these
# errors in pylint.
# pylint: disable=no-self-use

import asyncio
import json
import logging
import os
import sys

from autobahn.asyncio.websocket import (WebSocketServerFactory,
                                        WebSocketServerProtocol)
from autobahn.websocket.types import ConnectionDeny

from task_forge.ql.ast import AST
from task_forge.ql.parser import Parser
from task_forge.task import Note, Task

# from twisted.internet import reactor
# from twisted.python import log

STATUS_SUCCESS = 'success'
STATUS_FAILURE = 'failure'


def get_unix_socket(unix='taskforge.sock'):
    """Return a unix socket for the current user. Returns None on Windows."""
    if sys.platform == 'win32':
        return None

    return '/var/run/user/{}/{}'.format(os.getuid(), unix)


def invalid_message(message='Payload is required for this method.'):
    """Return an invalid message response."""
    return {'status': STATUS_FAILURE, 'message': message}


def dispatch(task_list, message):
    """Dispatch a server message to the appropriate task_list method."""
    if 'method' not in message:
        return invalid_message()

    if message['method'] == 'ping':
        return {'status': STATUS_SUCCESS, 'payload': {'message': 'pong'}}

    result = None
    if message['method'] == 'query':
        ast = Parser(message['payload'].get('query', '')).parse()
        result = task_list.search(ast)
    elif message['method'] == 'search':
        ast = AST.from_dict(message['payload'])
        result = task_list.search(ast)
    elif message['method'] == 'add_note':
        payload = message.get('payload', None)
        if payload is None:
            return invalid_message()

        note = payload.get('note')
        if note is None:
            return invalid_message()

        task_id = payload.get('task_id')
        if task_id is None:
            return invalid_message()

        task_list.add_note(task_id, Note(**note))
    else:
        method = getattr(task_list, message['method'])
        payload = message.get('payload', None)
        if payload is None:
            result = method()
        elif isinstance(payload, list):
            tasks = [Task.from_dict(x) for x in payload]
            result = method(tasks)
        elif isinstance(payload, dict) and 'title' in payload:
            task = Task.from_dict(payload)
            result = method(task)
        else:
            result = method(**payload)

    response = {'status': STATUS_SUCCESS, 'payload': None}

    if result is None:
        return response

    if isinstance(result, list):
        response['payload'] = [x.to_json() for x in result]
    else:
        response['payload'] = result.to_json()

    return response


class ServerProtocol(WebSocketServerProtocol):
    """Implement the Autobahn protocol."""

    def onConnect(self, request):  # pylint: disable=invalid-name
        """If a secret is provided verify the client secret."""
        logging.info('client connected: %s', request)
        client_secret = request.headers.get('token')
        if self.factory.secret is not None and client_secret != self.factory.secret:
            logging.info('client rejected: Invalid secret provided.')
            raise ConnectionDeny(403, 'Invalid secret provided.')

    def onOpen(self):  # pylint: disable=invalid-name
        """Log the connection."""
        logging.info('client attempting connection')

    def onMessage(self, payload, isBinary):  # pylint: disable=invalid-name
        """Accept the message, send to dispatch, return response."""
        if isBinary:
            logging.debug('binary message received: %d bytes', len(payload))
            logging.info('binary message ignored')
            return

        message = json.loads(payload)
        logging.debug('recieved payload: %s', payload)
        response = dispatch(self.factory.task_list, message)
        self.sendMessage(json.dumps(response).encode('utf-8'), False)

    def onClose(self, wasClean, code, reason):  # pylint: disable=invalid-name
        """Log disconnect."""
        pass


class ServerFactory(WebSocketServerFactory):
    """Wraps websocket server factory providing access to the task list."""

    protocol = ServerProtocol

    def __init__(self, *args, **kwargs):
        self.task_list = kwargs.pop('task_list')
        self.secret = kwargs.pop('secret')
        super().__init__(*args, **kwargs)


class Server:
    """Provides a Pythonic API for running a server."""

    def __init__(self,
                 task_list,
                 unix_socket=None,
                 host='localhost',
                 port=8080,
                 secret=None,
                 secret_file=None):

        self.secret = None
        if secret is not None:
            self.secret = secret
        elif secret_file is not None:
            with open(secret_file) as key:
                self.secret = key.read()

        self.factory = ServerFactory(task_list=task_list, secret=self.secret)
        self.loop = asyncio.get_event_loop()

        self.host = host
        self.port = port
        self.addr = '{}:{}'.format(self.host, self.port)

        if unix_socket is not None:
            self.addr = unix_socket

        if self.addr.endswith('.sock') or unix_socket is not None:
            self.coro = self.loop.create_unix_server(
                self.factory, path=self.addr)
        else:
            self.coro = self.loop.create_server(self.factory, self.host,
                                                self.port)

        self.server = self.loop.run_until_complete(self.coro)

    def run(self):
        """Start the server listening."""
        try:
            logging.info('server listening on: %s', self.addr)
            self.loop.run_forever()
        except Exception as ex:
            raise ex
        finally:
            self.stop()

    def stop(self):
        """Stop the server."""
        logging.info('stopping server')
        self.server.close()
        self.loop.close()
