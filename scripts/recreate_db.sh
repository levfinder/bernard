#!/bin/bash

set -eux


sudo su - postgres -c "psql -d postgres -c 'DROP DATABASE bernard'"

sudo su - postgres -c "psql -d postgres -c 'CREATE USER bernard WITH PASSWORD '\''bernard'\'''" || true
sudo su - postgres -c "psql -d postgres -c 'CREATE DATABASE bernard WITH OWNER bernard'"

python manage.py migrate
python manage.py createsuperuser --user viren --email viren@example.com
