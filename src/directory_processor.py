"""Directory processing functionality."""

from collections.abc import Sequence
from pathlib import Path

from file_processor import process_file


def process_directory(
    input_directory: Path,
    output_directory: Path,
    replacements: Sequence[tuple[str, str]],
) -> int:
    """Process all .txt files in a directory.

    Args:
        input_directory: Directory containing input text files.
        output_directory: Directory for processed files.
        replacements: Ordered literal replacement pairs.

    Returns:
        Number of files processed.

    Raises:
        NotADirectoryError: If input_directory is not a directory.
        OSError: If the directory cannot be accessed.
    """
    if not input_directory.is_dir():
        raise NotADirectoryError(
            f"input directory does not exist: {input_directory}"
        )

    input_files = sorted(input_directory.glob("*.txt"))

    for input_path in input_files:
        output_path = output_directory / input_path.name
        process_file(input_path, output_path, replacements)

    return len(input_files)