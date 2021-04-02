import logging

import click


class CustomCommand(click.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aliases = dict()

    def get_command(self, ctx, cmd_name):
        aliased = self.aliases.get(cmd_name, cmd_name)
        return self.commands.get(aliased)

    def format_commands(self, ctx, formatter):
        """Extra format methods for multi methods that adds all the commands
        after the options.
        """
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            aliases = [
                alias
                for alias, cmd_name in self.aliases.items()
                if cmd_name == subcommand
            ]
            if aliases:
                subcommand = f"{subcommand}|{'|'.join(aliases)}"

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            if rows:
                with formatter.section("Commands"):
                    formatter.write_dl(rows)

    def command(self, *args, **kwargs):
        def decorator(f):
            aliases = kwargs.pop("aliases", [])
            cmd = super(CustomCommand, self).command(*args, **kwargs)(f)
            for alias in aliases:
                self.aliases[alias] = cmd.name

            return cmd

        return decorator


@click.group(
    cls=CustomCommand,
    no_args_is_help=True,
)
@click.option("-v", "--verbose", is_flag=True)
def cli(verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)
