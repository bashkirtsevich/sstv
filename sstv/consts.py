import statistics

from .modes.mode import Tone

ID_WIDE = 0
ID_NARROW = 1

HEADER_WIDE = [
    Tone(1900, 0.100000),
    Tone(1500, 0.100000),
    Tone(1900, 0.100000),
    Tone(1500, 0.100000),
    Tone(2300, 0.100000),
    Tone(1500, 0.100000),
    Tone(2300, 0.100000),
    Tone(1500, 0.100000),
]

HEADER_NARROW = [
    Tone(1900, 0.100000),
    Tone(2300, 0.100000),
    Tone(1900, 0.100000),
    Tone(2300, 0.100000),
]

HEADERS = {
    ID_WIDE: HEADER_WIDE,
    ID_NARROW: HEADER_NARROW,
}

BIT_1_WIDE_FREQ = 1100
BIT_0_WIDE_FREQ = 1300

VIS_WIDE_BIT_SIZE = 0.030000
VIS_BIT_TONE_WIDE = Tone((BIT_0_WIDE_FREQ, BIT_1_WIDE_FREQ), VIS_WIDE_BIT_SIZE)
VIS_BIT_TONE_MEDIAN_WIDE = Tone(statistics.median([BIT_0_WIDE_FREQ, BIT_1_WIDE_FREQ]), VIS_WIDE_BIT_SIZE)

BIT_1_NARROW_FREQ = 1900
BIT_0_NARROW_FREQ = 2100

VIS_NARROW_BIT_SIZE = 0.022000
VIS_BIT_TONE_NARROW = Tone((BIT_0_NARROW_FREQ, BIT_1_NARROW_FREQ), VIS_NARROW_BIT_SIZE)
VIS_BIT_TONE_MEDIAN_NARROW = Tone(statistics.median([BIT_0_NARROW_FREQ, BIT_1_NARROW_FREQ]), VIS_NARROW_BIT_SIZE)
VIS_NARROW_PART1 = 0x2d
VIS_NARROW_PART2 = 0x15

CALIBRATION_WIDE = [
    Tone(1900, 0.300000),
    Tone(1200, 0.010000),
    Tone(1900, 0.300000),
    Tone(1200, 0.030000),
]

CALIBRATION_NARROW = [
    Tone(1900, 0.300000),
    Tone(2100, 0.100000),
    Tone(1900, 0.022000)
]

CALIBRATIONS = {
    ID_WIDE: CALIBRATION_WIDE,
    ID_NARROW: CALIBRATION_NARROW,
}
