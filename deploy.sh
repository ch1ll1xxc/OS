#!/bin/bash

apt install python3
pip install virtualenv
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
tar -xvf blocknote-master.tar.gz blocknote-master
cd blocknote-master
echo -e "from django.apps import AppConfig\n\nclass BaseConfig(AppConfig):\n\tname = 'todoapp'" > apps/todoapp/apps.py
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
