#!/bin/bash
# managepy.test.sh

# Usage: managepy.test.sh

source ./.init.sh
source ./venv.activate.sh

cd ${REPO_PATH}
USERNAME=`whoami`
echo "Running tests with: user==${USERNAME}."
python ${APP_NAME}/manage.py test --attr="user=${USERNAME}" && echo "Done." || echo "Done (with errors)."