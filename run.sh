#!/bin/bash

echo 'cloning project'
git clone 'https://github.com/GairePravesh/covid19-dashboard'
cd covid19-dashboard
git checkout master

echo "setting up environment ..."
echo "creating vitrual env ..."
python3 -m venv venv
source venv/bin/activate
echo "virtual env created ..."
echo "installing dependencies ..."
pip install -r requirements.txt
echo 'make sure api server is run seprately ...'
echo 'running covid dashboard django server ...'
python3 manage.py runserver 


