# NeteaseMusicApi
### 一个网易云音乐的Api

### 本项目使用Apache2.0开源协议
- 使用本项目时要求保留原始版权和许可声明。同时向贡献者明确授予专利权。
- 使用者可以自由修改，进行商业使用，可以使用不同的条款分发，没有开源要求。

## 项目介绍
本项目基于网易云音乐API，实现了部分网易云音乐的功能，包括但不限于：

- 搜索歌曲
- 获取歌曲详情
- 获取歌曲url
- 下载歌曲


## ~~食用~~使用教程
1. 使用pip安装 `pip install nemusicapi`
2. 导入包，创建api
    ```python
    from NEmusicApi import Api
    api = Api()
    ```
3. 然后就可以愉快的使用了

## 举个~~栗子~~例子
```python
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
```

## 注意事项
- 创建api的时候，不输入`cookie`或者cookie对应的账号没有vip，都有可能导致获取信息不完整，需要自己测试
- 创建api的时候，不输入`download_dir`，在使用`download_song`方法的时候会raise异常

## 单元测试
1. `poetry run python .\test\test_api.py`
2. `poetry run python .\test\test_base_api.py`