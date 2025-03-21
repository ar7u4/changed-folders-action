#!/bin/sh

# Find changed directories
CHANGED_DIRECTORIES=$(git diff --name-only HEAD~1 HEAD | xargs -I{} dirname {} | sort | uniq)

# Output the changed directories
echo "changed-directories=$CHANGED_DIRECTORIES" >> $GITHUB_OUTPUT