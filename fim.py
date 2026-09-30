import hashlib
import json
import os
import sys
from pathlib import Path

BASELINE_FILE = "baseline.json"


def calculate_sha256(file_path):
    """Return the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()


def collect_files(folder):
    """Collect files recursively, excluding the baseline file."""
    folder = Path(folder)
    files = []

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    for path in folder.rglob("*"):
        if path.is_file() and path.name != BASELINE_FILE:
            files.append(path)

    return files


def create_baseline(folder):
    """Create a baseline of SHA-256 hashes for files in a folder."""
    records = {}

    for file_path in collect_files(folder):
        relative_path = str(file_path.relative_to(folder))
        records[relative_path] = calculate_sha256(file_path)

    with open(BASELINE_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)

    print(f"Baseline created for {len(records)} file(s).")


def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        print("No baseline found. Run: python fim.py baseline <folder>")
        sys.exit(1)

    with open(BASELINE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def check_integrity(folder):
    """Compare current hashes with the saved baseline."""
    baseline = load_baseline()
    current = {}

    for file_path in collect_files(folder):
        relative_path = str(file_path.relative_to(folder))
        current[relative_path] = calculate_sha256(file_path)

    modified = []
    deleted = []
    added = []

    for path, old_hash in baseline.items():
        if path not in current:
            deleted.append(path)
        elif current[path] != old_hash:
            modified.append(path)

    for path in current:
        if path not in baseline:
            added.append(path)

    print("\nIntegrity Check")
    print("----------------")

    if modified:
        print("\nModified files:")
        for path in modified:
            print(f"  [MODIFIED] {path}")

    if deleted:
        print("\nDeleted files:")
        for path in deleted:
            print(f"  [DELETED]  {path}")

    if added:
        print("\nNew files:")
        for path in added:
            print(f"  [ADDED]    {path}")

    if not modified and not deleted and not added:
        print("No changes detected. All monitored files match the baseline.")


def usage():
    print("""
File Integrity Monitoring System

Usage:
    python fim.py baseline <folder>
    python fim.py check <folder>

Example:
    python fim.py baseline sample_data
    python fim.py check sample_data
""")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    command = sys.argv[1].lower()
    folder = sys.argv[2]

    try:
        if command == "baseline":
            create_baseline(folder)
        elif command == "check":
            check_integrity(folder)
        else:
            usage()
    except (FileNotFoundError, PermissionError) as error:
        print(f"Error: {error}")
