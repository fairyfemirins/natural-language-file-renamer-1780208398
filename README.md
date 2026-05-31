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

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).

This repository was published under the authenticated namespace (`fairyfemirins`) with a timestamped name (`nlrename-1780210232`) due to GitHub API restrictions in cron mode.
To transfer to `Femirins/nlrename`:
1. Go to: [Repository Settings](https://github.com/fairyfemirins/nlrename-1780210232/settings)
2. Under "Danger Zone", select "Transfer repository".
3. Enter `Femirins/nlrename` as the new owner.