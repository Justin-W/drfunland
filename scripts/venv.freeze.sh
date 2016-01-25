#!/bin/bash
# venv.freeze.sh

# Usage: bash scripts/venv.freeze.sh

source ./.init.sh
source ./venv.activate.sh


### determine the output file, path, etc.
OUTPUT_FILENAME=${1:-requirements.txt}
OUTPUT_FILEPATH=${SCRIPTS_OUTPUT_PATH}/${OUTPUT_FILENAME}
#create the output dir if it doesn't exist
[ ! -d ${SCRIPTS_OUTPUT_PATH} ] && mkdir -p ${SCRIPTS_OUTPUT_PATH}


### generate the output file
pip freeze > ${OUTPUT_FILEPATH}


### print the location of the output file
echo "Freeze file created at: ${OUTPUT_FILEPATH}"
open ${OUTPUT_FILEPATH}
