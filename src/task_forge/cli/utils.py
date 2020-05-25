"""Decorators and configuration file loading for the CLI."""

from typing import Any

from task_forge.cli.config import Config
from task_forge.sdk.client import v1

CONFIG = None


def config(func: Any) -> Any:
    """Load config and inject it as the keyword argument cfg."""

    def wrapper(*args, **kwargs):  # type: ignore
        global CONFIG

        if CONFIG is None:
            CONFIG = Config.load()

        kwargs["cfg"] = CONFIG
        try:
            return func(*args, **kwargs)
        finally:
            CONFIG.save()

    return wrapper


def get_client(cfg: Config) -> v1.API:
    """Return the API client for the current API version."""
    client = v1.API(cfg.server["hostname"])
    client.refresh_hook = cfg.set_token
    if cfg.creds and "tokens" in cfg.creds:
        client.set_token(cfg.creds["tokens"]["access"], cfg.creds["tokens"]["refresh"])

    if cfg.creds and "user" in cfg.creds:
        client.set_credentials(
            cfg.creds["user"]["username"], cfg.creds["user"]["password"]
        )

    return client
