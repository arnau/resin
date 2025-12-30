"""
Bronze layer CLI commands.
"""

import click

from resin.cli.options import suffix_option
from resin.commands.bronze import fetch, init


@click.group()
def bronze():
    """Bronze layer commands."""
    pass


@bronze.command(name="fetch")
@suffix_option
def fetch_cmd(db: str | None) -> None:
    """Fetch data from the GTR API into bronze layer."""
    for message in fetch(db):
        click.echo(message)


@bronze.command(name="init")
@suffix_option
def init_cmd(db: str | None) -> None:
    """Create bronze layer tables."""
    for message in init(db):
        click.echo(message)
