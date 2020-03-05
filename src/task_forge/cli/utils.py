"""Decorators and configuration file loading for the CLI."""

import logging
import socket
import subprocess
import sys
import time
from typing import Any, Dict

from task_forge.cli.config import Config


def config(func: Any) -> Any:
    """Load config and inject it as the keyword argument cfg."""
    cfg = Config.load()

    def wrapper(*args, **kwargs):  # type: ignore
        kwargs["cfg"] = cfg
        return func(*args, **kwargs)

    return wrapper


def server_is_reachable(srv_cfg: Dict[str, Any]) -> bool:
    """Return a boolean indicating if the server is reachable or not."""
    host = srv_cfg.get("host", "localhost")
    port = srv_cfg.get("port", 8000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        logging.debug("checking for network connection: %s:%d", host, port)
        sock.connect((host, port))
        return True
    except (ConnectionRefusedError, FileNotFoundError):
        logging.debug("server refused connection")
        return False
    finally:
        sock.close()


def start_server(cfg: Config) -> None:
    """Start the taskforge server as a daemon if necessary."""
    logging.debug("checking if server is running...")
    if server_is_reachable(cfg.server):
        logging.debug("server is running.")
        return

    logging.debug("server is not running")
    logging.debug("starting task server...")
    argv = ["taskforged"]
    if cfg.path is not None:
    proc = subprocess.Popen(argv)
        argv += ["--config-file", cfg.path]
    logging.debug("task server started with pid: %d", proc.pid)

    logging.debug("waiting for server to start...")
    retries = 1
    while not server_is_reachable(cfg.server) and retries <= 10:
        logging.debug("retrying, attempt: %d", retries)
        retries += 1
        time.sleep(10)

    if retries >= 10:
        logging.debug("retried 10 times, failing to start")
        logging.error("unable to connect to task server")
        sys.exit(1)


def inject_list(func: Any) -> Any:  # noqa: D202
    """Injects a kwarg task_list which contains a configured list object."""

    @config
    def wrapper(*args, **kwargs):  # type: ignore
        cfg = kwargs.pop("cfg")
        if cfg.general.get("disable_server", False):
            kwargs["task_list"] = cfg.load_list()
        else:
            start_server(cfg)
            kwargs["task_list"] = cfg.load_list(
                override_config={"name": "taskforged", "config": cfg.server}
            )

        return func(*args, **kwargs)

    return wrapper
