# Natural Language File Renamer

A CLI tool to rename files using natural language instructions.

## Features
- Rename files using natural language (e.g., `"today's date + original name"`).
- Supports dates, case transformations, replacements, prefixes, and suffixes.
- Dry-run mode for previewing changes.

## Examples
```bash
# Add today's date as a prefix
python3 renamer.py my_file.txt -i "today's date + original name"

# Add a prefix
python3 renamer.py my_file.txt -i "add prefix 'backup_'"

# Lowercase and replace spaces with underscores
python3 renamer.py "My File.txt" -i "lowercase and replace spaces with underscores"

# Preview changes without renaming
python3 renamer.py my_file.txt -i "add suffix '_old'" --dry-run
```

## Installation
```bash
pip install -r requirements.txt
```

## Requirements
- Python 3.8+
- `click`
- `python-dateutil`

## License
MIT