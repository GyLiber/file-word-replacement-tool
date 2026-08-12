"""File processing functionality."""

from pathlib import Path
from collections.abc import Sequence

from replacement import apply_replacements


def process_file(
    input_path: Path,
    output_path: Path,
    replacements: Sequence[tuple[str, str]],
) -> None:
    """Read, transform, and write a file.

    The input file is never modified.

    Args:
        input_path: Path to the source file.
        output_path: Path where the transformed file is written.
        replacements: Ordered literal replacement pairs.

    Raises:
        FileNotFoundError: If the input file does not exist.
        OSError: If the file cannot be read or written.
        ValueError: If a replacement source is empty.
    """
    text = input_path.read_text(encoding="utf-8")
    transformed = apply_replacements(text, replacements)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(transformed, encoding="utf-8")