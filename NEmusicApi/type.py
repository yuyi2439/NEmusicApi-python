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
    aac文件小，flac音质好
    """
    aac = 'aac'
    flac = 'flac'