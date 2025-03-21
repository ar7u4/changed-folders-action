# changed_folders.py
import os
import subprocess
import sys
from shlex import quote

def get_changed_folders(time_interval):
    try:
        value, unit = time_interval.split()
        value = int(value)
        unit = unit.rstrip('s')  # Handle plural units
    except ValueError:
        raise ValueError("Invalid time interval format. Use '<number> <unit>' (e.g., '3 hours'). Valid units: seconds, minutes, hours, days, weeks.")

    valid_units = ["second", "minute", "hour", "day", "week"]
    if unit not in valid_units:
        raise ValueError(f"Invalid unit: {unit}. Valid options: {', '.join(valid_units)}")

    # Build safe git command
    git_cmd = [
        'git', 'log',
        '--name-only',
        '--pretty=format:',
        f'--since="{value} {unit}s ago"',
        '--diff-filter=d'  # Exclude deleted files
    ]

    try:
        result = subprocess.run(
            git_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git command failed: {e.stderr}")

    changed_files = [
        line.strip() for line in result.stdout.splitlines()
        if line.strip() and not line.startswith('"')
    ]

    folders = set()
    for file_path in changed_files:
        folder = os.path.dirname(file_path)
        if folder:
            folders.add(os.path.normpath(folder))  # Normalize path

    return '\n'.join(sorted(folders))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python changed_folders.py <time_interval>")
        sys.exit(1)

    try:
        folders = get_changed_folders(sys.argv[1])
        print(folders)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)