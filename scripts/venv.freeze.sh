#!/bin/bash
# venv.freeze.sh

# Usage: bash scripts/venv.freeze.sh.sh
# Usage: source scripts/venv.freeze.sh.sh

source ./.init.sh
source ./venv.activate.sh

#default OUTPUT_FILENAME=requirements.txt
OUTPUT_FILENAME=${1:-requirements.txt}

#create the output dir if it doesn't exist
[ ! -d ${SCRIPTS_OUTPUT_PATH} ] && mkdir -p ${SCRIPTS_OUTPUT_PATH}

pip freeze > ${SCRIPTS_OUTPUT_PATH}/${OUTPUT_FILENAME}

echo "Freeze file created at: ${SCRIPTS_OUTPUT_PATH}/${OUTPUT_FILENAME}"
