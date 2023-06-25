#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PYTHON_SUFFIX=""

curl -sSL https://install.python-poetry.org | python3 -

poetry install

chmod +x $SCRIPT_DIR/.hooks/install_hooks.sh
$SCRIPT_DIR/.hooks/install_hooks.sh
