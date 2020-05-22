"""Decorators and configuration file loading for the CLI."""

import logging
import socket
import subprocess
import sys
import time
from typing import Any, Dict

from task_forge.cli.config import Config
from task_forge.sdk.client import v1


def config(func: Any) -> Any:
    """Load config and inject it as the keyword argument cfg."""
    cfg = Config.load()

    def wrapper(*args, **kwargs):  # type: ignore
        kwargs["cfg"] = cfg
        return func(*args, **kwargs)

    return wrapper


def get_client(cfg: Config):
    """
    Return the API client for the current API version
    """
    return v1.API(cfg.server.hostname)
