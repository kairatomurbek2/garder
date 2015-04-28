#!/bin/bash

. virtualenv/bin/activate
fab demo_env deploy_demo:$1
deactivate