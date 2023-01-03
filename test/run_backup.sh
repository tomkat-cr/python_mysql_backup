#!/bin/sh
cd /var/app
set -o allexport; source .env; set +o allexport ;

if [ "$1" == "regen"]; then
    rm -rf src/bin
    python3 -m venv src
    . src/bin/activate
    cd src
    pip install -r requirements.txt
    python -m pip install python-dotenv
else
    . src/bin/activate
    cd src
fi

python -m do_bkp_db ${BACKUP_CONFIG_FILENAME}
