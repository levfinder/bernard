#!/bin/bash

set -eux

psql -d 'postgres' -c "CREATE USER bernard WITH PASSWORD 'bernard'"
psql -d 'postgres' -c "CREATE DATABASE bernard WITH OWNER bernard"

