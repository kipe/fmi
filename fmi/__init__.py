# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, division, print_function
import requests
from fmi.observation import Observation
from bs4 import BeautifulSoup


class FMI(object):
    apikey = None
    api_endpoint = 'http://data.fmi.fi/fmi-apikey/{apikey}/wfs'

    def __init__(self, apikey, place):
        self.apikey = apikey
        self.place = place

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
            return 'relative_humidity', 1
        if identifier in ['n_man', 'totalcloudcover']:
            return 'cloud_coverage', 12.5 if identifier == 'n_man' else 1
        if identifier in ['p_sea', 'pressure']:
            return 'pressure', 1
        if identifier in ['td', 'dewpoint']:
            return 'dew_point', 1
        if identifier in ['weathersymbol3']:
            return 'weather_symbol', 1
        return None, 1

    def _parse_response(self, r):
        bs = BeautifulSoup(r.text)

        d = {}
        # Loop over all measurement timeseries
        for mts in bs.find_all('wml2:measurementtimeseries'):
            # Try to parse identifier as "human readable", get multiplier also (mainly for cloud coverage)
            identifier, multiplier = self._parse_identifier(mts)
            if identifier is None:
                continue

            # Loop through all the measurement points
            for p in mts.find_all('wml2:point'):
                # Find timestamp
                timestamp = p.find('wml2:time').text
                # Find value and multiply if by multiplier given in _parse_identifier()
                value = float(p.find('wml2:value').text) * multiplier

                # If timestamp isn't already initialized, initialize as dictionary
                if timestamp not in d.keys():
                    d[timestamp] = {}

                d[timestamp][identifier] = value

        return sorted([Observation(k, v) for k, v in d.items()], key=lambda x: x.time)

    def get(self, storedquery_id, **params):
        query_params = {
            'place': self.place,
            'request': 'getFeature',
            'storedquery_id': storedquery_id,
        }
        query_params.update(params)

        return self._parse_response(requests.get(self.api_endpoint.format(apikey=self.apikey), params=query_params))

    def observations(self):
        return self.get('fmi::observations::weather::timevaluepair', maxlocations=1)

    def forecast(self):
        return self.get('fmi::forecast::hirlam::surface::point::timevaluepair', maxlocations=1)
