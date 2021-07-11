"""
Main module for package staticwiki. The script is executed when invoking:
python -m staticwiki <options> [<arguments>]

For help, use:
python -m staticwiki -h | --help
"""

import argparse
import sys

import staticwiki


def init_cli() -> argparse.ArgumentParser:
    """Initialize the argument parser to handle the command line interface."""

    cli: argparse.ArgumentParser = argparse.ArgumentParser(
        usage="%(prog)s <options> [arguments]",
        description=("Generate a static site..."),
    )
    cli.prog = __package__
    cli.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{cli.prog} {staticwiki.__version__}",
    )
    cli.add_argument(
        "-n", "--new", action="store_true", help="create a new staticwiki project"
    )
    cli.add_argument(
        "-b", "--build", action="store_true", help="build a staticwiki project"
    )
    cli.add_argument(
        "-s", "--serve", action="store_true", help="serve a staticwiki project"
    )

    return cli


def main() -> None:
    """Entry point for the package as a Python module (python -m)"""

    cli = init_cli()
    args = cli.parse_args()

    if len(sys.argv) == 1:
        cli.print_help()
        sys.exit(1)

    print(args)

    print("Static Wiki")


if __name__ == "__main__":
    main()
