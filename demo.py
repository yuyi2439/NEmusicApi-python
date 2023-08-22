import os
from NEmusicApi import Api, QualityLevel

download_dir = './download'
cookie = '这里输入cookie'

api = Api(cookie=cookie, download_dir=download_dir)


def main(raw_song_name: str):
    res = api.get_song_data(raw_song_name, limit=1)
    if res is None:
        return
    song_id = list(res.keys())[0]
    song_name = list(res.values())[0]
    
    level = QualityLevel.hires
    res = api.get_song_download_data(song_id, level=level)
    if res is None:
        return
    song_url, song_type = res
    
    file_name = f'{song_name}_{level.value}.{song_type.value}'
    if not os.path.exists(os.path.join(download_dir, file_name)):
        api.download_song(song_url, file_name)


if __name__ == '__main__':
    main('这里输入歌曲名')