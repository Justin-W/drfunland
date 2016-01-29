#!/bin/bash
# venv.activate.sh

# Usage: source ./venv.activate.sh

source ./.init.sh

if [ ! -d ${VENV_PATH} ]
then
    #create it
    bash ./venv.create.sh
    echo "Created venv."
fi

source ${VENV_PATH}/bin/activate
python -c 'import sys; print sys.real_prefix' 2>/dev/null && VENV_ACTIVATED=1 || VENV_ACTIVATED=0
