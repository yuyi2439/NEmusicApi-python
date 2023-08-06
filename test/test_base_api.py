import unittest

from nemusicapi.base_api import BaseApi
from nemusicapi.exception import NoSongNameException

api = BaseApi()


class TestBaseApi(unittest.TestCase):
    def test_search_music(self):
        try:
            api.search_music('', limit=1)
            self.assertTrue(False)
        except NoSongNameException:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()