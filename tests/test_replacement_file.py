"""Tests for replacement-file parsing."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from replacement_file import read_replacements


def test_read_replacements(tmp_path: Path) -> None:
    path = tmp_path / "replacements.txt"

    path.write_text(
        "# replacements\n"
        "\n"
        "foo=bar\n"
        "hello=goodbye=again\n",
        encoding="utf-8",
    )

    assert read_replacements(path) == [
        ("foo", "bar"),
        ("hello", "goodbye=again"),
    ]


def test_invalid_replacement_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "replacements.txt"
    path.write_text("invalid\n", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="expected SOURCE=TARGET",
    ):
        read_replacements(path)


def test_empty_replacement_file_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "replacements.txt"
    path.write_text("# nothing here\n", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="contains no replacements",
    ):
        read_replacements(path)