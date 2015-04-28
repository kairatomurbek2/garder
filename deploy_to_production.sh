#!/bin/bash

. virtualenv/bin/activate
fab production_env deploy_production:$1
deactivate