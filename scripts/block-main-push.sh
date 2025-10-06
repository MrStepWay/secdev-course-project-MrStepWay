#!/bin/bash

# Имя текущей ветки
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ "$CURRENT_BRANCH" == "main" ]; then
    echo -e "ERROR: Direct push to the main branch is forbidden!"
    echo "Please use a feature branch and create a Pull Request."
    exit 1
fi

exit 0
