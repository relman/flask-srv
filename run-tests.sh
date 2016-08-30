#!/bin/bash
srcpath=/usr/local/src
venv=$srcpath/venv

yum update -y
yum install -y gcc gnupg python27-devel python27-pip python27-virtualenv

virtualenv $venv
source $venv/bin/activate
pip install -r $srcpath/requirements.txt
python $srcpath/service_tests.py
deactivate
