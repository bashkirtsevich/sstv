from .mode import ModeWide, ColorScheme, Tone, Channel, ModeMetaclass


class PXMeta(ModeMetaclass):
    def init_fields(cls):
        cls.CHAN_TIME = cls.SCAN_TIME

        cls.CHAN_OFFSETS = [cls.SYNC_PULSE + cls.SYNC_PORCH]
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[0] + cls.CHAN_TIME)
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[1] + cls.CHAN_TIME)

        cls.LINE_TIME = cls.SYNC_PULSE + cls.CHAN_COUNT * cls.CHAN_TIME
        cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH

        cls.TIMING_SEQUENCE = [
            Tone(1200, cls.SYNC_PULSE),
            Tone(1500, cls.SYNC_PORCH),
            Channel(0, cls.PIXEL_TIME),
            Channel(1, cls.PIXEL_TIME),
            Channel(2, cls.PIXEL_TIME),
            Tone(1500, cls.SYNC_PORCH),
        ]


class PXAbstract(ModeWide):
    VIS_COUNT = 1

    COLOR = ColorScheme.RGB
    LINE_WIDTH = 640
    LINE_COUNT = 496

    CHAN_COUNT = 3
    CHAN_SYNC = 0

    HAS_ODD_LINES = False
    HAS_START_SYNC = False
    HAS_HALF_SCAN = False
    HAS_ALT_SCAN = False


class P3(PXAbstract, metaclass=PXMeta):
    NAME = "P3"
    VIS_CODE = 113
    SCAN_TIME = 0.133333  # sec
    SYNC_PULSE = 0.005208  # sec
    SYNC_PORCH = 0.001042  # sec
    WINDOW_FACTOR = 10


class P5(PXAbstract, metaclass=PXMeta):
    NAME = "P5"
    VIS_CODE = 114
    SCAN_TIME = 0.200000  # sec
    SYNC_PULSE = 0.007813  # sec
    SYNC_PORCH = 0.001562375  # sec
    WINDOW_FACTOR = 10


class P7(PXAbstract, metaclass=PXMeta):
    NAME = "P7"
    VIS_CODE = 115
    SCAN_TIME = 0.266667  # sec
    SYNC_PULSE = 0.010417  # sec
    SYNC_PORCH = 0.002083  # sec
    WINDOW_FACTOR = 10
