#!/bin/bash
# установка Python
# TODO - получить версию через параметр командной строки 
# https://www.python.org/ftp/python

PYTHON_VER=3.10.5

sudo apt -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libsqlite3-dev
sudo apt -y install libssl-dev libsqlite3-dev libreadline-dev libffi-dev libbz2-dev liblzma-dev

wget https://www.python.org/ftp/python/$PYTHON_VER/Python-$PYTHON_VER.tgz
tar -xf Python-$PYTHON_VER.tgz && cd Python-$PYTHON_VER || exit
./configure --enable-optimizations && make -j "$(nproc)"
sudo make altinstall