#!/bin/bash

. virtualenv/bin/activate
# $1 here is Jenkins build number that you should pass to this file from command line
TAG="$(read -r version < version_source; echo ${version//\*/$1})"
fab demo_env deploy_demo:${TAG}
deactivate