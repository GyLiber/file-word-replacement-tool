"""Tests for file processing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from file_processor import process_file


def test_process_file_writes_replaced_content(tmp_path: Path) -> None:
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    input_path.write_text("foo hello foo", encoding="utf-8")

    process_file(
        input_path,
        output_path,
        [("foo", "bar"), ("hello", "goodbye")],
    )

    assert output_path.read_text(encoding="utf-8") == "bar goodbye bar"


def test_process_file_preserves_input(tmp_path: Path) -> None:
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"

    original = "foo hello foo"
    input_path.write_text(original, encoding="utf-8")

    process_file(input_path, output_path, [("foo", "bar")])

    assert input_path.read_text(encoding="utf-8") == original


def test_process_file_creates_output_directory(tmp_path: Path) -> None:
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output" / "result.txt"

    input_path.write_text("foo", encoding="utf-8")

    process_file(input_path, output_path, [("foo", "bar")])

    assert output_path.read_text(encoding="utf-8") == "bar"