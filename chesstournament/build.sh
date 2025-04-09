#!/usr/bin/env bash

set -o errexit #noqa E999

pip3 install -r requirements.txt

make static COLLECTSTATIC_FLAGS=--noinput
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py populate

echo "creado"