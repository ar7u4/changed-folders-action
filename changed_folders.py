# changed_folders.py
import sys
import fnmatch
import fileinput
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
        folder = os.path.dirname(path)
        if folder and not any(fnmatch.fnmatch(folder, pat) for pat in excludes):
            folders.add(os.path.normpath(folder))
    return sorted(folders)

if __name__ == "__main__":
    excludes = []
    stdin_mode = False
    interval = None

    args = sys.argv[1:]
    while args:
        arg = args.pop(0)
        if arg == '--exclude':
            excludes.append(args.pop(0))
        elif arg == '--stdin':
            stdin_mode = True
        else:
            interval = arg

    try:
        if stdin_mode:
            # Process folders from stdin
            folders = [line.strip() for line in fileinput.input('-')]
            filtered = [
                f for f in folders
                if not any(fnmatch.fnmatch(f, pat) for pat in excludes)
            ]
            print('\n'.join(filtered))
        elif interval:
            # Time-based processing
            folders = get_time_based_folders(interval, excludes)
            print('\n'.join(folders))
        else:
            raise ValueError("Missing required arguments")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)