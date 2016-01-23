#!/bin/bash
# managepy.test.sh

# Usage: managepy.test.sh

source ./.init.sh
source ./venv.activate.sh

cd ${REPO_PATH}
echo 'Running tests with: +runme.'
python ${APP_NAME}/manage.py test --attr='runme' && echo "Done." || echo "Done (with errors)."