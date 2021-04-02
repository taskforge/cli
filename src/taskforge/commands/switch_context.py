import click

from taskforge.commands.cli import cli
from taskforge.state import State


@cli.command(aliases=["sc"])
@click.argument("context", nargs=1, required=False)
def switch_context(context):
    """
    Switch the current context.

    This will change what the next task is such that the only tasks considered are of
    the given context. Useful when you're leaving work and coming home, for instance.
    """
    if context:
        State.current_context = context
    else:
        State.current_context = None
    State.save()
