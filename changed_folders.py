# changed_folders.py
import fnmatch
import os
import subprocess
import sys
import json

def get_changed_folders(time_interval, exclude_patterns):
    # ... existing git logic ...

    # Filter excluded folders
    filtered_folders = []
    for folder in sorted(folders):
        if not any(fnmatch.fnmatch(folder, pattern) for pattern in exclude_patterns):
            filtered_folders.append(folder)

    return '\n'.join(filtered_folders)

if __name__ == "__main__":
    exclude_patterns = []
    if len(sys.argv) > 2 and sys.argv[2] == "--exclude":
        exclude_patterns = sys.argv[3].split('\n')

    try:
        folders = get_changed_folders(sys.argv[1], exclude_patterns)
        print(folders)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)