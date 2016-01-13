#!/bin/bash
# venv.update.sh

# Usage: bash scripts/venv.update.sh

source ./.init.sh

if [ ! -d {VENV_PATH} ]
then
    #create it
    bash ./venv.create.sh
fi

#activate it
source ./venv.activate.sh

#update it

#default ENV_NAME=local
ENV_NAME=${1:-local}

cd ${REPO_PATH}
pip install -r requirements/${ENV_NAME}.txt

echo "Updated venv."
