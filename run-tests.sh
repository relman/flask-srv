#!/bin/bash
srcpath=/usr/local/src

apt-get update
apt-get install -y gnupg python-dev python-pip python-virtualenv

virtualenv venv
source venv/bin/activate
pip install -r $srcpath/requirements.txt
python service_tests.py
deactivate
