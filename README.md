# Natural Language File Renamer

A CLI tool to rename files using natural language expressions.

## Features
- Rename files using natural language (e.g., `"today's date + original name"`).
- Supports dates (e.g., `"next Monday"`, `"last Friday"`).
- Case transformations (uppercase, lowercase, title case).
- Dry-run mode for previewing changes.

## Installation
```bash
pip install --user click python-dateutil
```

## Usage
```bash
# Preview changes
python nlrename.py "today's date + original name" *.txt --dry-run

# Apply changes
python nlrename.py "uppercase + original extension" *.jpg
```

## Examples
| Pattern                     | Original Name       | New Name               |
|-----------------------------|---------------------|------------------------|
| `"today's date + original name"` | `notes.txt`         | `2026-05-31_notes.txt` |
| `"uppercase + original extension"` | `image.jpg`         | `IMAGE.jpg`            |
| `"next Monday + original name"`   | `report.pdf`        | `2026-06-02_report.pdf` |

## Limitations
- Does not support nested directories (use `find -exec` for batch operations).
- Date parsing may fail for ambiguous expressions.

## License
MIT