import unittest

from nemusicapi.api import Api

api = Api()


class TestApi(unittest.TestCase):
    def test_get_song_data(self):
        res = api.get_song_data('Dear Moments', limit=1)
        self.assertEqual(res, {1487339803: 'Dear Moments'})


if __name__ == '__main__':
    unittest.main()