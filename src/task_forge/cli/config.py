"""Configuration class definition."""

import os
import sys

from typing import Any, Dict, Optional, cast
from getpass import getpass

import appdirs
import toml

USER_CONFIG = os.path.join(appdirs.user_config_dir(), "taskforge", "config.toml")
CONFIG_FILES = [
    "/etc/taskforge/config.toml",
    os.path.join(os.getenv("TASKFORGE_CONFIG_DIR", ""), "config.toml"),
    USER_CONFIG,
    "taskforge.toml",
]


class ConfigDict(dict):
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self.get(name, None)


def default_server_config() -> ConfigDict:
    """Return the default configuration for a server."""
    return ConfigDict(
        **{
            # TODO: change
            "hostname": "http://localhost:8000",
        }
    )


class Config:
    """Configuration object for Taskforge CLI and taskforged."""

    def __init__(
        self,
        general: ConfigDict = None,
        server: ConfigDict = None,
        creds: ConfigDict = None,
    ):
        self.general = general if general is not None else dict()
        self.server = server if server is not None else default_server_config()
        self.creds = creds if creds is not None else ConfigDict()
        self.path: str = USER_CONFIG
        self.cred_file: Optional[str] = self.general.get("cred_file", None)

    def set_token(self, access_token, refresh_token) -> None:
        self.creds.tokens = {
            "access": access_token,
            "refresh": refresh_token,
        }

    def get_credentials(self, username: Optional[str] = None):
        if not self.cred_file:
            self.cred_file = os.path.join(os.path.dirname(self.path), "creds.toml",)

        if not self.creds.user:
            self.load_creds()

        if (
            self.creds.user
            and "username" in self.creds["user"]
            and "password" in self.creds["user"]
        ):
            return self.creds

        username = username if username else input("Username: ")
        username.strip()
        password = getpass("Password: ")
        password.strip()
        self.creds = ConfigDict({"user": {"username": username, "password": password}})
        return self.creds

    def save(self, path: str = None) -> None:
        with open(self.path, "w") as cfg_file:
            combined = {
                "general": self.general,
                "server": self.server,
            }
            toml.dump(combined, cfg_file)

        with open(self.cred_file, "w") as creds_file:
            toml.dump(self.creds, creds_file)

    @staticmethod
    def load(path: str = None) -> "Config":
        """Load the config file from path or from the default config file paths."""
        cfg = Config()

        paths = CONFIG_FILES
        if path is not None:
            paths = [path]

        loaded = False
        for filename in paths:
            if os.path.isfile(filename):
                cred_file = os.path.join(os.path.dirname(filename), "creds.toml")
                with open(filename) as config_file:
                    user_cfg = toml.load(config_file)
                    cfg.general.update(user_cfg.get("general", {}))
                    cfg.server.update(user_cfg.get("server", {}))
                    cfg.path = filename
                    cfg.cred_file = cred_file
                    cfg.load_creds()
                    loaded = True

        if not loaded:
            config_dir = os.path.dirname(USER_CONFIG)
            if not os.path.isdir(config_dir):
                os.makedirs(config_dir)
            with open(USER_CONFIG, "w") as cfg_file:
                cfg_file.write(cfg.toml())

        return cfg

    def load_creds(self):
        if os.path.isfile(self.cred_file):
            with open(self.cred_file) as cred_file:
                self.creds = ConfigDict(toml.load(cred_file))
        else:
            self.creds = ConfigDict({"user": {}})

    def toml(self) -> str:
        """Return a toml string of this config."""
        return toml.dumps(
            {key: val for key, val in self.__dict__.items() if key[0] != "_"}
        )
