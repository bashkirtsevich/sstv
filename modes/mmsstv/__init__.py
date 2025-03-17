from .ml import MMSSTVML180
from .ml import MMSSTVML240
from .ml import MMSSTVML280
from .ml import MMSSTVML320
from .mp import MMSSTVMP115
from .mp import MMSSTVMP140
from .mp import MMSSTVMP175
from .mp import MMSSTVMP73
from .mr import MMSSTVMR115
from .mr import MMSSTVMR140
from .mr import MMSSTVMR175
from .mr import MMSSTVMR73
from .mr import MMSSTVMR90

__all__ = [
    "MMSSTVML180",
    "MMSSTVML240",
    "MMSSTVML280",
    "MMSSTVML320",

    "MMSSTVMP73",
    "MMSSTVMP115",
    "MMSSTVMP140",
    "MMSSTVMP175",

    "MMSSTVMR73",
    "MMSSTVMR90",
    "MMSSTVMR115",
    "MMSSTVMR140",
    "MMSSTVMR175",
]

# Narrow

# class MMSSTV73N(Mode):
#     NAME = "MMSSTV MP73-N"
#
#     VIS_CODE = 2
#     NARROW = True
#
#     COLOR = ColorScheme.YUV
#     LINE_WIDTH = 320
#     LINE_COUNT = 256
#     SCAN_TIME = 0.140000  # sec
#     SYNC_PULSE = 0.009000  # sec
#     SYNC_PORCH = 0.001500  # sec
#     SEP_PULSE = 0.001000  # sec
#
#     CHAN_COUNT = 3
#     CHAN_SYNC = 0
#     CHAN_TIME = SEP_PULSE + SCAN_TIME
#
#     CHAN_OFFSETS = [SYNC_PULSE + SYNC_PORCH + CHAN_TIME]
#     CHAN_OFFSETS.append(CHAN_OFFSETS[0] + CHAN_TIME)
#     CHAN_OFFSETS.append(SYNC_PULSE + SYNC_PORCH)
#
#     LINE_TIME = SYNC_PULSE + 3 * CHAN_TIME
#     PIXEL_TIME = SCAN_TIME / LINE_WIDTH
#     WINDOW_FACTOR = 2.48
#
#     TONE_SEP = Tone(1500, SEP_PULSE)
#     TONE_SYNC = Tone(1200, SYNC_PULSE)
#
#     TIMING_SEQUENCE = [
#         TONE_SYNC,
#         TONE_SEP,
#         Channel(0, PIXEL_TIME),
#         Channel(1, PIXEL_TIME),
#         Channel(2, PIXEL_TIME),
#         LineSwitch,
#         Channel(0, PIXEL_TIME),
#     ]
#
#     HAS_ODD_LINES = False
#     HAS_START_SYNC = False
#     HAS_HALF_SCAN = False
#     HAS_ALT_SCAN = False
