"""
Silver layer CLI commands.
"""

import click

from resin.cli.options import suffix_option
from resin.commands.silver import init


@click.group()
def silver():
    """Silver layer commands."""
    pass


@silver.command(name="init")
@suffix_option
def init_cmd(db: str | None) -> None:
    """Create silver layer tables."""
    for message in init(db):
        click.echo(message)
