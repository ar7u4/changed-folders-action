import os
import subprocess
import sys

def get_changed_folders(time_interval):
    git_command = f"git log --name-only --pretty=format: --since='{time_interval}' | grep -v '^$' | sort | uniq"
    changed_files = subprocess.check_output(git_command, shell=True, text=True).splitlines()

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
    folders = get_changed_folders(time_interval)
    print(folders)
