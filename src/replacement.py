"""Core text replacement functionality."""

from collections.abc import Sequence


def apply_replacements(
    text: str,
    replacements: Sequence[tuple[str, str]],
) -> str:
    """Apply ordered literal string replacements to text.

    Replacements are applied sequentially in the order supplied.

    Args:
        text: Text to transform.
        replacements: Ordered (source, target) replacement pairs.

    Returns:
        The transformed text.

    Raises:
        ValueError: If a replacement source is empty.
    """
    result = text

    for source, target in replacements:
        if not source:
            raise ValueError("replacement source cannot be empty")

        result = result.replace(source, target)

    return result