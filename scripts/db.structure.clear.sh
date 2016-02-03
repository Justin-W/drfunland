#!/bin/bash
# db.structure.update.sh

# Usage: bash db.structure.update.sh

source ./.init.sh
source ./venv.activate.sh

echo "applying migration files to the database"
cd ${MANAGEPY_PATH}
python manage.py migrate ${DBAPP_NAME} zero
