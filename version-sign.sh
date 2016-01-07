#!/bin/bash
read -r version < version-source
git tag ${version//\*/$1}
git push --tags