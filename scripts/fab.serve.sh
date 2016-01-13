#!/bin/bash
# fab.serve.sh

# Usage: bash scripts/fab.serve.sh
# Usage: source scripts/fab.serve.sh

source ./.init.sh
source ./venv.activate.sh

cd ${REPO_PATH}
fab serve
