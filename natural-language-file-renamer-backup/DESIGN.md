# Design Document: Natural Language File Renamer

## Problem Statement
Users often need to batch-rename files but lack the technical skills to use regex or scripting tools. A natural language interface lowers the barrier to entry.

## Solution
A CLI tool that parses natural language commands (e.g., "rename all .jpg to vacation_*.jpg") and renames files accordingly.

## Architecture
1. **Command Parser**: Uses regex to extract source and target patterns from natural language.
2. **Filename Generator**: Replaces wildcards (`*`) with the original filename or numbered sequences (`#`).
3. **File Renamer**: Uses `os.rename` to apply changes, with a dry-run mode for safety.

## Trade-offs
- **Minimal Dependencies**: No external libraries (e.g., `spaCy` for NLP) to avoid large downloads.
- **Limited NLP**: Only supports simple commands (e.g., "rename all X to Y").

## Future Work
- Add support for more complex commands (e.g., "rename all files older than 1 week").
- Integrate with cloud storage (e.g., Google Drive, Dropbox).

## License
MIT