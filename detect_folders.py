import os
import sys
import subprocess
import fnmatch
from datetime import datetime, timedelta
import re

def parse_interval(interval):
    units = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days'}
    total = timedelta()

    matches = re.findall(r'(\d+)([smhd])', interval.lower())
    for value, unit in matches:
        kwargs = {units[unit]: int(value)}
        total += timedelta(**kwargs)

    return datetime.now() - total

def get_folders(mode, interval=None, excludes=None):
    if mode == 'last-push':
        cmd = ['git', 'diff', '--name-only', 'HEAD^', '--diff-filter=dACMR']
    else:
        cutoff = parse_interval(interval)
        cmd = [
            'git', 'log',
            '--name-only',
            '--pretty=format:',
            f'--since={cutoff.isoformat()}',
            '--diff-filter=dACMR'
        ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    folders = set()

    for filepath in filter(None, result.stdout.split('\n')):
        folder = os.path.dirname(filepath)
        if folder and not any(fnmatch.fnmatch(folder, pat) for pat in excludes):
            folders.add(os.path.normpath(folder))

    return sorted(folders)

if __name__ == '__main__':
    mode = sys.argv[1]
    excludes = []
    args = sys.argv[2:]

    while args:
        if args[0] == '--exclude':
            excludes.append(args.pop(1))
        else:
            interval = args.pop(0)

    folders = get_folders(mode, interval, excludes)
    print('\n'.join(folders))