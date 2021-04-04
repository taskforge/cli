import click

from taskforge.commands.cli import cli
from taskforge.commands.login import do_login
from taskforge.commands.utils import inject_client, spinner


@cli.command()
@click.option("--email", prompt=True)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
)
@click.option(
    "--full-name",
    prompt=True,
    required=False,
)
@inject_client
def register(
    email,
    password,
    full_name,
    client,
):
    """
    Register as a new user with Taskforge.

    Once the token is generated you should set the environment variable TASKFORGE_TOKEN
    to the given token.
    """
    with spinner("Registering your account..."):
        user = {
            "email": email,
            "password": password,
            "full_name": full_name,
        }
        client.users.create(user)

    do_login(client, email, password)
