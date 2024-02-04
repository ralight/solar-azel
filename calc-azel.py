#!/usr/bin/env python3

from pysolar.solar import *
import datetime
import json
import pytz
import time

# Pre-calculate azimuth and elevation values for a given location, at 1 minute intervals
# Takes a while!

# Replace the latitude and longitude with your desired location
latitude = 55.12356
longitude = -4.839700

st = datetime.date(2023, 1, 1)

interval = 1

start_stamp = int(time.mktime(st.timetuple()))

data = {}
data['az'] = {}
data['el'] = {}

for i in range(0, 365*24*60/interval):
    if i % 1000 == 0:
        print(i)
    ms = (start_stamp + i*60*interval)
    ts = datetime.datetime.fromtimestamp(ms)
    ts = ts.replace(tzinfo=pytz.timezone("Europe/London"))
    azimuth = get_azimuth(latitude, longitude, ts)
    elevation = get_altitude(latitude, longitude, ts)

    data['az'][ms] = azimuth
    data['el'][ms] = elevation

with open("data-azel.json", "w") as f:
    f.write(json.dumps(data))
