# Solar generation by sun azimuth / elevation

Plot graphs of solar output based on the sun position. One minute interval
gives a really good plot. 60 minute interval gives plots that show a nice
analemma shape: https://en.wikipedia.org/wiki/Analemma

This is just for fun, so if you want to use it yourself it will require some
tweaking.

Original inspiration: https://twitter.com/pilgrimbeart/status/1753384808065966545

Other examples: https://fosstodon.org/@ralight/111870136515060827

```
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt

# Pre-calculate solar azimuth and elevation. This takes a while, but is useful
# if you want to experiment with different plots. Configure the latitude and
# longitude first, likewise the interval, which is 1 minute.
./calc-azel.py

# Plot! This will require modification to load your data.
./solar-azel.py
```
