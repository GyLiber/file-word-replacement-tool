"""Tests for the replacement engine."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import pytest

from replacement import apply_replacements


def test_single_replacement() -> None:
    assert apply_replacements("hello world", [("world", "GyLiber")]) == (
        "hello GyLiber"
    )


def test_multiple_replacements() -> None:
    replacements = [
        ("foo", "bar"),
        ("hello", "goodbye"),
    ]

    assert apply_replacements("hello foo", replacements) == "goodbye bar"


def test_replacements_are_ordered() -> None:
    replacements = [
        ("foo", "bar"),
        ("bar", "baz"),
    ]

    assert apply_replacements("foo", replacements) == "baz"


def test_replacement_can_remove_text() -> None:
    assert apply_replacements("hello world", [("world", "")]) == "hello "


def test_empty_source_is_rejected() -> None:
    with pytest.raises(ValueError, match="replacement source cannot be empty"):
        apply_replacements("hello", [("", "world")])