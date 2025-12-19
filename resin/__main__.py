"""
Entry point for running the resin package directly.
Allows running with: python -m resin
"""

from .commands.fetcher import main

if __name__ == "__main__":
    main()
