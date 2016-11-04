#!/bin/bash

if [ ! -d "virtualenv" ]; then
    virtualenv --no-site-packages --distribute virtualenv
fi
. virtualenv/bin/activate
pip install -r requirements.txt
deactivate
