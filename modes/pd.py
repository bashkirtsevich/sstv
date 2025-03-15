from .mode import ModeWide, ColorScheme, Tone, Channel, ModeMetaclass, LineSwitch


class PDMeta(ModeMetaclass):
    def init_fields(cls):
        cls.CHAN_TIME = cls.SCAN_TIME + cls.SEP_PULSE

        cls.CHAN_OFFSETS = [cls.SYNC_PULSE + cls.SYNC_PORCH]
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[0] + cls.CHAN_TIME)
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[1] + cls.CHAN_TIME)
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[2] + cls.CHAN_TIME)

        cls.LINE_TIME = cls.SYNC_PULSE + cls.CHAN_COUNT * cls.CHAN_TIME
        cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH

        cls.TIMING_SEQUENCE = [
            Tone(1200, cls.SYNC_PULSE),
            Tone(1500, cls.SYNC_PORCH),
            Channel(0, cls.PIXEL_TIME),
            Channel(1, cls.PIXEL_TIME),
            Channel(2, cls.PIXEL_TIME),
            LineSwitch(),
            Channel(0, cls.PIXEL_TIME),
        ]


class PDAbstract(ModeWide):
    VIS_COUNT = 1

    COLOR = ColorScheme.YUV

    SYNC_PULSE = 0.009000  # sec
    SYNC_PORCH = 0.001000  # sec
    SEP_PULSE = 0.000100  # sec
    SEP_PORCH = 0.0

    CHAN_COUNT = 4
    CHAN_SYNC = 0

    WINDOW_FACTOR = 30  # FIXME

    HAS_ODD_LINES = True
    HAS_START_SYNC = False
    HAS_HALF_SCAN = False
    HAS_ALT_SCAN = False


class PD50(PDAbstract, metaclass=PDMeta):
    NAME = "PD50"
    VIS_CODE = 93
    LINE_WIDTH = 320
    LINE_COUNT = 256
    SCAN_TIME = 0.091520  # sec


class PD90(PD50):
    NAME = "PD90"
    VIS_CODE = 99
    SCAN_TIME = 0.170240  # sec


class PD120(PDAbstract, metaclass=PDMeta):
    NAME = "PD120"
    VIS_CODE = 95
    LINE_WIDTH = 640
    LINE_COUNT = 496
    SCAN_TIME = 0.121600  # sec


class PD160(PDAbstract, metaclass=PDMeta):
    NAME = "PD160"
    VIS_CODE = 98
    LINE_WIDTH = 512
    LINE_COUNT = 400
    SCAN_TIME = 0.195584  # sec


class PD180(PDAbstract, metaclass=PDMeta):
    NAME = "PD180"
    VIS_CODE = 96
    LINE_WIDTH = 640
    LINE_COUNT = 496
    SCAN_TIME = 0.183040  # sec


class PD240(PD180):
    NAME = "PD240"
    VIS_CODE = 97
    SCAN_TIME = 0.244480  # sec


class PD290(PDAbstract, metaclass=PDMeta):
    NAME = "PD290"
    VIS_CODE = 94
    LINE_WIDTH = 800
    LINE_COUNT = 616
    SCAN_TIME = 0.228800  # sec
