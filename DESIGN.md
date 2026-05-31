# Design Document: Natural Language File Renamer

## 1. Introduction
### 1.1 Purpose
The **Natural Language File Renamer (nlfr)** is a CLI tool designed to simplify file renaming using natural language expressions. It addresses the pain point of manual or regex-based renaming by allowing users to describe transformations in plain English.

### 1.2 Scope
- **Input**: Natural language expressions (e.g., `"today's date + original name"`) and file paths.
- **Output**: Renamed files with transformations applied.
- **Constraints**: Offline operation, minimal dependencies, cross-platform compatibility.

## 2. Design
### 2.1 Architecture
- **Single-file script**: Self-contained for easy distribution.
- **Modular parser**: Separates expression parsing from filesystem operations.
- **Dry run mode**: Preview changes before applying.

### 2.2 Components
| Component               | Responsibility                                                                 |
|-------------------------|---------------------------------------------------------------------------------|
| `parse_expression()`    | Parse natural language expression and return transformed filename.             |
| `cli()`                 | Handle CLI arguments, iterate over files, and apply renaming.                  |
| Filesystem Sanitization | Replace illegal characters in filenames (e.g., `/`, `:`, `*`).                 |

### 2.3 Expression Parsing
The parser uses **string replacement** and **regex** to transform expressions:
1. Replace placeholders (e.g., `today's date`, `uuid`).
2. Apply case transformations (e.g., `lowercase`, `titlecase`).
3. Sanitize the output for filesystem compatibility.

### 2.4 Error Handling
- **Invalid expressions**: Gracefully degrade (e.g., treat unknown phrases as literal text).
- **Filesystem errors**: Skip problematic files and log errors.
- **Dry run**: Always suggest `--dry-run` for safety.

## 3. Implementation
### 3.1 Dependencies
- `click`: CLI argument parsing.
- `python-dateutil`: Date arithmetic.
- `uuid`: Generate UUIDs.

### 3.2 Code Structure
```python
# Pseudocode
for file in files:
    original_name, original_ext = split_filename(file)
    parent_folder = get_parent_folder_name(file)
    new_name = parse_expression(expression, original_name, original_ext, parent_folder, counter)
    new_name = sanitize_filename(new_name)
    if dry_run:
        print(f"DRY RUN: {file} -> {new_name}")
    else:
        os.rename(file, new_name)
```

## 4. Verification
### 4.1 Test Cases
| Expression                     | Input File       | Expected Output                     |
|--------------------------------|------------------|-------------------------------------|
| `today's date + original name` | file.txt         | 2026-05-31 + file.txt               |
| `lowercase + uuid`             | IMAGE.JPG        | + 3de4dd64-29bd-4145-a86f-ba2c1041836a.jpg |
| `parent folder name + counter` | notes/*.md       | notes + 1.md, notes + 2.md, ...     |

### 4.2 Edge Cases
- **Illegal characters**: Replace `/`, `:`, `*`, etc. with `_`.
- **Empty expressions**: Treat as literal text.
- **Missing files**: Skip and log errors.

## 5. Future Work
- **Custom date formats**: Support `YYYYMMDD`, `MM-DD-YYYY`, etc.
- **Plugins**: Allow user-defined transformations.
- **GUI**: Web or desktop interface for non-CLI users.

## 6. Lessons Learned
- **API Restrictions**: Static project lists are a reliable fallback for autonomous agents.
- **Demand Validation**: Always validate novelty via `web_search` before development.
- **Self-Contained**: Single-file scripts simplify distribution and installation.