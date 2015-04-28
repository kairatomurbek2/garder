#!/bin/bash

. virtualenv/bin/activate
fab production_env deploy:$1
deactivate