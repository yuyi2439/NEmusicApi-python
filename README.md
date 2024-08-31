# NEmusicApi

> 一个网易云音乐的Api框架

# 本项目年久失修，不建议使用

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

[demo.py](demo.py)

## 注意事项

- 创建api的时候，不输入`cookie`或者cookie对应的账号没有vip，都有可能导致获取信息不完整，需要自己测试
- 创建api的时候，不输入`download_dir`，在使用`download_song`方法的时候会raise异常
