#!/bin/bash
# db.fixtures.update.sh

# Usage: bash db.fixtures.update.sh

source ./.init.sh
source ./venv.activate.sh

#default FIXTURE_NAME=testdata
FIXTURE_NAME=${1:-testdata}

FIXTURE_PATH=${DBAPP_NAME}/fixtures/${FIXTURE_NAME}.json
FIXTURE_DIR=${FIXTURE_PATH%/"${FIXTURE_NAME}"*}

echo "updating '${FIXTURE_NAME}' data fixture files (based on the data currently in the database)"
cd ${MANAGEPY_PATH}

# ensure the destination dir exists
[ ! -d ${FIXTURE_DIR} ] && mkdir -p ${FIXTURE_DIR}

# export the current database data to the fixture file (as JSON by default)
python manage.py dumpdata ${DBAPP_NAME} > ${FIXTURE_PATH}

# convert the fixture file to pretty-printed format (makes DIFFing and SCM much easier)

#the following line doesn't allow us to specify any formatting options
#cat ${FIXTURE_PATH} | python -m json.tool > ${FIXTURE_PATH}.temp && mv ${FIXTURE_PATH}.temp ${FIXTURE_PATH}

#the following implementation DOES allow us to specify formatting options
python -c'import json,sys; s=open(sys.argv[1]).read(); print json.dumps(json.loads(s), indent=4, sort_keys=False)' ${FIXTURE_PATH} > ${FIXTURE_PATH}.temp && mv ${FIXTURE_PATH}.temp ${FIXTURE_PATH}
#PY_CODE="import json,sys; s=open(sys.argv[1]).read(); print json.dumps(json.loads(s), indent=4, sort_keys=False)"
#python -c'${PY_CODE}' ${FIXTURE_PATH} > ${FIXTURE_PATH}.temp && mv ${FIXTURE_PATH}.temp ${FIXTURE_PATH}
