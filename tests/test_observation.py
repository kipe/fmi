import unittest
from datetime import datetime
from dateutil.tz import tzutc
from fmi import FMI


class TestObservations(unittest.TestCase):
    def test_lappeenranta(self):
        f = FMI(place='Lappeenranta')
        for point in f.observations():
            assert point.time < datetime.now(tz=tzutc())
            assert isinstance(point.temperature, float)

        for point in f.observations(fmisid=101237):
            assert point.time < datetime.now(tz=tzutc())
            assert isinstance(point.temperature, float)
