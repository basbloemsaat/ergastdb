#!/usr/bin/env python

from datetime import datetime, tzinfo
from dateutil import parser
import json
import os
import requests
import shutil
import pathlib


# get the latests ergast db file, unless it already was downloaded

url = "http://ergast.com/downloads/f1db.sql.gz"
status_file = os.path.join(os.path.dirname(
    __file__), "../data/version.json")
target_file = os.path.join(os.path.dirname(
    __file__), "../data/ergast_f1db.sql.gz")

pathlib.Path(os.path.join(os.path.dirname(__file__), "../data/")
             ).mkdir(parents=True, exist_ok=True)

try:
    with open(status_file) as f:
        status = json.load(f)
except:
    status = {
        "last-modified": "Sun, 20 Jun 2021 16:24:25 GMT",
        "size": 0
    }

resp = requests.head(url)
lastmod = resp.headers['Last-Modified']

lastmod_date = parser.parse(lastmod)
status_lastmod_date = parser.parse(status['last-modified'])

size = int(resp.headers['Content-Length'])
status_size = status['size']


if (lastmod_date > status_lastmod_date or size != status_size):
    print('Getting new ergast db')
    try:
        os.remove(target_file)
    except:
        pass

    try:
        resp = requests.get(url, stream=True)
        with open(target_file, 'wb') as out_file:
            shutil.copyfileobj(resp.raw, out_file)

        # os.system('gunzip /tmp/f1db.sql.gz -f')
        # os.rename("/tmp/f1db.sql", target_file)

        status['size'] = size
        status['last-modified'] = lastmod
    except (RuntimeError, TypeError, NameError):
        pass
else:
    print('Already up to date, not refreshing')

with open(status_file, 'w') as outfile:
    json.dump(status, outfile)
