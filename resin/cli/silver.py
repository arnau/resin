"""
Silver layer CLI commands.
"""

import click

from resin.cli.options import suffix_option
from resin.commands.silver import init, load, sql


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


@silver.command(name="load")
@suffix_option
def load_cmd(db: str | None) -> None:
    """Load data into silver tables from bronze."""
    for message in load(db):
        click.echo(message)


@silver.command(name="sql")
@click.argument("entity")
def sql_cmd(entity: str) -> None:
    """Print the SQL for a silver entity's select_all() query."""
    for message in sql(entity):
        click.echo(message)
