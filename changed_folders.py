import os
import subprocess
import sys

def get_changed_folders(time_interval):
    # Validate and parse the time interval input.
    # Expected format: "<number> <unit>" e.g., "3 hours"
    try:
        parts = time_interval.split()
        if len(parts) != 2:
            raise ValueError
        value, unit = parts
        value = int(value)
        unit = unit.lower()
    except ValueError:
        raise ValueError("Invalid time interval format. Use the format: '<number> <unit>' (e.g., '3 hours'). Valid units: seconds, minutes, hours, days, weeks, months.")

    valid_units = ["seconds", "minutes", "hours", "days", "weeks", "months"]
    if unit not in valid_units:
        raise ValueError(f"Invalid unit: {unit}. Valid options: {', '.join(valid_units)}")

    # Git expects the interval with an "ago" suffix.
    # For example: "3 hours ago"
    git_time_arg = f"--since='{value} {unit} ago'"

    # Construct the git command to retrieve changed files.
    git_command = f"git log --name-only --pretty=format: {git_time_arg} | grep -v '^$' | sort | uniq"
    changed_files = subprocess.check_output(git_command, shell=True, text=True).splitlines()

    # Extract unique folders from changed files.
    folders = set()
    for file_path in changed_files:
        folder = os.path.dirname(file_path)
        if folder:  # Ignore root-level files
            folders.add(folder)

    # Return folders as a space-separated string.
    return " ".join(folders)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python changed_folders.py <time_interval>")
        sys.exit(1)

    time_interval = sys.argv[1]
    try:
        folders = get_changed_folders(time_interval)
        print(folders)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
