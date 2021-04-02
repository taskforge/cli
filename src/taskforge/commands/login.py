import click
import sys

from taskforge.commands.cli import cli
from taskforge.commands.utils import coro, inject_client, spinner
from taskforge.client.http import ClientException


async def do_login(client, email, password):
    try:
        with spinner("Generating a personal access token"):
            pat = await client.users.login(email, password)
            msg = """\
Your personal access token is:

{pat}

This token must be set as the environment variable TASKFORGE_TOKEN for us with this CLI.
Add this to your shell configuration file to use it:

    export TASKFORGE_TOKEN="{pat}"
""".format(pat=pat)
    except ClientException as exc:
        if exc.status_code == 401:
            click.echo(exc.msg)
            sys.exit(401)

        raise exc

    click.echo(msg)
    click.echo('WARNING!', color='yellow')
    click.echo(
        'This personal access token can be revoked but it gives full permissions to'
        'operate on taskforge as your user. Protect it like a password.'
    )


@cli.command()
@click.option("--email", prompt=True)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
)
@coro
@inject_client
async def login(
    email,
    password,
    client,
):
    """
    Login to taskforge to generate a Personal Access Token.

    Once the token is generated you should set the environment variable TASKFORGE_TOKEN
    to the given token.
    """
    await do_login(client, email, password)
