"""Replacement-file parsing functionality."""

from pathlib import Path


def read_replacements(path: Path) -> list[tuple[str, str]]:
    """Read ordered replacement pairs from a text file.

    Each non-empty, non-comment line must use SOURCE=TARGET syntax.

    Args:
        path: Path to the replacement definition file.

    Returns:
        Ordered replacement pairs.

    Raises:
        ValueError: If a replacement definition is invalid.
        OSError: If the file cannot be read.
    """
    replacements: list[tuple[str, str]] = []

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            raise ValueError(
                f"invalid replacement on line {line_number}: "
                "expected SOURCE=TARGET"
            )

        source, target = line.split("=", 1)

        if not source:
            raise ValueError(
                f"invalid replacement on line {line_number}: "
                "source cannot be empty"
            )

        replacements.append((source, target))

    if not replacements:
        raise ValueError("replacement file contains no replacements")

    return replacements