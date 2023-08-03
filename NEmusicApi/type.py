from enum import Enum


class QualityLevel(Enum):
    standard = 'standard'
    higher = 'higher'
    exhigh = 'exhigh'
    lossless = 'lossless'
    hires = 'hires'


class EncodeType(Enum):
    aac = 'aac'
    flac = 'flac'