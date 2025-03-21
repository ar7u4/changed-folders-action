def get_time_based_folders(interval, excludes):
    cutoff = parse_time_interval(interval)

    # Get current branch name
    branch_cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
    branch_result = subprocess.run(branch_cmd, capture_output=True, text=True)
    if branch_result.returncode != 0:
        raise RuntimeError(f"Failed to get branch: {branch_result.stderr}")
    current_branch = branch_result.stdout.strip()

    # Find first parent commit in the time window
    commit_cmd = [
        'git', 'log',
        '--first-parent',
        '--until', cutoff.isoformat(),
        '--format=%H',
        '-n', '1',
        current_branch
    ]

    commit_result = subprocess.run(commit_cmd, capture_output=True, text=True)
    if commit_result.returncode != 0:
        raise RuntimeError(f"Commit lookup failed: {commit_result.stderr}")

    base_commit = commit_result.stdout.strip() or 'HEAD^'

    # Get changed files between commits
    diff_cmd = [
        'git', 'diff',
        '--name-only',
        '--diff-filter=dACMRTUXB',
        f'{base_commit}..HEAD'
    ]

    diff_result = subprocess.run(diff_cmd, capture_output=True, text=True)
    if diff_result.returncode != 0:
        raise RuntimeError(f"Git diff failed: {diff_result.stderr}")

    return process_files(diff_result.stdout, excludes)