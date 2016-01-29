#!/bin/bash
# managepy.test.sh

# Usage: bash ./managepy.test.sh

source ./.init.sh
source ./venv.activate.sh

cd ${REPO_PATH}
USERNAME=`whoami`
echo "Running tests with: assignedto='${USERNAME}'."
python ${APP_NAME}/manage.py test --attr="assignedto=${USERNAME}" && echo "Done." || echo "Done (with errors)."