#!/bin/bash
set -e

CURRENT=`pwd`
PROJECT_DIR=`basename "$CURRENT"`
DB_NAME=${1}
SQL_USER=${2}
SQL_PASS=${3}
CURRENTDATE=`date +%Y-%m-%d-%s`
echo "$PROJECT_DIR"

echo "Dumping database..."
mysqldump -u${SQL_USER} -p${SQL_PASS} ${DB_NAME} | gzip -c > bigsurvey_${CURRENTDATE}.gz
echo "Done."

echo "Packing backup..."
tar -zcf ./backups/backup_${CURRENTDATE}.tar.gz bigsurvey fabfile.py create_backup.sh restore_backup.sh install* bigsurvey_${CURRENTDATE}.gz
echo "Done."

echo "Cleaning up..."
rm bigsurvey_${CURRENTDATE}.gz
cd backups
if [ `ls -1 | grep backup | wc -l` -gt 5 ]
then
rm -rf `ls -t | grep backup | tail -n1`
fi
echo "Done."