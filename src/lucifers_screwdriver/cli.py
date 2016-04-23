"""
Command line interface.
"""
from argparse import ArgumentParser
from .metadata import load as meta_load


def get_args():
    p = ArgumentParser(
        prog="lucifers-screwdriver"
    )

    p.add_argument(
        "metadata",
        help="Metadata file."
    )

    args = p.parse_args()

    return args



def main():
    args = get_args()

    with open(args.metadata) as meta_filename:
        print(meta_load(meta_filename))
