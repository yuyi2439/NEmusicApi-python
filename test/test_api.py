import unittest

from nemusicapi.api import Api
from nemusicapi.exception import NoSongNameErr

api = Api()


class TestApi(unittest.TestCase):
    def test_get_song_data(self):
        res = api.get_song_data('Dear Moments', limit=1)
        self.assertEqual(res, {1487339803: 'Dear Moments'})
    
    def test_download_song(self):
        try:
            api.download_song('', '')
            self.assertTrue(False)
        except NoSongNameErr:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()