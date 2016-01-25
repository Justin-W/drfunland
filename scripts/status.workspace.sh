#!/bin/bash
# status.workspace.sh

# Usage: bash scripts/status.workspace.sh

source ./.init.sh


### determine the output file, path, etc.
OUTPUT_FILENAME=${1:-"$0.log"}
OUTPUT_FILEPATH=${SCRIPTS_OUTPUT_PATH}/${OUTPUT_FILENAME}
#create the output dir if it doesn't exist
[ ! -d ${SCRIPTS_OUTPUT_PATH} ] && mkdir -p ${SCRIPTS_OUTPUT_PATH}


### temporarily redirect stdout to the output file
#cache the current stdout (as FD #4)
exec 4<&1
#redirect stdout to the output file
exec 1>${OUTPUT_FILEPATH}


### generate the output file

#reset/empty any existing file
> ${OUTPUT_FILEPATH}

echo "###"
echo "### ENV variables (inactive virtualenv)"
echo "###"
echo ""
printenv

echo ""
echo "###"
echo "### SHELL variables (inactive virtualenv)"
echo "###"
echo ""
( set -o posix ; set ) | less

#source ./venv.activate.sh 1>/dev/null 2>> ${OUTPUT_FILEPATH}
source ./venv.activate.sh 1>/dev/null

echo ""

echo ""
echo "###"
echo "### ENV variables (active virtualenv)"
echo "###"
echo ""
printenv

echo ""
echo "###"
echo "### SHELL variables (active virtualenv)"
echo "###"
echo ""
( set -o posix ; set ) | less


echo ""
echo "###"
echo "### declare -f (active virtualenv)"
echo "###"
echo ""
declare -f


echo ""
echo "###"
echo "### Other ENV info (active virtualenv)"
echo "###"
echo ""

echo ""
echo "python:"
type python
python --version 2>&1

echo ""
echo "bash:"
type bash
bash --version

echo ""
echo "virtualenv:"
type virtualenv

echo ""
echo "pip:"
type pip
pip --version

echo ""
echo "brew:"
type brew
brew --version

echo ""
echo "git:"
type git
git --version

echo ""
echo "postgres:"
type postgres
postgres --version

echo ""
echo "createdb:"
type createdb

echo ""
echo "fab:"
type fab

echo ""
echo "graphviz:"
type dot
dot -V 2>&1
type neato
neato -V 2>&1

echo ""
echo "java:"
type java
java -version 2>&1

echo ""
echo "IntelliJ:"
ls /Applications/ | grep -i intellij


### Clean Up

### un-redirect stdout
#restore stdout (using the previously cached FD)
exec 1<&4


### print the location of the output file
echo "Log file created at: ${OUTPUT_FILEPATH}"
open ${OUTPUT_FILEPATH}
