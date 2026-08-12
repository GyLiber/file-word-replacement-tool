"""Tests for directory processing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from directory_processor import process_directory


def test_process_directory_processes_all_text_files(
    tmp_path: Path,
) -> None:
    input_directory = tmp_path / "input"
    output_directory = tmp_path / "output"
    input_directory.mkdir()

    (input_directory / "one.txt").write_text(
        "foo hello",
        encoding="utf-8",
    )
    (input_directory / "two.txt").write_text(
        "hello foo",
        encoding="utf-8",
    )
    (input_directory / "ignored.md").write_text(
        "foo",
        encoding="utf-8",
    )

    count = process_directory(
        input_directory,
        output_directory,
        [("foo", "bar"), ("hello", "goodbye")],
    )

    assert count == 2
    assert (output_directory / "one.txt").read_text(
        encoding="utf-8"
    ) == "bar goodbye"
    assert (output_directory / "two.txt").read_text(
        encoding="utf-8"
    ) == "goodbye bar"
    assert not (output_directory / "ignored.md").exists()


def test_process_directory_preserves_input_files(
    tmp_path: Path,
) -> None:
    input_directory = tmp_path / "input"
    output_directory = tmp_path / "output"
    input_directory.mkdir()

    original = "foo hello"
    input_path = input_directory / "test.txt"
    input_path.write_text(original, encoding="utf-8")

    process_directory(
        input_directory,
        output_directory,
        [("foo", "bar")],
    )

    assert input_path.read_text(encoding="utf-8") == original