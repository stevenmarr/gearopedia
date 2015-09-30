#!/usr/bin/python
import sys
import logging
import os
logging.basicConfig(stream=sys.stderr)
os.environ['APP_CONFIG'] = '/var/www/gearopedia/config/production.py'
sys.path.insert(0,"/var/www/gearopedia/")

from gearopedia import app as application
