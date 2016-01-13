#!/bin/bash
# venv.update.hard.sh

# Usage: bash scripts/venv.update.hard.sh

source ./.init.sh

bash ./venv.delete.sh
bash ./venv.create.sh
bash ./venv.update.sh $1

echo "Recreated venv."
