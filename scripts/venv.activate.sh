#!/bin/bash
# venv.activate.sh

# Usage: source scripts/venv.activate.sh

source ./.init.sh

source ${VENV_PATH}/bin/activate
python -c 'import sys; print sys.real_prefix' 2>/dev/null && VENV_ACTIVATED=1 || VENV_ACTIVATED=0
