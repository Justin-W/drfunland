#!/bin/bash
# db.migrations.update.sh

# Usage: bash db.migrations.update.sh

source ./.init.sh
source ./venv.activate.sh

echo "creating new migration files (based on the changes you have made to your models)"
cd ${MANAGEPY_PATH}
#python manage.py makemigrations ${DBAPP_NAME}
python manage.py makemigrations
