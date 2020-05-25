"""Configuration class definition."""

import os
from typing import Any, Dict, Optional
from getpass import getpass

import toml
import appdirs

USER_CONFIG = os.path.join(appdirs.user_config_dir(), "taskforge", "config.toml")
CONFIG_FILES = [
    "/etc/taskforge/config.toml",
    os.path.join(os.getenv("TASKFORGE_CONFIG_DIR", ""), "config.toml"),
    USER_CONFIG,
    "taskforge.toml",
]


def find_config_file(path=None):
    paths = CONFIG_FILES
    if path is not None:
        paths = [path]

    for filename in paths:
        if os.path.isfile(filename):
            return filename

    return None


def default_server_config() -> Dict[str, Any]:
    """Return the default configuration for a server."""
    return {
        # TODO: change
        "hostname": "http://localhost:8000",
    }


class Config:
    """Configuration object for Taskforge CLI and taskforged."""

    def __init__(
        self,
        general: Dict[str, Any] = None,
        server: Dict[str, Any] = None,
        creds: Dict[str, Any] = None,
    ):
        self.general = general if general is not None else dict()
        self.server = server if server is not None else default_server_config()
        self.creds = creds if creds is not None else dict()
        self.path: str = USER_CONFIG
        self.cred_file: Optional[str] = self.general.get("cred_file", None)

    def set_token(self, access_token: str, refresh_token: str) -> None:
        """Set the access and refresh token stored in the creds file."""
        self.creds["tokens"] = {
            "access": access_token,
            "refresh": refresh_token,
        }

    def get_credentials(self, username: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve the stored credentials

        The user will be prompted to input if none are available.
        """
        if not self.cred_file:
            self.cred_file = os.path.join(os.path.dirname(self.path), "creds.toml",)

        if "user" not in self.creds:
            self.load_creds()

        if (
            "user" in self.creds
            and "username" in self.creds["user"]
            and "password" in self.creds["user"]
        ):
            return self.creds

        username = username if username else input("Username: ")
        username.strip()
        password = getpass("Password: ")
        password.strip()
        self.creds = dict({"user": {"username": username, "password": password}})
        return self.creds

    def save(self, path: str = None) -> None:
        """Save the config and creds files."""
        with open(self.path, "w") as cfg_file:
            combined = {
                "general": self.general,
                "server": self.server,
            }
            toml.dump(combined, cfg_file)

        assert self.cred_file is not None
        with open(self.cred_file, "w") as creds_file:
            toml.dump(self.creds, creds_file)

    @staticmethod
    def load(path: str = None) -> "Config":
        """Load the config file from path or from the default config file paths."""
        cfg = Config()
        filename = find_config_file()
        if filename is not None:
            cred_file = os.path.join(os.path.dirname(filename), "creds.toml")
            with open(filename) as config_file:
                user_cfg = toml.load(config_file)
                cfg.general.update(user_cfg.get("general", {}))
                cfg.server.update(user_cfg.get("server", {}))
                cfg.path = filename
                cfg.cred_file = cred_file
                cfg.load_creds()

        if filename is None:
            config_dir = os.path.dirname(USER_CONFIG)
            if not os.path.isdir(config_dir):
                os.makedirs(config_dir)

            with open(USER_CONFIG, "w") as cfg_file:
                cfg_file.write(cfg.toml())

        return cfg

    def load_creds(self) -> None:
        """
        Load the creds file.

        This is derived from self.path if not explicitly set.
        """
        if self.cred_file is not None and os.path.isfile(self.cred_file):
            with open(self.cred_file) as cred_file:
                self.creds = toml.load(cred_file)
        else:
            self.creds = dict()

    def toml(self) -> str:
        """Return a toml string of this config."""
        return toml.dumps(
            {key: val for key, val in self.__dict__.items() if key[0] != "_"}
        )
