#!/bin/bash
set -e

PROJECT_DIR=/home/bigsurvey/projects/bigsurvey
DB_NAME=bigsurvey
SQL_USER="root"
SQL_PASS="root"

cd ${PROJECT_DIR}
BACKUP_NAME=`ls -t backups | head -n1`

if [ ! -z "$1" ]
then
if [ -f backups/$1 ]
then
BACKUP_NAME=$1
else
echo "Specified backup file does not exist."
fi
else
echo "Trying to use the latest backup from backups folder..."
fi

if [ ! -z "${BACKUP_NAME}" ]
then
echo "Backup name is ${BACKUP_NAME}"
echo "Unpacking backup..."
sudo tar -zxf backups/${BACKUP_NAME} -C ./
echo "Done."

DB_BACKUP=`ls | grep bfp*.gz`

echo "Restoring database..."
gunzip < ${DB_BACKUP} | mysql -u${SQL_USER} -p${SQL_PASS} ${DB_NAME}
echo "Done."

echo "Cleaning up..."
sudo rm -rf ${DB_BACKUP}
touch survey/main/wsgi.py
sudo service apache2 restart
echo "Done."

else
echo "No backups were created yet."
fi