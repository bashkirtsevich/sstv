from .mode import ModeWide, ColorScheme, Tone, Channel, ModeMetaclass


class MartinMeta(ModeMetaclass):
    def init_fields(cls):
        cls.CHAN_TIME = cls.SEP_PULSE + cls.SCAN_TIME

        cls.CHAN_OFFSETS = [cls.SYNC_PULSE + cls.SYNC_PORCH]
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[0] + cls.CHAN_TIME)
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[1] + cls.CHAN_TIME)

        cls.LINE_TIME = cls.SYNC_PULSE + cls.SYNC_PORCH + 3 * cls.CHAN_TIME
        cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH

        cls.TONE_SYNC = Tone(cls.FREQ_SYNC_PULSE, cls.SYNC_PULSE)
        cls.TONE_SEP = Tone(1500, cls.SEP_PULSE)

        cls.TIMING_SEQUENCE = [
            cls.TONE_SYNC,
            cls.TONE_SEP,
            Channel(0, cls.PIXEL_TIME),
            cls.TONE_SEP,
            Channel(1, cls.PIXEL_TIME),
            cls.TONE_SEP,
            Channel(2, cls.PIXEL_TIME),
            cls.TONE_SEP,
        ]


class MartinAbstract(ModeWide):
    COLOR = ColorScheme.GBR
    LINE_WIDTH = 320
    LINE_COUNT = 256
    SYNC_PULSE = 0.004862
    SYNC_PORCH = 0.000572
    SEP_PULSE = 0.000572

    CHAN_COUNT = 3
    CHAN_SYNC = 0

    HAS_ODD_LINES = False
    HAS_START_SYNC = False
    HAS_HALF_SCAN = False
    HAS_ALT_SCAN = False


class Martin1(MartinAbstract, metaclass=MartinMeta):
    NAME = "Martin 1"
    VIS_CODE = 44
    SCAN_TIME = 0.146432
    WINDOW_FACTOR = 2.34


class Martin2(MartinAbstract, metaclass=MartinMeta):
    NAME = "Martin 2"
    VIS_CODE = 40
    SCAN_TIME = 0.073216
    WINDOW_FACTOR = 4.68
