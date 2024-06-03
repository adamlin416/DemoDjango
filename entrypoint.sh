#!/bin/bash

./wait-for-it.sh db:3306 --

python ./demobotrista/manage.py migrate
python ./demobotrista/manage.py manage_groups

exec "$@"