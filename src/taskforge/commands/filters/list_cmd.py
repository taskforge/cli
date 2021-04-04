import click

from taskforge.commands.filters.filters import filters
from taskforge.commands.utils import inject_client


@filters.command()
@inject_client
def list(client):
    """
    List saved filters.
    """
    for filter in client.filters.list():
        click.echo(filter["name"])
