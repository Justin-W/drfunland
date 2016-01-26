#!/bin/bash
# workspace.update.osx.sh

# Usage: bash workspace.update.osx.sh

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

echo ""
echo "Updating workspace..."

echo ""
echo "brew:"
brew --version || ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update

echo ""
echo "brew doctor:"
brew doctor 2>&1

echo ""
echo "brew cask:"
brew cask --version || brew install caskroom/cask/brew-cask

echo ""
echo "pkg-config:"
pkg-config --version || brew install pkg-config

echo ""
echo "git:"
git --version || brew install git

echo ""
echo "python (2.x):"
type python || brew install python

echo ""
echo "virtualenv:"
type virtualenv || pip install virtualenv

echo ""
echo "postgres:"
postgres --version || brew install postgresql

echo ""
echo "graphviz:"
type dot || brew install graphviz
#brew info graphviz || brew install graphviz

#echo ""
#echo "java:"
#type java
#java -version 2>&1

#echo ""
#echo "IntelliJ:"
#ls /Applications/ | grep -i intellij


### Clean Up

### un-redirect stdout
#restore stdout (using the previously cached FD)
exec 1<&4


### print the location of the output file
echo "Log file created at: ${OUTPUT_FILEPATH}"
open ${OUTPUT_FILEPATH}
