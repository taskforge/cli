"""Decorators and configuration file loading for the CLI."""

import logging
import os
import socket
import subprocess
import sys
from contextlib import closing

import toml

from task_forge.lists import InvalidConfigError
from task_forge.lists.load import get_list

CONFIG_FILES = [
    'taskforge.toml',
    os.path.join(os.getenv('HOME', ''), '.taskforge.d', 'config.toml'),
    '/etc/taskforge/config.toml'
]


def default_config():
    """Return a dict with the default config values."""
    return {
        'general': {},
        'list': {
            'name': 'sqlite',
            'config': {
                'directory': '~/.taskforge.d'
            }
        },
        'server': default_server_config()
    }


def default_server_config():
    """Return the default configuration for a server."""
    if sys.platform == 'win32':
        return {
            'host': 'localhost',
            'port': 8080,
            # 'secret_file': '~/.taskforge.d/server_secret'
        }

    return {
        # By default use a unix socket not a network socket
        'unix_socket': '/var/run/user/{}/taskforge.sock'.format(os.getuid()),
        # Only used with network communication
        # 'secret_file': '~/.taskforge.d/server_secret'
    }


def load_config():
    """Load the config file from the default locations."""
    cfg = {}

    for filename in CONFIG_FILES:
        if os.path.isfile(filename):
            with open(filename) as config_file:
                cfg = toml.load(config_file)

    default = default_config()
    default.update(cfg)
    return default


def config(func):
    """Load config and inject it as the keyword argument cfg."""
    cfg = load_config()

    def wrapper(*args, **kwargs):
        kwargs['cfg'] = cfg
        return func(*args, **kwargs)

    return wrapper


def load_list(cfg):
    """Load the correct List implementation based on the provided config."""
    impl = get_list(cfg['list']['name'])
    if impl is None:
        print('unknown list: {}'.format(cfg['list']['name']))
        sys.exit(1)

    try:
        return impl(**cfg['list']['config'])
    except InvalidConfigError as invalid_config:
        print('Invalid config: {}'.format(invalid_config))
        sys.exit(1)
    except TypeError as unknown_key:
        print('Invalid config unknown config key: {}'.format(unknown_key))
        sys.exit(1)


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
            sock.connect(srv_cfg['unix_socket'])
        else:
            sock.connect((host, port))

        return True
    except ConnectionRefusedError:
        return False
    finally:
        sock.close()


def start_server(cfg):
    """Start the taskforge server as a daemon if necessary."""
    logging.debug('checking if server is running...')
    srv_cfg = cfg.get('server', {})
    if server_is_reachable(srv_cfg):
        logging.debug('server is running.')
        return

    logging.debug('server is not running')
    logging.debug('starting task server...')
    subprocess.Popen(['task', 'server'])
    logging.debug('task server started!')

    logging.debug('waiting for server to start...')
    retries = 1
    while not server_is_reachable(srv_cfg) and retries <= 10:
        logging.debug('retrying, attempt: %d', retries)
        retries += 1

    if retries >= 10:
        logging.debug('retried 10 times, failing to start')
        raise InvalidConfigError('unable to connect to task server')


def inject_list(func):  # noqa: D202
    """Injects a kwarg task_list which contains a configured list object."""

    @config
    def wrapper(*args, **kwargs):
        cfg = kwargs.pop('cfg')
        if cfg['general'].get('disable_server', False):
            kwargs['task_list'] = load_list(cfg)
        else:
            start_server(cfg)
            kwargs['task_list'] = load_list({
                'list': {
                    'name': 'task_server',
                    'config': cfg['server']
                }
            })

        return func(*args, **kwargs)

    return wrapper
