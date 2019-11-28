import unittest
from datetime import datetime
from dateutil.tz import tzutc
from fmi import FMI


class TestObservations(unittest.TestCase):
    def test_lappeenranta(self):
        now = datetime.now(tz=tzutc())

        f = FMI(place='Lappeenranta')
        for point in f.observations():
            assert point.time < now
            assert isinstance(point.temperature, float)
