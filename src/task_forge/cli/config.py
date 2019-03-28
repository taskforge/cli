"""Configuration class definition."""

import os
import sys

import appdirs
import toml

from task_forge.lists import InvalidConfigError
from task_forge.lists.load import get_list

CONFIG_FILES = [
    '/etc/taskforge/config.toml'
    os.path.join(appdirs.user_config_dir(), 'taskforge', 'config.toml'),
    'taskforge.toml',
]


def default_list_config():
    """Return the default list configuration."""
    return {
        'name': 'sqlite',
        'config': {
            'directory': os.path.join(appdirs.user_data_dir(), 'taskforge')
        }
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
        'unix_socket': f'/var/run/user/{os.getuid()}/taskforge.sock',
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

        return cfg

    def load_list(self, override_config=None):
        """Return the loaded list from this config."""
        if self.list_impl is not None:
            return self.list_impl

        list_cfg = self.list if override_config is None else override_config
        try:
            impl = get_list(list_cfg['name'])
            if impl is None:
                print(f'unknown list: {self.list["name"]}')
                sys.exit(1)
        except KeyError:
            print('no list name provided by config: {}',
                  toml.dumps(self.__dict__))
            sys.exit(1)

        try:
            return impl(**list_cfg['config'])
        except InvalidConfigError as invalid_config:
            print(f'Invalid config: {invalid_config}')
            sys.exit(1)
        except TypeError as unknown_key:
            print(f'Invalid config unknown config key: {unknown_key}')
            sys.exit(1)

    def toml(self):
        """Return a toml string of this config."""
        return toml.dumps(
            {key: val
             for key, val in self.__dict__.items() if key[0] != '_'})

    def __getitem__(self, key):
        """Allow retrieval of config values as if Config was a dict."""
        return self.__dict__[key]

    def __setitem__(self, key, value):
        """Allow setting of config values as if Config was a dict."""
        self.__dict__[key] = value
