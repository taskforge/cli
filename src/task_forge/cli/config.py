"""Configuration class definition."""

import os
import sys
from typing import Any, Dict, Optional, cast

import appdirs
import toml

from task_forge.lists import InvalidConfigError, TaskList
from task_forge.lists.load import get_list

CONFIG_FILES = [
    "/etc/taskforge/config.toml",
    os.path.join(os.getenv("TASKFORGE_CONFIG_DIR", ""), "config.toml"),
    os.path.join(appdirs.user_config_dir(), "taskforge", "config.toml"),
    "taskforge.toml",
]


ConfigDict = Dict[str, Any]


def default_list_config() -> ConfigDict:
    """Return the default list configuration."""
    return {
        "name": "sqlite",
        "config": {"directory": os.path.join(appdirs.user_data_dir(), "taskforge")},
    }


def default_server_config() -> ConfigDict:
    """Return the default configuration for a server."""
    return {
        "host": "localhost",
        "port": 8000,
        # Only used with network communication
        # 'secret_file': '~/.taskforge.d/server_secret'
    }


class Config:
    """Configuration object for Taskforge CLI and taskforged."""

    def __init__(
        self,
        general: ConfigDict = None,
        list: ConfigDict = None,  # pylint: disable=redefined-builtin
        server: ConfigDict = None,
    ):
        self.general = general if general is not None else {}
        self.list = list if list is not None else default_list_config()
        self.server = server if server is not None else default_server_config()
        self.list_impl = None
        self.path: Optional[str] = None

    @staticmethod
    def load(path: str = None) -> "Config":
        """Load the config file from path or from the default config file paths."""
        cfg = Config()

        paths = CONFIG_FILES
        if path is not None:
            paths = [path]

        for filename in paths:
            if os.path.isfile(filename):
                with open(filename) as config_file:
                    user_cfg = toml.load(config_file)
                    cfg.general.update(user_cfg.get("general", {}))
                    cfg.list.update(user_cfg.get("list", {}))
                    cfg.server.update(user_cfg.get("server", {}))
                    cfg.path = filename

        return cfg

    def load_list(self, override_config: ConfigDict = None) -> TaskList:
        """Return the loaded list from this config."""
        if self.list_impl is not None:
            return self.list_impl

        list_cfg = self.list if override_config is None else override_config
        try:
            impl = get_list(list_cfg["name"])
            if impl is None:
                print(f'unknown list: {self.list["name"]}')
                sys.exit(1)
        except KeyError:
            print("no list name provided by config: {}", toml.dumps(self.__dict__))
            sys.exit(1)

        try:
            return cast(TaskList, impl(**list_cfg["config"]))
        except InvalidConfigError as invalid_config:
            print(f"Invalid config: {invalid_config}")
            sys.exit(1)
        except TypeError as unknown_key:
            print(f"Invalid config unknown config key: {unknown_key}")
            sys.exit(1)

    def toml(self) -> str:
        """Return a toml string of this config."""
        return toml.dumps(
            {key: val for key, val in self.__dict__.items() if key[0] != "_"}
        )
