import json
import os
import random
import base64
import codecs

import requests
from Crypto.Cipher import AES
import urllib3

from nemusicapi.exception import NoDownloadDirException
from nemusicapi.type import QualityLevel, EncodeType


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def aes_encrypt(raw_text: str, raw_key: str):
    key = raw_key.encode('utf-8')  # 将密钥转换为utf-8格式
    iv = '0102030405060708'.encode('utf-8')  # iv偏移量
    encryptor = AES.new(key, AES.MODE_CBC, iv)  # 创建一个AES对象
    _text = raw_text.encode('utf-8')  # 将明文转换为utf-8格式
    pad = 16 - len(_text) % 16
    text = _text + (pad * chr(pad)).encode('utf-8')  # 明文需要转成二进制，且可以被16整除
    _encrypt_text = encryptor.encrypt(text)  # 加密
    encrypt_text = base64.b64encode(_encrypt_text)  # base64编码转换为byte字符串
    return encrypt_text.decode('utf-8')


def rsa_encrypt(raw_text: str, key: str, f: str):
    _text = raw_text[::-1]  # 随机字符串逆序排列
    text = bytes(_text, 'utf-8')  # 将随机字符串转换为byte类型的数据
    sec_key = int(codecs.encode(text, encoding='hex'), 16) ** int(key, 16) % int(f, 16)  # RSA加密
    return format(sec_key, 'x').zfill(256)  # RSA加密后字符串长度为256，不足的补x


def get_params(raw_params: str):
    random_str = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 16))
    encText = aes_encrypt(raw_params, '0CoJUm6Qyw8W8jud')
    params = aes_encrypt(encText, random_str)
    encSecKey = rsa_encrypt(random_str, '010001', '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7')  # RSA加密后获得encSecKey
    return params, encSecKey


class RawApi:
    def __init__(self, *,
                 cookie=''
                 ):
        self.cookie = cookie
        

    def _get_data(self, url: str, raw_params) -> dict:
        _params, encSecKey = get_params(json.dumps(raw_params))
        params = {
            "params": _params,
            "encSecKey": encSecKey
        }
        headers = {
            'Cookie': self.cookie
        }
        res = requests.post(url=url, params=params, headers=headers, verify=False)
        return res.json()


    def search_music(self, song_name: str, *, type=1, offset=0, total='true', limit=20):
        params = {
            'hlpretag': '<span class=\'s-fc7\'>',
            'hlposttag': '</span>',
            's': song_name,
            'type': type,
            'offset': offset,
            'total': total,
            'limit': limit
        }
        url = 'https://music.163.com/weapi/cloudsearch/get/web'
        res = self._get_data(url, params)
        return res
    
    def get_song_file_data(self, song_id: int, *, level: QualityLevel, encodeType: EncodeType):
        url = f'https://music.163.com/weapi/song/enhance/player/url/v1'
        params = {
            'ids': '["' + str(song_id) + '"]',
            'level': level.value,
            'encodeType': encodeType.value
        }
        res = self._get_data(url, params)
        return res


class Api(RawApi):
    def __init__(self, *, 
                 cookie='',
                 download_dir=None
                 ):
        super().__init__(cookie=cookie)
        self.download_dir = download_dir
        
        if download_dir:
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
    
    
    def refresh_song_data(self, raw_song_name: str) -> tuple[int, str] | None:
        res = self.search_music(raw_song_name)
        if res['result']['songCount'] == 0:
            return
        song_id = res['result']['songs'][0]['id']
        song_name = res['result']['songs'][0]['name']
        return song_id, song_name


    def get_song_download_data(self, song_id: int, *, level=QualityLevel.standard, encodeType=EncodeType.flac) -> tuple[str, str] | None:
        res = self.get_song_file_data(song_id, level=level, encodeType=encodeType)
        if res['data'][0]['url'] is None:
            return
        song_url = res['data'][0]['url']
        song_type = res['data'][0]['type']
        return song_url, song_type


    def download_song(self, song_url: str, file_name: str):
        if self.download_dir == None:
            raise NoDownloadDirException
        
        file_path = os.path.join(self.download_dir, file_name)
        
        with open(file_path, 'wb') as f:
            f.write(requests.get(song_url).content)
        return True