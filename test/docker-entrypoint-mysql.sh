#!/bin/sh
# docker-entrypoint.sh
# 2023-01-02 | CR
#
# https://tecadmin.net/how-to-install-python-3-9-on-debian-9/

cd /tmp

apt -y update
apt -y upgrade

apt -y install wget build-essential libreadline-gplv2-dev libncursesw5-dev \
     libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
     libffi-dev zlib1g-dev

wget https://www.python.org/ftp/python/3.9.4/Python-3.9.4.tgz
tar xzf Python-3.9.4.tgz

cd Python-3.9.4
./configure --enable-optimizations
make altinstall

python3.9 -V
pip3.9 -V

ln -s /usr/local/bin/python3.9 /usr/local/bin/python3
ln -s /usr/local/bin/pip3.9 /usr/local/bin/pip3

mkdir -p /usr/local/opt/python@3.10/bin
ln -s /usr/local/bin/python3.9 /usr/local/opt/python@3.10/bin/python3.10

cd /var/app
# bash run.sh run


