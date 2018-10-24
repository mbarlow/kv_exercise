#!/bin/bash

echo
echo '-----------------------------------------------------'
echo Setting up virtual env.
echo '-----------------------------------------------------'
echo

virtualenv env
source env/bin/activate

echo
echo '-----------------------------------------------------'
echo Installing requirements.txt inside virtualenv.
echo '-----------------------------------------------------'
echo

pip install -r requirements.txt

echo
echo '-----------------------------------------------------'
echo Running unittests...
echo '-----------------------------------------------------'
echo

python tests.py

echo
echo '-----------------------------------------------------'
echo Done building ship! Run: ./run.sh to launch flask app
echo '-----------------------------------------------------'
echo
