#!/bin/bash
# venv.delete.sh

# Usage: bash ./venv.delete.sh

source ./.init.sh

#remove the existing venv dir
[ -d ${VENV_PATH} ] && rm -rf ${VENV_PATH} || echo "Directory not found."

echo "Deleted venv."
