import unittest
from datetime import datetime

from dateutil.tz import tzutc

from fmi import FMI


class TestForecast(unittest.TestCase):
    def test_lappeenranta(self):
        f = FMI(place="Lappeenranta")
        for point in f.forecast():
            assert point.time > datetime.now(tz=tzutc())
            assert isinstance(point.temperature, float)

        f = FMI(coordinates=f"{61.058876:.3f},{28.186262:.3f}")
        for point in f.forecast():
            assert point.time > datetime.now(tz=tzutc())
            assert isinstance(point.temperature, float)
