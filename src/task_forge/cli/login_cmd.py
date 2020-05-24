"""
Usage: task login [options]

Login to the Taskforge server

Options:
    -u <username>, --username <username>  Your username on the server.
                                          If not provided you will be prompted.
    -f, --force                           Force a token refresh.
"""

from typing import Any

from task_forge.cli.utils import config, get_client
from task_forge.cli.config import Config


@config
def run(args: Any, cfg: Config) -> None:
    """Run the login command."""
    username = args["--username"]
    creds = cfg.get_credentials(username if username else None)
    if "tokens" in creds and not args["--force"]:
        print("You're already logged in!")
        return
    client = get_client(cfg)
    tokens = client.login(creds["user"]["username"], creds["user"]["password"])
    cfg.set_token(tokens["access"], tokens["refresh"])
