#!/usr/bin/env python

import sys
import site

site.addsitedir('/var/www/gcs/lib/python3.6/site-packages')

sys.path.insert(0, '/var/www/gcs')

from app import app as application