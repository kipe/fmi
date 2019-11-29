FMI weather observation and forecast fetcher [![Build Status](https://travis-ci.org/kipe/fmi.svg?branch=master)](https://travis-ci.org/kipe/fmi)
============================================

This library provides easy to use methods for fetching both observations and
forecast data from [Finnish Meteorological Institute (FMI)](https://en.ilmatieteenlaitos.fi/open-data).
Currently just a quick hack, as I needed this for a project.


Installation
-----
```
pip install fmi_weather
```

Usage
-----

The library usage is fairly simple:
```
from fmi import FMI
f = FMI(place='Lappeenranta')
# f.observations() returns a list of Observation -objects for the last X hours.
print(f.observations())
```

Another way to set the API key and place is by setting them in environment variables FMI_PLACE.
After setting the environment variables, you can use the library without "any" initialization:
```
from fmi import FMI
f = FMI()
# f.forecast() returns a list of Observation -objects (sorry, confusing, I know :P) for the next 36 hours
print(f.forecast())
```

Forecast icons
--------------

Thanks to [FMI](https://github.com/fmidev/opendata-resources),
SVG icons are also provided as part of the library.

The weather symbol information is only available for forecasts unfortunately,
so the `Observation.icon` -property is valid only for them.
`.icon` returns the SVG-file path and `.icon_as_svg` returns the content itself.
