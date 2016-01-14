#!/bin/bash
# scripts.init.sh

# NOTE: This script MUST be executed from the directory it resides in, or else the SCRIPTS_PATH var will be wrong

VENV_PATH=~/pyenvs/drfunlandenv
APP_NAME=drfunapp

SCRIPTS_PATH=$PWD
SCRIPTS_OUTPUT_PATH=${SCRIPTS_PATH}/out
REPO_PATH=${SCRIPTS_PATH%/scripts*}
REPO_NAME=${REPO_PATH##*/}
VENV_NAME=${VENV_PATH##*/}