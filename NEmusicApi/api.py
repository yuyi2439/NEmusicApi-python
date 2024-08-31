import os

import requests
import urllib3

from .type import QualityLevel, EncodeType
from .rawapi import RawApi
from .exception import NoDownloadDirErr, SongIdErrorErr

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Api(RawApi):
    def __init__(
        self, *,
        cookie='',
        download_dir: str = ''
    ):
        super().__init__(cookie=cookie)
        self.download_dir = download_dir

        if download_dir:
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

    def get_song_data(
        self, raw_song_name: str, *,
        limit: int = 10
    ) -> dict[int, str] | None:
        res = self.search_music(raw_song_name, limit=limit)
        if res['result']['songCount'] == 0:
            return
        song_data = {}
        for j in res['result']['songs']:
            song_id = j['id']
            song_name = j['name']
            song_data[song_id] = song_name
        return song_data

    def get_song_download_data(
        self, song_id: int, *,
        level=QualityLevel.standard,
        encodeType=EncodeType.flac
    ) -> tuple[str, EncodeType]:

        res = self.get_song_file_data(
            song_id,
            level=level,
            encodeType=encodeType
        )
        if res['data'][0]['url'] is None:
            raise SongIdErrorErr(f"Song {song_id} not found")
        song_url = res['data'][0]['url']
        song_type = res['data'][0]['type']
        return song_url, EncodeType(song_type)

    def download_song(
        self, song_url: str, file_name: str, *,
        download_dir: str = ''
    ):
        """
        如果没有设置`download_dir`，将使用创建api时设置的值
        """
        if download_dir == '':
            download_dir = self.download_dir

        if download_dir == '':
            raise NoDownloadDirErr

        file_path = os.path.join(download_dir, file_name)

        with open(file_path, 'wb') as f:
            f.write(requests.get(song_url).content)
