"""
Usage: task login [options]

Login to the Taskforge server

Options:
    -u <username>, --username <username>  Your username on the server.
                                          If not provided you will be prompted.
"""

from typing import Any
from task_forge.cli.config import Config
from task_forge.cli.utils import get_client, config


@config
def run(args: Any, cfg: Config) -> None:
    username = args["--username"]
    creds = cfg.get_credentials(username if username else None)
    if "tokens" in creds:
        print("You're already logged in!")
        return
    client = get_client(cfg)
    tokens = client.login(creds["user"]["username"], creds["user"]["password"])
    cfg.set_token(tokens["access"], tokens["refresh"])
