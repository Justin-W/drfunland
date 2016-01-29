#!/bin/bash
# venv.update.sh

# Usage: bash ./venv.update.sh

# activate the venv (creating a new one if necessary)
source ./venv.activate.sh

# now update it (fast/non-hard)

#default ENV_NAME=local
ENV_NAME=${1:-local}

cd ${REPO_PATH}
pip install -r requirements/${ENV_NAME}.txt

echo "Updated venv."
