"""
Entry point for running the resin package directly.
Allows running with: python -m resin
"""

import sys

from .commands import fetcher

if __name__ == "__main__":
    suffix = sys.argv[1] if len(sys.argv) > 1 else None
    fetcher.main(suffix)
