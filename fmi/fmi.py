import os
import requests
import warnings
from .observation import Observation, Forecast
from bs4 import BeautifulSoup


class FMI(object):
    api_endpoint = 'https://opendata.fmi.fi/wfs'

    def __init__(self, apikey=None, place=None, coordinates=None):
        self.place = os.environ.get('FMI_PLACE', place)
        self.coordinates = os.environ.get('FMI_COORDINATES', coordinates)
        if apikey is not None:
            warnings.simplefilter('default')
            warnings.warn('The use of FMI API key is deprecated.',
                          DeprecationWarning)

    def _parse_identifier(self, x):
        identifier = x['gml:id'].split('-')[-1].lower()
        if identifier in ['t2m', 'temperature']:
            return 'temperature', 1
        if identifier in ['ws_10min', 'windspeedms']:
            return 'wind_speed', 1
        if identifier in ['wg_10min', 'windgust']:
            return 'wind_gust', 1
        if identifier in ['wd_10min', 'winddirection']:
            return 'wind_direction', 1
        if identifier in ['r_1h', 'precipitation1h']:
            return 'precipitation_1h', 1
        if identifier in ['ri_10min', 'precipitationamount']:
            return 'precipitation', 1
        if identifier in ['rh', 'humidity']:
            return 'humidity', 1
        if identifier in ['n_man', 'totalcloudcover']:
            return 'cloud_coverage', 12.5 if identifier == 'n_man' else 1
        if identifier in ['p_sea', 'pressure']:
            return 'pressure', 1
        if identifier in ['td', 'dewpoint']:
            return 'dew_point', 1
        if identifier in ['weathersymbol3']:
            return 'weather_symbol', 1
        if identifier in ['radiationglobalaccumulation']:
            return 'radiation_global_accumulation', 1
        if identifier in ['radiationlwaccumulation']:
            return 'radiation_long_wave_accumulation', 1
        if identifier in ['radiationnetsurfacelwaccumulation']:
            return 'radiation_netsurface_long_wave_accumulation', 1
        if identifier in ['radiationnetsurfaceswaccumulation']:
            return 'radiation_netsurface_short_wave_accumulation', 1
        if identifier in ['radiationdiffuseaccumulation']:
            return 'radiation_diffuse_accumulation', 1
        return None, 1

    def _parse_response(self, r, klass=Observation):
        bs = BeautifulSoup(r.text, 'html.parser')

        d = {}
        # Loop over all measurement timeseries
        for mts in bs.find_all('wml2:measurementtimeseries'):
            # Try to parse identifier as "human readable",
            # get multiplier also (mainly for cloud coverage)
            identifier, multiplier = self._parse_identifier(mts)
            if identifier is None:
                continue

            # Loop through all the measurement points
            for p in mts.find_all('wml2:point'):
                # Find timestamp
                timestamp = p.find('wml2:time').text
                # Find value and multiply if by multiplier
                # given in _parse_identifier()
                value = float(p.find('wml2:value').text) * multiplier

                # If timestamp isn't already initialized,
                # initialize as dictionary
                if timestamp not in d.keys():
                    d[timestamp] = {}

                d[timestamp][identifier] = value

        return sorted(
            [klass(k, v) for k, v in d.items()],
            key=lambda x: x.time)

    def get(self, storedquery_id, klass=Observation, **params):
        query_params = {
            'request': 'getFeature',
            'storedquery_id': storedquery_id,
        }
        if self.place is not None:
            query_params['place'] = self.place
        elif self.coordinates is not None:
            query_params['latlon'] = self.coordinates
        query_params.update(params)

        request = requests.get(self.api_endpoint, params=query_params)
        request.raise_for_status()

        return self._parse_response(request, klass=klass)

    def observations(self, **params):
        return self.get(
            'fmi::observations::weather::timevaluepair',
            maxlocations=1,
            **params)

    def forecast(self, model='hirlam', **params):
        if model not in ['hirlam', 'harmonie']:
            raise ValueError('model must be one of "hirlam", "harmonie"')
        return self.get(
            'fmi::forecast::%s::surface::point::timevaluepair' % (model),
            maxlocations=1,
            klass=Forecast,
            **params)

    @staticmethod
    def fetch_stations():
        response = requests.get('https://cdn.fmi.fi/weather-observations/metadata/all-finnish-observation-stations.fi.json')  # noqa: E501
        response.raise_for_status()
        return [
            {
                'fmisid': station.get('fmisid', None),
                'wmo': station.get('wmo', None),
                'name': station.get('name', ''),
                'latitude': station.get('y', None),
                'longitude': station.get('x', None),
                'height': station.get('z', None),
                'started': station.get('started', 1900),
                'groups': [
                    x.strip()
                    for x in station.get('groups', '').split(',')
                ],
            }
            for station in response.json().get('items', [])
            if station['ended'] is None
        ]
