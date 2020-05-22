"""
Usage: task register

Register as a new user on the Taskforge server
"""

from typing import Any
from task_forge.cli.config import Config
from task_forge.cli.utils import get_client
from task_forge.sdk.types import User


@config
def run(ags: Any, cfg: Config) -> None:
    email = input("Email: ")
    creds = cfg.get_credentials()

    user = User(
        username=creds["user"]["username"],
        password=creds["user"]["password"],
        email=email,
    )
    client = get_client(cfg)
    client.users.create(user)

    tokens = client.login(user.username, user.password)
    cfg.set_token(tokens["access"], tokens["refresh"])
