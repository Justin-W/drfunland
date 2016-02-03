#!/bin/bash
# db.fixtures.apply.sh

# Usage: bash db.fixtures.apply.sh

source ./.init.sh
source ./venv.activate.sh

echo "clearing ALL database data"
cd ${MANAGEPY_PATH}
python manage.py flush --noinput
