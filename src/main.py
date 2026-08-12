"""Command-line interface for the File Word Replacement Tool."""

import argparse
from pathlib import Path

from file_processor import process_file


def parse_replacement(value: str) -> tuple[str, str]:
    """Parse a replacement definition in SOURCE=TARGET form."""
    if "=" not in value:
        raise argparse.ArgumentTypeError(
            "replacement must use SOURCE=TARGET syntax"
        )

    source, target = value.split("=", 1)

    if not source:
        raise argparse.ArgumentTypeError(
            "replacement source cannot be empty"
        )

    return source, target


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Replace words in one or more text files and write the "
            "results to an output directory."
        )
    )

    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="input files to process",
    )

    parser.add_argument(
        "-r",
        "--replacement",
        action="append",
        required=True,
        type=parse_replacement,
        metavar="SOURCE=TARGET",
        help="replacement pair; may be specified multiple times",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        required=True,
        type=Path,
        help="directory for processed files",
    )

    return parser


def main() -> int:
    """Run the command-line application."""
    parser = build_parser()
    args = parser.parse_args()

    for input_path in args.files:
        if not input_path.is_file():
            parser.error(f"input file does not exist: {input_path}")

    for input_path in args.files:
        output_path = args.output_dir / input_path.name

        try:
            process_file(
                input_path,
                output_path,
                args.replacement,
            )
        except (OSError, ValueError) as exc:
            parser.error(f"failed to process {input_path}: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())