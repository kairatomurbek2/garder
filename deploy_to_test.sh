#!/bin/bash

. virtualenv/bin/activate
fab demo_env deploy:$1
deactivate