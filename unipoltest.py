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

if __name__ == '__main__':
    unittest.main(exit=False)
