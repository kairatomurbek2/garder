#!/bin/bash
set -e

echo =================== UPLOAD PWS BACKUP ===================
scp /tmp/$1 garder@162.243.84.251:$2
ssh garder@162.243.84.251 /bin/bash delete_old_backups.sh