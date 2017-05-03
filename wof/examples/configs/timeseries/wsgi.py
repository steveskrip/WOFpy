#! /home/ubuntu/miniconda/envs/wofpy/bin/python
import sys
sys.path.insert(0, "/var/www/timeseries")

from runserver import app as application
application.secret_key = 'Thisismysecretkey'
