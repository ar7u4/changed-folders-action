import os
import subprocess
import sys

def get_changed_folders(time_interval):
    # Validate the time interval
    try:
        value, unit = time_interval.split()
        value = int(value)
        unit = unit.lower()
    except (ValueError, AttributeError):
        raise ValueError(f"Invalid time interval format: {time_interval}. Use '3 hours', '1 day', etc.")

    valid_units = ["seconds", "minutes", "hours", "days", "weeks", "months"]
    if unit not in valid_units:
        raise ValueError(f"Invalid time unit: {unit}. Use {', '.join(valid_units)}.")

    # Git command to get changed files
    git_command = f"git log --name-only --pretty=format: --since='{value} {unit} ago' | grep -v '^$' | sort | uniq"
    try:
        changed_files = subprocess.check_output(git_command, shell=True, text=True).splitlines()
    except subprocess.CalledProcessError:
        print("No changes detected.")
        return ""

    # Extract unique folders
    folders = set()
    for file_path in changed_files:
        folder = os.path.dirname(file_path)
        if folder:
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
