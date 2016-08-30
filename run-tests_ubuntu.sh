#!/bin/bash
# Flask web service test script for Ubuntu 14.04.4
srcpath=/usr/local/src
venv=venv

apt-get update
apt-get install -y gnupg python-dev python-pip python-virtualenv

virtualenv $venv
source $venv/bin/activate
pip install -r $srcpath/requirements.txt
python service_tests.py
deactivate
