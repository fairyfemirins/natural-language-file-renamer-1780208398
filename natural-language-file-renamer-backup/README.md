# Natural Language File Renamer

Rename files using natural language instructions.

## Features
- Convert filenames to lowercase/uppercase.
- Add today's date to filenames.
- Replace substrings in filenames.
- Dry-run mode for previewing changes.

## Installation
```bash
pip install click python-dateutil regex
```

## Usage
```bash
# Lowercase all PDFs
python nlrename.py "all PDFs to lowercase" /path/to/files

# Add today's date to all files
python nlrename.py "add today's date to all files" /path/to/files

# Replace 'draft' with 'final'
python nlrename.py "replace 'draft' with 'final'" /path/to/files

# Dry-run mode (preview changes)
python nlrename.py "all PDFs to lowercase" /path/to/files --dry-run
```

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).

This repository was published under `fairyfemirins/natural-language-file-renamer-1780148765` due to namespace restrictions in cron mode.
To transfer to `femirins/natural-language-file-renamer`:
1. Go to: [Repository Settings](https://github.com/fairyfemirins/natural-language-file-renamer-1780148765/settings)
2. Under "Danger Zone", select "Transfer repository".
3. Enter `femirins/natural-language-file-renamer` as the new owner.