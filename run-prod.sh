#!/bin/bash
# Simple shell script to run application in dev mode

python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py run


