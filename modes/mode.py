import abc
import typing
from enum import Enum

# https://radio.clubs.etsit.upm.es/blog/2019-08-10-sstv-scottie1-encoder/

SSTVGen = typing.Generator[typing.Tuple[float, float], None, None]
Color = int
Pixel3 = typing.Tuple[Color, Color, Color]
Pixel = typing.Union[Color, Pixel3]

Tone = typing.NamedTuple("Tone", [("freq", typing.Union[int, typing.Tuple[int, int]]), ("time", float)])
Channel = typing.NamedTuple("Channel", [("id", typing.Union[int, typing.Tuple[int, int]]), ("time", float)])


class LineSwitch:
    pass


class ToneGenerator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def gen(self) -> SSTVGen:
        return None


# FSKGARD = 100
# FSKINTVAL = 22
# FSKSPACE = 2100

NARROW_SYNC = 1900
NARROW_LOW = 2044
NARROW_HIGH = 2300
NARROW_CENTE = ((NARROW_HIGH + NARROW_LOW) / 2)
NARROW_BW = (NARROW_HIGH - NARROW_LOW)
NARROW_BWH = (NARROW_BW / 2)
NARROW_BPFLO = 1600
NARROW_BPFHIG = 2500
NARROW_AFCLO = 1800
NARROW_AFCHIG = 1950


class ColorScheme(Enum):
    RGB = "RGB"
    GBR = "GBR"
    YUV = "YUV"
    BW = "BW"

    def mode_pil(self) -> str:
        match self:
            case self.RGB | self.GBR:
                return "RGB"
            case self.YUV:
                return "YCbCr"
            case self.BW:
                return "L"
            case _:
                raise NotImplemented

    def to_rbg(self, pixel: Pixel) -> Pixel:
        match self:
            case self.GBR:
                return (pixel[2], pixel[0], pixel[1])
            case self.RGB:
                return (pixel[0], pixel[1], pixel[2])
            case self.YUV:
                return (pixel[0], pixel[2], pixel[1])
            case self.BW:
                return (pixel, pixel, pixel)
            case _:
                raise NotImplemented

    def from_rgb(self, pixel: Pixel) -> Pixel:
        match self:
            case self.GBR:
                return (pixel[1], pixel[2], pixel[0])
            case self.RGB:
                return (pixel[0], pixel[1], pixel[2])
            case self.YUV:
                return (pixel[0], pixel[2], pixel[1])
            case self.BW:
                return (pixel, pixel, pixel)
            case _:
                raise NotImplemented


class ModeMetaclass(abc.ABCMeta):
    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        mcls.init_fields(cls)
        return cls

    def init_fields(cls):
        return None


class ModeAbstract(metaclass=ModeMetaclass):
    @staticmethod
    @abc.abstractmethod
    def color_to_freq(color: Color) -> float:
        return None


class ModeWide(ModeAbstract):
    @staticmethod
    def color_to_freq(color: Color) -> float:
        return color * (2300 - 1500) / 255 + 1500


class ModeNarrow(ModeAbstract):
    @staticmethod
    def color_to_freq(color: Color) -> float:
        return color * NARROW_BW / 255 + NARROW_LOW
