"""
Command line interface for the resin package.
"""

import click

from resin.database.exceptions import DatabaseLockError

from .bronze import bronze
from .silver import silver


@click.group()
def cli():
    """Resin CLI for fetching and managing GTR API data."""
    pass


class ExceptionHandler(click.Group):
    def invoke(self, ctx: click.Context) -> None:
        try:
            super().invoke(ctx)
        except DatabaseLockError as e:
            click.echo(f"Error: {e}", err=True)
            ctx.exit(1)


cli = ExceptionHandler(
    name=cli.name,
    commands=cli.commands,
    help=cli.help,
)


cli.add_command(bronze)
cli.add_command(silver)
