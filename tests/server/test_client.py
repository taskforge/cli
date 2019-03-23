# pylint: disable=missing-docstring

from multiprocessing import Process
from unittest.mock import Mock

import pytest

from task_forge.server.client import Client
from task_forge.server.server import Server, get_unix_socket


@pytest.fixture
def server():
    addr = get_unix_socket(unix='taskforge_client_test.sock')
    srv = Server(Mock(return_value={}), unix_socket=addr)
    proc = Process(target=srv.run)
    proc.start()
    yield addr
    srv.stop()
    proc.terminate()


def test_ping(server):  #pylint: disable=redefined-outer-name
    client = Client(server)
    client.send_message({'method': 'ping'})
    response = client.recv_message()
    assert response == {'status': 'success', 'payload': {'message': 'pong'}}

    client.send_message({'method': 'ping'})
    response = client.recv_message()
    assert response == {'status': 'success', 'payload': {'message': 'pong'}}
