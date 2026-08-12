"""Command-line interface for the File Word Replacement Tool."""

import argparse
from pathlib import Path

from directory_processor import process_directory
from file_processor import process_file
from replacement_file import read_replacements


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
            "Replace words in files and write the results to an "
            "output directory."
        )
    )

    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="input files to process",
    )

    parser.add_argument(
        "-i",
        "--input-dir",
        type=Path,
        help="directory containing .txt files to process",
    )

    replacement_group = parser.add_mutually_exclusive_group(required=True)

    replacement_group.add_argument(
        "-r",
        "--replacement",
        action="append",
        type=parse_replacement,
        metavar="SOURCE=TARGET",
        help="replacement pair; may be specified multiple times",
    )

    replacement_group.add_argument(
        "--replacement-file",
        type=Path,
        metavar="FILE",
        help="file containing SOURCE=TARGET replacement pairs",
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
    if bool(args.input_dir) == bool(args.files):
            parser.error(
                "specify either input files or --input-dir"
            )

    try:
        if args.replacement_file is not None:
            replacements = read_replacements(args.replacement_file)
        else:
            replacements = args.replacement

        if args.input_dir is not None:
            count = process_directory(
                args.input_dir,
                args.output_dir,
                replacements,
            )
            print(f"Processed {count} file(s).")
            return 0

        if not args.files:
            parser.error("at least one input file is required")

        output_paths: set[Path] = set()

        for input_path in args.files:
            if not input_path.is_file():
                parser.error(
                    f"input file does not exist: {input_path}"
                )

            output_path = args.output_dir / input_path.name

            if output_path in output_paths:
                parser.error(
                    "multiple input files produce the same output: "
                    f"{output_path}"
                )

            output_paths.add(output_path)

        for input_path in args.files:
            output_path = args.output_dir / input_path.name
            process_file(
                input_path,
                output_path,
                replacements,
            )

        print(f"Processed {len(args.files)} file(s).")
        return 0

    except (OSError, ValueError, NotADirectoryError) as exc:
        parser.error(str(exc))

    return 1


if __name__ == "__main__":
    raise SystemExit(main())