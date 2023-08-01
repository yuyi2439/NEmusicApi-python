import json
import random
import base64
import codecs

import requests
from Crypto.Cipher import AES
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def aes_encrypt(text, key):
    iv = '0102030405060708'.encode('utf-8')  # iv偏移量
    text = text.encode('utf-8')  # 将明文转换为utf-8格式
    pad = 16 - len(text) % 16
    text = text + (pad * chr(pad)).encode('utf-8')  # 明文需要转成二进制，且可以被16整除
    key = key.encode('utf-8')  # 将密钥转换为utf-8格式
    encryptor = AES.new(key, AES.MODE_CBC, iv)  # 创建一个AES对象
    encrypt_text = encryptor.encrypt(text)  # 加密
    encrypt_text = base64.b64encode(encrypt_text)  # base4编码转换为byte字符串
    return encrypt_text.decode('utf-8')


# RSA加密获得encSeckey
def rsa_encrypt(str, key, f):
    str = str[::-1]  # 随机字符串逆序排列
    str = bytes(str, 'utf-8')  # 将随机字符串转换为byte类型的数据
    sec_key = int(codecs.encode(str, encoding='hex'), 16) ** int(key, 16) % int(f, 16)  # RSA加密
    return format(sec_key, 'x').zfill(256)  # RSA加密后字符串长度为256，不足的补x


def get_params(raw_params: str):
    random_str = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 16))
    encText = aes_encrypt(raw_params, '0CoJUm6Qyw8W8jud')
    params = aes_encrypt(encText, random_str)
    encSecKey = rsa_encrypt(random_str, '010001', '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7')  # RSA加密后获得encSecKey
    return params, encSecKey


class Api:
    def __init__(self, cookie=''):
        self.cookie = cookie

    def get_data(self, url: str, raw_params) -> dict:
        params, encSecKey = get_params(json.dumps(raw_params))
        _params = {
            "params": params,
            "encSecKey": encSecKey
        }
        headers = {
            'Cookie': self.cookie
        }
        res = requests.post(url=url, params=_params, headers=headers, verify=False)    # 向服务器发送请求
        return res.json()  # 返回结果


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
        res = self.get_data(url, params)
        return res
    
    def get_song_url(self, song_id: int, *, level='standard', encodeType='flac'):
        """
        level: standard标准 higher较高 exhigh极高 lossless无损 hires
        encodeType: aac flac
        """
        url = f'https://music.163.com/weapi/song/enhance/player/url/v1'
        params = {
            'ids': '["' + str(song_id) + '"]',
            'level': level,
            'encodeType': encodeType
        }
        res = self.get_data(url, params)
        return res
