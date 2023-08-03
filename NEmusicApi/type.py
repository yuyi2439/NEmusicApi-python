from enum import Enum


class QualityLevel(Enum):
    """
    越靠下，音质越高
    """
    standard = 'standard'
    higher = 'higher'
    exhigh = 'exhigh'
    lossless = 'lossless'
    hires = 'hires'


class EncodeType(Enum):
    """
    越靠下文件越大，音质越好
    """
    mp3 = 'mp3'
    aac = 'aac'
    flac = 'flac'