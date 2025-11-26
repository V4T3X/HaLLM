#!/bin/bash

set -e

sudo apt-get install -y ethtool python3-tk gdb-multiarch tcpdump python3-pip \
                        python3-venv cmake g++ build-essential libpixman-1-dev \
                        clang-format python3-virtualenv python3-virtualenvwrapper \
			ninja-build

echo 
echo "=== Virtualenvwrapper Setup ==="
echo "Add the following lines to your ~/.bashrc or ~/.zshrc:"
echo 
echo "export VIRTUALENVWRAPPER_PYTHON=\$(which python3)"
echo "export WORKON_HOME=$HOME/.virtualenvs"
echo "source /usr/share/virtualenvwrapper/virtualenvwrapper.sh"
echo
echo "After adding, reload your shell with:"
echo "source ~/.bashrc    # or source ~/.zshrc"
echo
echo "Then you can create a virtual environment using mkvirtualenv:"
echo "mkvirtualenv -p \$(which python3) halucinator"
