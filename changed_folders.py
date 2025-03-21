import os
import subprocess
import sys

def get_changed_folders(time_interval):
    # Validate and parse the time interval input.
    try:
        parts = time_interval.split()
        if len(parts) != 2:
            raise ValueError
        value, unit = parts
        value = int(value)
        unit = unit.lower()
    except ValueError:
        raise ValueError("Invalid time interval format. Use '<number> <unit>' (e.g., '3 hours'). Valid units: seconds, minutes, hours, days, weeks, months.")

    valid_units = ["seconds", "minutes", "hours", "days", "weeks", "months"]
    if unit not in valid_units:
        raise ValueError(f"Invalid unit: {unit}. Valid options: {', '.join(valid_units)}")

    # Use the git log with --since to filter changes.
    git_time_arg = f"--since='{value} {unit} ago'"
    git_command = f"git log --name-only --pretty=format: {git_time_arg} | grep -v '^$' | sort | uniq"
    changed_files = subprocess.check_output(git_command, shell=True, text=True).splitlines()

    folders = set()
    for file_path in changed_files:
        folder = os.path.dirname(file_path)
        if folder:  # Ignore files at root
            folders.add(folder)

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
