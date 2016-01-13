#!/bin/bash
# run.flake8.sh

# Usage: bash run.flake8.sh

source ./.init.sh
source ./venv.activate.sh

cd ${REPO_PATH}
flake8 ${APP_NAME} && echo "flake8 PASSED!" || echo "flake8 FAILED!"
