"""Decorators and configuration file loading for the CLI."""

from typing import Any

from task_forge.cli.config import Config
from task_forge.sdk.client import v1


def config(func: Any) -> Any:
    """Load config and inject it as the keyword argument cfg."""
    cfg = Config.load()

    def wrapper(*args, **kwargs):  # type: ignore
        kwargs["cfg"] = cfg
        try:
            return func(*args, **kwargs)
        finally:
            cfg.save()

    return wrapper


def get_client(cfg: Config) -> v1.API:
    """Return the API client for the current API version."""
    client = v1.API(cfg.server["hostname"])
    if cfg.creds and cfg.creds["tokens"]:
        client.set_token(cfg.creds["tokens"]["access"], cfg.creds["tokens"]["refresh"])
    return client
