# Changed Folders Runner

This GitHub Action detects changed folders within a specified time interval and runs custom commands or scripts for each folder.

## 🚀 Usage

### Inputs:

- `time_interval` (required): Time interval to check for changes (e.g., `"3 hours"`, `"1 day"`).
- `commands` (optional): Multi-line string of commands to run for each folder.
- `script` (optional): Path to a script that runs for each folder. Overrides `commands` if both are provided.

### Example Workflows:

#### ✅ Run Commands Per Folder:

```yaml
name: Command Workflow

on: [push]

jobs:
  run-changed-folders:
    runs-on: ubuntu-latest
    steps:
      - name: Run commands for changed folders
        uses: your-username/your-repo@v1
        with:
          time_interval: '3 hours'
          commands: |
            echo "Building $FOLDER"
            ./build.sh "$FOLDER"
            echo "Testing $FOLDER"
            ./test.sh "$FOLDER"
