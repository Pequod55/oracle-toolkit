if [[ `git status --porcelain modify_patchlist.yaml` ]]; then
    echo "Modified patchlist detected, proceeding with modifications."
else
    echo "No modifications in patchlist, skipping further steps."
    exit 0
fi
if [[ `git status --porcelain` ]]; then
    git config --global user.name "GitHub Actions"
    git config --global user.email "actions@github.com"
    git config --global pull.rebase false
    git add .
    git commit -m "automation: Update files"
    git push
    echo "Changes pushed successfully."