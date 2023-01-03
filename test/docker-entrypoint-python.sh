#!/bin/sh
apk update
apk add mysql mysql-client zip
rm -rf /var/cache/apk
sh /var/app/test/run_backup.sh