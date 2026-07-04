# Python File Integrity Monitor

A Python command-line file integrity monitor that creates a cryptographic snapshot of a directory and detects file additions, deletions, and modifications by comparing the current state against a previously saved snapshot.

## Features

- Assign a directory to monitor
- Generate SHA-256 hashes for all files
- Save snapshots in JSON format
- Compare the current directory against the last snapshot
- Detect:
  - Added files
  - Deleted files
  - Modified files
- Clear scan summary and status report
- Handles invalid directories and corrupted snapshot files

## Concepts Implemented

- File hashing with `hashlib`
- Directory traversal using `os.walk()`
- File and path handling with `os.path`
- JSON serialization and deserialization
- Dictionaries
- Functions
- File I/O
- Exception handling
- Cryptographic hash verification

## How It Works

### Assign Directory

- Enter the directory you want to monitor.
- The program recursively scans every file.
- A SHA-256 hash is generated for each file.
- A snapshot is saved as a JSON file.

### Compare Directory

- Load the previously saved snapshot.
- Scan the directory again.
- Compare the new hashes against the saved hashes.
- Display all added, deleted, and modified files along with a summary.

## Example Output

```text
========== SCAN RESULTS ==========

Monitoring Directory:
/home/user/Documents

Files Scanned: 12

========== ADDED FILES ==========

notes.txt

========== DELETED FILES ==========

old_report.pdf

========== MODIFIED FILES ==========

config.ini

========== SUMMARY ==========

Added:    1
Deleted:  1
Modified: 1

Status: WARNING - File changes detected.
```

## Requirements

- Python 3.x
- Uses only Python's standard library (`os`, `hashlib`, `json`)

## Future Improvements

- Automatic scheduled scans
- Snapshot history and versioning
- Logging scan results
- Ignore/include file rules
- Support for multiple snapshot locations
