#!/bin/bash
set -e

echo =================== DOWNLOAD PWS BACKUP ===================
cd /tmp
mkdir backup
scp garder@162.243.84.251:$1 /tmp/backup

DIR=/tmp/backup/*.gz

if [ "$(ls -A $DIR 2> /dev/null)" == "" ]; then
  echo "not gz"
else
  tar -zxvf /tmp/backup/*.gz -C /tmp/backup
fi