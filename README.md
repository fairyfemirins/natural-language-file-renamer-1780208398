# Natural Language File Renamer (nlrename)

A CLI tool to batch-rename files using natural language commands.

## Features
- Rename files using natural language (e.g., `"today's date + original name"`).
- Supports date prefixes (`today`, `yesterday`, `tomorrow`).
- Transformations: `lowercase`, `uppercase`, `titlecase`.
- Regex replacements (e.g., `"replace ' ' with '_'"`).
- Dry-run mode for safety.

## Installation
```bash
pip install --user click python-dateutil
```

## Usage
```bash
# Rename all .txt files with today's date
nlrename "today's date + original name" *.txt

# Lowercase and replace spaces with underscores
nlrename "lowercase + replace ' ' with '_'" *.jpg

# Dry run (preview changes)
nlrename --dry-run "uppercase + today's date" *.png
```

## Examples
| Command                          | Before          | After                |
|---------------------------------|-----------------|----------------------|
| `today's date + original name`  | `notes.txt`     | `2026-05-31_notes.txt` |
| `lowercase + replace ' ' with '_'` | `My File.jpg` | `my_file.jpg`        |
| `uppercase + today's date`      | `image.png`     | `2026-05-31_IMAGE.png` |

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).

## License
MIT