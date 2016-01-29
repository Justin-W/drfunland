#!/bin/bash
# venv.create.sh

# Usage: bash ./venv.create.sh

source ./.init.sh

VENV_PARENT=${VENV_PATH%/"${VENV_NAME}"*}
echo ${VENV_PARENT}

cd ${VENV_PARENT}
virtualenv -p python ${VENV_PATH}

echo "New venv created at: ${VENV_PATH}"
