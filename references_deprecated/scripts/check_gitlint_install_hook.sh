#!/bin/bash

# Check if gitlint is installed
if ! command -v gitlint &> /dev/null
then
    echo "gitlint could not be found. Please install gitlint first."
    exit 1
fi

# Check if gitlint install-hook is set up
# Check if commit-msg hook is installed
if [ ! -f .git/hooks/commit-msg ] || ! grep -q "gitlint" .git/hooks/commit-msg; then
    echo "commit-msg hook is not set up. Setting it up now..."
    gitlint install-hook
    if [ $? -eq 0 ]; then
        echo "gitlint install-hook set up successfully."
    else
        echo "Failed to set up gitlint install-hook."
        exit 1
    fi
else
    echo "gitlint install-hook is already set up."
fi