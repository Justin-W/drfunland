#!/bin/bash
# db.fixtures.apply.sh

# Usage: bash db.fixtures.apply.sh

source ./.init.sh
source ./venv.activate.sh

#default FIXTURE_NAME=testdata
FIXTURE_NAME=${1:-testdata}

echo "applying '${FIXTURE_NAME}' data fixture files (to the database)"
cd ${MANAGEPY_PATH}
python manage.py loaddata ${FIXTURE_NAME}
