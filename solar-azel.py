#!/usr/bin/env python3

from influxdb import InfluxDBClient
import datetime
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytz
import time

def scatter_gen(mins):
    global data

    x = []
    y = []
    v = []

    st = datetime.date(2023, 1, 1)
    ifclnt = InfluxDBClient('data.example.com', 8086, username='username', password='password', database='database')
    timespan = "time >= \'2023-01-01 00:00:00\' and time <= \'2023-12-31 23:59:59\'"
    q = 'select mean("p_pv1") from "solar" where %s GROUP BY time(%dm) fill(linear);' % (timespan, mins)
    q += 'select mean("p_pv1") from "solar" where %s GROUP BY time(%dm) fill(linear);'% (timespan, mins)

    stamp = int(time.mktime(st.timetuple()))
    rs = ifclnt.query(q)

    p_pv1 = list(rs[0].get_points())
    p_pv2 = list(rs[1].get_points())

    for i in range(0, len(p_pv1)):
        if i % 1000 == 0:
            print(i)
        ts = (stamp + 0*4*3600 + i*60*mins)
        azimuth = data['az'][str(ts)]
        elevation = data['el'][str(ts)]

        try:
            v1 = float(p_pv1[i]['mean'])
        except TypeError:
            v1 = 0
        try:
            v2 = float(p_pv2[i]['mean'])
        except TypeError:
            v2 = 0

        if v1+v2 <= 0 or elevation > 0:
            continue

        v.append(v1+v2)
        x.append(azimuth)
        y.append(elevation)

    return (x, y, v)


with open("data-azel.json", "r") as f:
    data = json.load(f)

matplotlib.use('Agg')

fig = plt.figure(num=1, figsize=(14,7.5))
(x, y, v) = scatter_gen(1)

sc = ((72./fig.dpi)**2)*4
plt.scatter(x, y, c=v, cmap='viridis', s=sc, marker="o")
plt.title("PV generation by azimuth and elevation, 2023")
plt.xlabel("Azimuth")
plt.ylabel("Elevation")

plt.colorbar(label="PV generation (W)")

plt.savefig("azel.png", format="png")
