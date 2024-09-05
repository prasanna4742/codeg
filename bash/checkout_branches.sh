#!/bin/bash

# Replace <repository_url> with the actual URL of your repository
repository_url="$1"

# Clone the repository
git clone "$repository_url"

# Change to the cloned repository directory
cd "$(basename "$repository_url")"

# Get a list of all branches
branches=$(git branch --list)

# Iterate over each branch and create a separate directory
for branch in $branches; do
    branch_name=$(echo "$branch" | sed 's/^.\+//')
    mkdir -p "$branch_name"
    git checkout "$branch_name"
    cp -r ./* "$branch_name"
done