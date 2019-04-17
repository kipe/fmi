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
    radiation_global_accumulation = None
    radiation_long_wave_accumulation = None
    radiation_netsurface_long_wave_accumulation = None
    radiation_netsurface_short_wave_accumulation = None
    radiation_diffuse_accumulation = None

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
        self.radiation_global_accumulation = point.get(
            'radiation_global_accumulation', None)
        self.radiation_long_wave_accumulation = point.get(
            'radiation_long_wave_accumulation', None)
        self.radiation_netsurface_long_wave_accumulation = point.get(
            'radiation_netsurface_long_wave_accumulation', None)
        self.radiation_netsurface_short_wave_accumulation = point.get(
            'radiation_netsurface_short_wave_accumulation', None)
        self.radiation_diffuse_accumulation = point.get(
            'radiation_diffuse_accumulation', None)

    def __repr__(self):
        return '<Observation: %s - %.1f C>' % (
            self.time.isoformat(), self.temperature)

    @property
    def icon(self):
        if self.weather_symbol is None:
            return None

        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'symbols/%i.svg' % (self.weather_symbol))

    @property
    def icon_as_svg(self):
        icon = self.icon
        if icon is None:
            return None

        with open(icon, 'r') as f:
            data = f.read()
        return data

    def as_influx_measurement(self):
        return {
            'time': self.time,
            'fields': {
                key: value
                for key, value in self.__dict__.items()
                if key not in ['time'] and value is not None
            }
        }
