#!/bin/sh
# run.sh
# 2023-01-01 | CR
#
APP_DIR='src'
ENV_FILESPEC=""
if [ -f "./.env" ]; then
    ENV_FILESPEC="./.env"
fi
if [ -f "../.env" ]; then
    ENV_FILESPEC="../.env"
fi
if [ "$ENV_FILESPEC" != "" ]; then
    set -o allexport; source ${ENV_FILESPEC}; set +o allexport ;
fi
if [ "$1" = "deactivate" ]; then
    cd ${APP_DIR} ;
    deactivate ;
fi
if [[ "$1" != "deactivate" && "$1" != "pipfile" && "$1" != "clean" && "$1" != "test" ]]; then
    python3 -m venv ${APP_DIR} ;
    . ${APP_DIR}/bin/activate ;
    cd ${APP_DIR} ;
    pip3 install -r requirements.txt ;
fi
if [ "$1" = "pipfile" ]; then
    deactivate ;
    pipenv lock
fi
if [ "$1" = "clean" ]; then
    echo "Cleaning..."
    deactivate ;
    rm -rf __pycache__ ;
    rm -rf bin ;
    rm -rf include ;
    rm -rf lib ;
    rm -rf pyvenv.cfg ;
    ls -lah
fi
if [[ "$1" = "run" || "$1" = "" ]]; then
    echo "Run..."
    python do_bkp_db.py ${BACKUP_CONFIG_FILENAME}
    echo "Done..."
fi
if [ "$1" = "test" ]; then
    cd test
    # docker-compose -f docker-compose-mysql.yml up -d --build
    # docker exec -ti mysql bash
    docker-compose -f docker-compose-python.yml up -d --build
    docker exec -ti python_alpine sh
fi
