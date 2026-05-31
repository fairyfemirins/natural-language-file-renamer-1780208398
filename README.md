# Natural Language File Renamer (nlfr)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CLI tool to rename files using **natural language expressions**.

## Problem
Renaming files in bulk is tedious. Existing tools require regex, manual input, or AI APIs. **Natural Language File Renamer (nlfr)** lets you rename files using plain English expressions like:

```bash
nlfr "today's date + original name" file.txt
nlfr "lowercase + uuid" image.JPG
nlfr "parent folder name + counter" *.md
```

## Features
- **Natural language expressions**: Use phrases like `today's date`, `uuid`, `lowercase`, `parent folder name`, etc.
- **Bulk renaming**: Rename multiple files at once.
- **Dry run mode**: Preview changes before applying.
- **Counter support**: Sequential numbering for batches.
- **Cross-platform**: Works on Linux, macOS, and Windows.

## Installation
```bash
pip install click python-dateutil
curl -o /usr/local/bin/nlfr https://raw.githubusercontent.com/femirins/natural-language-file-renamer/main/nlfr.py
chmod +x /usr/local/bin/nlfr
```

## Usage
```bash
# Rename a single file
nlfr "today's date + original name" file.txt

# Rename multiple files with a counter
nlfr "parent folder name + counter" *.md

# Dry run (preview changes)
nlfr --dry-run "lowercase + uuid" image.JPG

# Set custom counter start
nlfr --counter-start 10 "counter + original name" *.txt
```

### Supported Expressions
| Expression            | Example Output               | Description                          |
|-----------------------|------------------------------|--------------------------------------|
| today's date          | 2026-05-31                   | Current date in YYYY-MM-DD format.   |
| yesterday's date      | 2026-05-30                   | Yesterday's date.                    |
| tomorrow's date       | 2026-06-01                   | Tomorrow's date.                     |
| this month            | 2026-05                      | Current month in YYYY-MM format.     |
| last month            | 2026-04                      | Last month.                          |
| next month            | 2026-06                      | Next month.                          |
| original name         | file                         | Original filename (without extension).|
| original extension    | txt                          | Original file extension.             |
| uuid                  | 3de4dd64-29bd-4145-a86f-ba2c1041836a | Random UUID.                        |
| counter               | 1                            | Sequential counter (per batch).      |
| lowercase             | file                         | Convert to lowercase.                |
| uppercase             | FILE                         | Convert to uppercase.                |
| titlecase             | File                         | Convert to title case.               |
| parent folder name    | documents                    | Name of the parent folder.           |
| custom text           | notes_                       | Literal text (e.g., `notes_`).       |

## Technical Architecture
- **Language**: Python 3.6+
- **Dependencies**: `click`, `python-dateutil`, `uuid`
- **Parsing**: Custom natural language parser with regex and string replacement.
- **Filesystem**: Sanitizes filenames to avoid illegal characters.

### Why This Approach?
- **No external APIs**: Works offline, no privacy concerns.
- **Minimal dependencies**: Only `click` and `python-dateutil`.
- **Self-contained**: Single-file script for easy installation.

## Limitations
- **Complex expressions**: Limited to predefined placeholders and transformations.
- **No undo**: Always use `--dry-run` before applying changes.

## License
MIT

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).