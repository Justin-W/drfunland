#!/bin/bash
# venv.update.hard.sh

# Usage: bash scripts/venv.update.hard.sh

source ./.init.sh

#remove the existing venv dir
[ -d ${VENV_PATH} ] && rm -rf ${VENV_PATH} || echo "Directory not found."

echo "Deleted venv."
