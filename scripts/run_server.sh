#!/bin/bash

set -eux

source ~/.virtualenvs/levf/bin/activate
source ~/env

./manage.py migrate
./manage.py runserver 0.0.0.0:$PORT
