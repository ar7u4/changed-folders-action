# changed_folders.py
import sys
import fnmatch
import fileinput
import os  # <-- ADD MISSING IMPORT
from datetime import datetime, timedelta
import subprocess
import re

def parse_time_interval(interval):
    units = {
        'sec': 'seconds', 'min': 'minutes', 'hr': 'hours',
        'day': 'days', 'week': 'weeks', 'month': 'months'
    }
    total = timedelta()

    matches = re.findall(r'(\d+)\s*(sec|min|hr|day|week|month)s?', interval.lower())
    for value, unit in matches:
        kwargs = {units[unit]: int(value)}
        total += timedelta(**kwargs)

    return datetime.now() - total

def get_time_based_folders(interval, excludes):
    cutoff = parse_time_interval(interval)
    cmd = [
        'git', 'log',
        '--name-only',
        '--pretty=format:',
        f'--since={cutoff.isoformat()}',
        '--diff-filter=dACMRTUXB'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return process_files(result.stdout, excludes)

def process_files(git_output, excludes):
    folders = set()
    for path in filter(None, git_output.split('\n')):
        folder = os.path.dirname(path)  # <-- REQUIRES os MODULE
        if folder and not any(fnmatch.fnmatch(folder, pat) for pat in excludes):
            folders.add(os.normpath(folder))  # <-- NORMALIZE PATH
    return sorted(folders)

# Rest of the script remains the same...