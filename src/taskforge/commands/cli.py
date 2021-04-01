from copy import deepcopy

import click


class CustomCommand(click.Group):
    def command(self, *args, **kwargs):
        def decorator(f):
            aliases = kwargs.pop("aliases", [])
            non_alias = super(CustomCommand, self).command(*args, **kwargs)(f)
            for alias in aliases:
                cmd = deepcopy(non_alias)
                cmd.name = alias
                cmd.short_help = f"Alias for '{non_alias.name}'"
                self.add_command(cmd)

            return non_alias

        return decorator


@click.group(cls=CustomCommand)
def cli():
    pass
