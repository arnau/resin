"""
Shared CLI options.
"""

import click

suffix_option = click.option(
    "-s", "--suffix", "db", default=None, help="Database suffix"
)
