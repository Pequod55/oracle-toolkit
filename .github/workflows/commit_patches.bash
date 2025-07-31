#!/bin/bash
# Script to automate git operations for patch list modifications

# Exit immediately if a command exits with a non-zero status.
# Treat unset variables as an error.
# The return value of a pipeline is the status of the last command to exit with a non-zero status.
set -euo pipefail

#
# Script configuration
#
GIT_USER="GitHub Actions"
GIT_EMAIL="actions@github.com"
PATCH_FILE="modify_patchlist.yaml"
COMMIT_MESSAGE="automation: Update patch files"

#
# Main execution
#
main() {
    # Check for required environment variables passed from the workflow
    if [[ -z "${PR_BRANCH}" || -z "${GITHUB_REPO}" || -z "${GITHUB_TOKEN}" ]]; then
        echo "Error: Required environment variables (PR_BRANCH, GITHUB_REPO, GITHUB_TOKEN) are not set."
        exit 1
    fi

    # Check for changes in the primary trigger file.
    # The `|| true` prevents the script from exiting if there are no changes,
    # as `git status --porcelain` would return an empty string and the `if` would be false.
    if ! git status --porcelain "${PATCH_FILE}" | grep -q .; then
        echo "No modifications in ${PATCH_FILE}, skipping commit."
        exit 0
    fi
    
    echo "Modified ${PATCH_FILE} detected, proceeding with commit and push."
    
    # Configure git user
    git config --global user.name "${GIT_USER}"
    git config --global user.email "${GIT_EMAIL}"
    
    # Add, commit, and push the changes
    # Use a specific file list if possible, otherwise `.` is okay.
    git add .
    
    # Commit the changes
    git commit -m "${COMMIT_MESSAGE}"
    
    # Push the changes to the correct PR branch using the token for authentication
    # The "HEAD:${PR_BRANCH}" syntax pushes the current commit to the specified remote branch.
    echo "Pushing changes to branch '${PR_BRANCH}'..."
    git push "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git" "HEAD:${PR_BRANCH}"
    
    echo "Changes pushed successfully."
}

main "$@"