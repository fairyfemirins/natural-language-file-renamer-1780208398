# Natural Language File Renamer

A CLI tool to rename files using natural language patterns (e.g., `"today's date + original name"`).

## Features
- Rename files using natural language (e.g., `"today's date + original name"`).
- Support for date patterns (`today's date`, `tomorrow's date`, `yesterday's date`).
- Case transformations (`lowercase`, `uppercase`).
- String replacements (`replace 'old' with 'new'`).
- Dry-run mode to preview changes.

## Installation

### System Python (Debian/Ubuntu)
```bash
sudo apt install python3-click python3-dateutil
pip install --user .
```

### Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install .
```

## Usage

### Basic Usage
```bash
nl-renamer file1.txt file2.txt --pattern "today's date + original name"
```

### Dry Run (Preview Changes)
```bash
nl-renamer file1.txt file2.txt --pattern "lowercase" --dry-run
```

### Examples
| Pattern                          | Original Name       | New Name               |
|---------------------------------|---------------------|------------------------|
| `today's date + original name`  | `file.txt`          | `2026-05-31_file.txt`  |
| `lowercase`                     | `FILE.TXT`          | `file.txt`             |
| `uppercase`                     | `file.txt`          | `FILE.TXT`             |
| `replace 'file' with 'doc'`     | `file.txt`          | `doc.txt`              |

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).

## License
MIT