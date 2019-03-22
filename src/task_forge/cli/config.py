"""Configuration class definition."""

import os
import sys
import toml

from task_forge.lists import InvalidConfigError
from task_forge.lists.load import get_list

CONFIG_FILES = [
    'taskforge.toml',
    os.path.join(os.getenv('HOME', ''), '.taskforge.d', 'config.toml'),
    '/etc/taskforge/config.toml'
]


def default_list_config():
    """Return the default list configuration."""
    return {'name': 'sqlite', 'config': {'directory': '~/.taskforge.d'}}


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


class Config:
    """Configuration object for Taskforge CLI and taskforged."""

    def __init__(self, general=None, list=None, server=None):
        self.general = general if general is not None else {}
        self.list = list if list is not None else default_list_config()
        self.server = server if server is not None else default_server_config()
        self.list_impl = None
        self.path = None

    @staticmethod
    def load(path=None):
        """Load the config file from path or from the default config file paths."""
        cfg = Config()

        paths = CONFIG_FILES
        if path is not None:
            paths = [path]

        for filename in paths:
            if os.path.isfile(filename):
                with open(filename) as config_file:
                    user_cfg = toml.load(config_file)
                    cfg.__dict__.update(user_cfg)
                    cfg.path = config_file
                    break

        return cfg

    def load_list(self, override_config=None):
        """Return the loaded list from this config."""
        if self.list_impl is not None:
            return self.list_impl

        list_cfg = self.list if override_config is None else override_config
        try:
            impl = get_list(list_cfg['name'])
            if impl is None:
                print('unknown list: {}'.format(self.list['name']))
                sys.exit(1)
        except KeyError:
            print('no list name provided by config: {}',
                  toml.dumps(self.__dict__))
            sys.exit(1)

        try:
            return impl(**list_cfg['config'])
        except InvalidConfigError as invalid_config:
            print('Invalid config: {}'.format(invalid_config))
            sys.exit(1)
        except TypeError as unknown_key:
            print('Invalid config unknown config key: {}'.format(unknown_key))
            sys.exit(1)

    def toml(self):
        """Return a toml string of this config."""
        return toml.dumps(
            {key: val
             for key, val in self.__dict__.items() if key[0] != '_'})

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
