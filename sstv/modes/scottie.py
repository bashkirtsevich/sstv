from .mode import ModeWide, ColorScheme, Tone, Channel, ModeMetaclass


class ScottieMeta(ModeMetaclass):
    def init_fields(cls):
        cls.CHAN_TIME = cls.SEP_PULSE + cls.SCAN_TIME

        cls.CHAN_OFFSETS = [cls.SYNC_PULSE + cls.SYNC_PORCH + cls.CHAN_TIME]
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[0] + cls.CHAN_TIME)
        cls.CHAN_OFFSETS.append(cls.SYNC_PULSE + cls.SYNC_PORCH)

        cls.LINE_TIME = cls.SYNC_PULSE + 3 * cls.CHAN_TIME
        cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH

        cls.TONE_SEP = Tone(1500, cls.SEP_PULSE)
        cls.TONE_SYNC = Tone(cls.FREQ_SYNC_PULSE, cls.SYNC_PULSE)

        cls.TIMING_SEQUENCE = [
            cls.TONE_SEP,
            Channel(0, cls.PIXEL_TIME),
            cls.TONE_SEP,
            Channel(1, cls.PIXEL_TIME),
            cls.TONE_SYNC,
            cls.TONE_SEP,
            Channel(2, cls.PIXEL_TIME),
        ]


class ScottieAbstract(ModeWide):
    COLOR = ColorScheme.GBR
    LINE_WIDTH = 320
    LINE_COUNT = 256
    SYNC_PULSE = 0.009000  # sec
    SYNC_PORCH = 0.001500  # sec
    SEP_PULSE = 0.001500  # sec

    CHAN_COUNT = 3
    CHAN_SYNC = 2

    HAS_ODD_LINES = False
    HAS_START_SYNC = True
    HAS_HALF_SCAN = False
    HAS_ALT_SCAN = False


class Scottie1(ScottieAbstract, metaclass=ScottieMeta):
    NAME = "Scottie 1"
    VIS_CODE = 60
    SCAN_TIME = 0.138240  # sec
    WINDOW_FACTOR = 2.48


class Scottie2(ScottieAbstract, metaclass=ScottieMeta):
    NAME = "Scottie 2"
    VIS_CODE = 56
    SCAN_TIME = 0.088064  # sec
    WINDOW_FACTOR = 3.82


class ScottieDX(ScottieAbstract, metaclass=ScottieMeta):
    NAME = "Scottie DX"
    VIS_CODE = 76
    SCAN_TIME = 0.345600  # sec
    WINDOW_FACTOR = 0.98
