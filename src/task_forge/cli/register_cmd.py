"""
Usage: task register

Register as a new user on the Taskforge server
"""

from typing import Any
from task_forge.cli.config import Config
from task_forge.cli.utils import get_client
from task_forge.sdk.types import User


def run(ags: Any) -> None:
    cfg = Config.load()
    email = input("Email: ")
    creds = cfg.get_credentials()

    user = User(username=creds["username"], password=creds["password"], email=email)
    client = get_client(cfg)
    client.users.create(user)

    tokens = client.login(creds["username"], creds["password"])
    cfg.set_token(tokens["access"], tokens["refresh"])
