# File Integrity Monitoring System

A beginner-friendly cybersecurity project built with Python that detects changes to files by comparing their current SHA-256 hashes with a trusted baseline.

## Features

- Creates a SHA-256 baseline for files in a folder
- Detects modified files
- Detects deleted files
- Detects newly added files
- Stores the baseline in JSON format
- Uses Python file handling, hashing, functions, and exception handling

## Technologies

- Python 3
- hashlib
- pathlib
- command-line interface (CLI)

## How it works

1. The user selects a folder to monitor.
2. The program calculates a SHA-256 hash for every file.
3. The hashes are saved as the trusted baseline.
4. Later, the program calculates the hashes again.
5. The new hashes are compared with the baseline.
6. A difference indicates that a file was added, modified, or deleted.

## Run

Create the baseline:

```bash
python fim.py baseline sample_data
```

Modify `sample_data/example.txt`, then run:

```bash
python fim.py check sample_data
```

You can also add or delete a file inside `sample_data` and run the check again.



