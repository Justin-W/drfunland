#!/bin/bash
# test.sh

REPO_PATH=~/dev/github/Justin-W/drfunland/drfunland
VENV_PATH=~/pyenvs/drfunlandenv
cd ${REPO_PATH}
source ${VENV_PATH}/bin/activate
#fab serve
fab test
