#!/bin/bash
# fab.test.sh

# Usage: bash scripts/fab.test.sh

source ./.init.sh
source ./venv.activate.sh

cd ${REPO_PATH}
fab test
