# Repository Labels

This directory contains the configuration for GitHub repository labels that are automatically synced by the label-sync workflow.

## Files

- `labels.yml`: Defines all labels used in this repository
- `workflows/label-sync.yml`: Workflow that automatically syncs labels

## How It Works

The label-sync workflow automatically:
1. Runs when changes are pushed to the main branch
2. Reads label definitions from `labels.yml`
3. Creates or updates labels in the repository
4. Preserves existing labels not defined in the config file

## Adding New Labels

To add a new label:

1. Edit `.github/labels.yml`
2. Add your label definition:
   ```yaml
   - name: "your-label-name"
     color: "hexcolor"  # without # prefix
     description: "Label description"
   ```
3. Commit and push to main branch
4. The workflow will automatically sync the labels

## Required Labels

The following labels are required by Dependabot and other automation:

- `github-actions`: For GitHub Actions dependency updates
- `dependencies`: For all dependency updates
- `python`: For Python dependency updates
- `docker`: For Docker dependency updates

## Manual Trigger

You can manually trigger the label sync workflow from the Actions tab in GitHub.
