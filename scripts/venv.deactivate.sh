#!/bin/bash
# venv.deactivate.sh

# Usage: source ./venv.deactivate.sh

source ./.init.sh

python -c 'import sys; print sys.real_prefix' 2>/dev/null && VENV_ACTIVATED=1 || VENV_ACTIVATED=0
#[[ "$(type -t deactivate)" != function ]]; VENV_ACTIVATED=$?

if [ 1 -eq ${VENV_ACTIVATED} ]
then
    #deactivate the venv
    deactivate
    #source ${VENV_PATH}/bin/deactivate

    python -c 'import sys; print sys.real_prefix' 2>/dev/null && VENV_ACTIVATED=1 || VENV_ACTIVATED=0
fi
