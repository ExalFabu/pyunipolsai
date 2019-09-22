import unittest
import pyunipolsai
from secrets import CREDS, HEADERS, PLATE


class UnipolSai(unittest.TestCase):
    def test_login(self):
        uni = pyunipolsai.authenticate(CREDS, HEADERS)
        self.assertTrue(uni.is_authenticated)

    def test_position_request(self):
        uni = pyunipolsai.authenticate(CREDS, HEADERS)
        self.assertTrue(uni.is_authenticated)
        pos = uni.get_position(plate=PLATE, update=False)
        self.assertIsInstance(pos, pyunipolsai.PositionData)

    def test_position_update(self):
        uni = pyunipolsai.authenticate(CREDS, HEADERS)
        self.assertTrue(uni.is_authenticated)
        old_pos = uni.get_position(plate=PLATE, update=False)
        pos = uni.get_position(plate=PLATE, update=True)
        self.assertIsInstance(pos, pyunipolsai.PositionData)
        self.assertNotEqual(old_pos.unix_timestamp, pos.unix_timestamp)


class PositionData(unittest.TestCase):
    def test_init(self):
        pd = pyunipolsai.utils.PositionData(unix_timestamp=156890938000, timezone=3600,
                                            dst=3600, lat=38.17301, lon=13.160862, address='Via Iccara',
                                            zipcode=90044)
        self.assertIsNotNone(pd)
        print(pd.as_dict())
        self.assertIsInstance(pd.as_dict(), dict)


if __name__ == '__main__':
    unittest.main(exit=False)
