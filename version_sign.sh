#!/bin/bash
read -r version < version_source
git tag ${version//\*/$1}
git push --tags