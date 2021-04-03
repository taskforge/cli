from taskforge.commands.cli import CustomCommand, cli


@cli.group(aliases=["f"], cls=CustomCommand)
def filters():
    """
    Manage and run saved TQL queries.
    """
    pass
