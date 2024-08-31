import unittest

from nemusicapi.rawapi import RawApi
from nemusicapi.exception import NoSongNameErr

raw_api = RawApi()


class TestBaseApi(unittest.TestCase):
    def test_search_music(self):
        try:
            raw_api.search_music('', limit=1)
            self.assertTrue(False)
        except NoSongNameErr:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()