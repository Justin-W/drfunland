#!/bin/bash
# managepy.test.sh

# Usage: managepy.test.sh

source ./.init.sh
source ./venv.activate.sh

cd ${REPO_PATH}
python ${APP_NAME}/manage.py test && echo "Done." || echo "Done (with errors)."