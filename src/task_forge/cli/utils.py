"""Decorators and configuration file loading for the CLI."""

import logging
import socket
import subprocess
import os
import sys
import time

from task_forge.cli.config import Config


def config(func):
    """Load config and inject it as the keyword argument cfg."""
    cfg = Config.load()

    def wrapper(*args, **kwargs):
        kwargs['cfg'] = cfg
        return func(*args, **kwargs)

    return wrapper


def server_is_reachable(srv_cfg):
    """Return a boolean indicating if the server is reachable or not."""
    if 'unix_socket' in srv_cfg:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    else:
        host = srv_cfg.get('host', 'localhost')
        port = srv_cfg.get('port', 8080)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        if 'unix_socket' in srv_cfg:
            logging.debug('checking for unix socket: %s', srv_cfg['unix_socket'])
            # if not os.path.isfile(srv_cfg['unix_socket']):
            #     logging.debug('unix socket not found: %s', srv_cfg['unix_socket'])
            #     return False
            sock.connect(srv_cfg['unix_socket'])
        else:
            logging.debug('checking for network connection: %s:%d', host, port)
            sock.connect((host, port))

        return True
    except (ConnectionRefusedError, FileNotFoundError):
        logging.debug('server refused connection')
        return False
    finally:
        sock.close()


def start_server(cfg):
    """Start the taskforge server as a daemon if necessary."""
    logging.debug('checking if server is running...')
    if server_is_reachable(cfg.server):
        logging.debug('server is running.')
        return

    logging.debug('server is not running')
    logging.debug('starting task server...')
    argv = ['taskforged']
    if cfg.path is not None:
        argv += ['--config', cfg.path]
    proc = subprocess.Popen(argv)
    logging.debug('task server started with pid: %d', proc.pid)

    logging.debug('waiting for server to start...')
    retries = 1
    while not server_is_reachable(cfg.server) and retries <= 10:
        logging.debug('retrying, attempt: %d', retries)
        retries += 1
        time.sleep(10)

    if retries >= 10:
        logging.debug('retried 10 times, failing to start')
        logging.error('unable to connect to task server')
        sys.exit(1)


def inject_list(func):  # noqa: D202
    """Injects a kwarg task_list which contains a configured list object."""

    @config
    def wrapper(*args, **kwargs):
        cfg = kwargs.pop('cfg')
        if cfg.general.get('disable_server', False):
            kwargs['task_list'] = cfg.load_list()
        else:
            start_server(cfg)
            kwargs['task_list'] = cfg.load_list(override_config={
                'name': 'task_server',
                'config': cfg.server,
            })

        return func(*args, **kwargs)

    return wrapper
