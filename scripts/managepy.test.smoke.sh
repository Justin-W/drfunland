#!/bin/bash
# managepy.test.sh

# Usage: managepy.test.sh

source ./.init.sh
source ./venv.activate.sh

cd ${REPO_PATH}
echo 'Running tests with: +smoke, -skip, -skip_local.'
python ${APP_NAME}/manage.py test --attr='smoke,!skip,!skip_local' && echo "Done." || echo "Done (with errors)."