import unittest
from datetime import datetime
from dateutil.tz import tzutc
from fmi import FMI


class TestForecast(unittest.TestCase):
    def test_lappeenranta(self):
        f = FMI(place='Lappeenranta')
        for point in f.forecast():
            assert point.time > datetime.now(tz=tzutc())
            assert isinstance(point.temperature, float)

        f = FMI(coordinates='%.03f,%.03f' % (61.058876, 28.186262))
        for point in f.forecast():
            assert point.time > datetime.now(tz=tzutc())
            assert isinstance(point.temperature, float)
