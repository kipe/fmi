# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, division, print_function
import os
from datetime import datetime
from dateutil.tz import tzutc
from dateutil.parser import parse as parse_dt


class Observation(object):
    time = datetime(1970, 1, 1, tzinfo=tzutc())
    temperature = None
    wind_speed = None
    wind_gust = None
    wind_direction = None
    humidity = None
    cloud_coverage = None
    pressure = None
    dew_point = None
    precipitation = None
    precipitation_1h = None
    weather_symbol = None

    def __init__(self, timestamp, point):
        self.time = parse_dt(timestamp)
        self.temperature = point.get('temperature', None)
        self.wind_speed = point.get('wind_speed', None)
        self.wind_gust = point.get('wind_gust', None)
        self.wind_direction = point.get('wind_direction', None)
        self.humidity = point.get('humidity', None)
        self.cloud_coverage = point.get('cloud_coverage', None)
        self.pressure = point.get('pressure', None)
        self.dew_point = point.get('dew_point', None)
        self.precipitation = point.get('precipitation', None)
        self.precipitation_1h = point.get('precipitation_1h', None)
        self.weather_symbol = int(point.get('weather_symbol', 0))

    @property
    def icon(self):
        if self.weather_symbol is None:
            return None

        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'symbols/%i.svg' % (self.weather_symbol))

    @property
    def icon_as_svg(self):
        icon = self.icon
        if icon is None:
            return None

        with open(icon, 'r') as f:
            data = f.read()
        return data
