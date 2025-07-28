#!/bin/bash
# Script to automate git operations for patch list modifications
# Checks for changes in specific files and pushes updates if necessary

#
# Default git configuration values
#
GIT_USER="GitHub Actions"
GIT_EMAIL="actions@github.com"
PATCH_FILE="modify_patchlist.yaml"

#
# Function to configure git global settings
#
configure_git() {
    git config --global user.name "${GIT_USER}"
    git config --global user.email "${GIT_EMAIL}"
    git config --global pull.rebase false
}

#
# Function to check if specific file has changes
#
check_file_changes() {
    local file=$1
    if [[ $(git status --porcelain "${file}") ]]; then
        echo "Modified ${file} detected, proceeding with modifications."
        return 0
    else
        echo "No modifications in ${file}, skipping further steps."
        return 1
    fi
}

#
# Function to commit and push changes
#
commit_and_push() {
    if [[ $(git status --porcelain) ]]; then
        configure_git
        git add .
        git commit -m "automation: Update patch files"
        git push
        echo "Changes pushed successfully."
    fi
}

#
# Main execution
#
main() {
    # Check for changes in patch file
    if ! check_file_changes "${PATCH_FILE}"; then
        exit 0
    fi
    
    # Commit and push if there are changes
    commit_and_push
}

main "$@"