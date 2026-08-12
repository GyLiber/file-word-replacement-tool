# File Word Replacement Tool

A small command-line utility for replacing words in one or more text files
and writing the processed files to an output directory.

This is a GyLiber project created primarily to support modification of
compiler test-case files for similar languages.

## Requirements

- Python 3.10+
- Pytest for development/testing

The application itself has no runtime third-party dependencies.

## Setup

Clone the repository and create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the development dependency:

```bash
python -m pip install pytest
```

## Usage

```bash
python src/main.py \
    -r 'SOURCE=TARGET' \
    -o OUTPUT_DIRECTORY \
    INPUT_FILE [INPUT_FILE ...]
```

Multiple replacements can be supplied:

```bash
python src/main.py \
    -r 'foo=bar' \
    -r 'hello=goodbye' \
    -o output \
    input-one.txt input-two.txt
```

Replacements are literal and are applied sequentially in the order supplied.

Original input files are never modified.

When processing multiple files, each output file uses the original filename.
Input files therefore must not result in duplicate output filenames.

### Processing a Directory

To process every `.txt` file in a directory using the same replacement set:

```bash
python src/main.py \
    -i scanner-test-cases \
    --replacement-file replacements.txt \
    -o project-scanner-test-case

## Testing

Run the automated tests with:

```bash
python -m pytest
```

## Design

See DESIGN.md for the project's design and v1.0.0 success
criteria.

## AI Usage

ChatGPT was used throughout the development of this project, including
documentation, design decisions, implementation, testing guidance, and
development-related problem solving.

This acknowledgement is provided to maintain transparent documentation of
AI involvement in the creation of the software.

## Version

1.0.0