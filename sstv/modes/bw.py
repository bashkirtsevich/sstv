from .mode import ModeMetaclass, Tone, Channel, ModeWide, ColorScheme


class RobotBWMeta(ModeMetaclass):
    def init_fields(cls):
        cls.CHAN_TIME = cls.SCAN_TIME
        cls.CHAN_OFFSETS = [cls.SYNC_PULSE + cls.SYNC_PORCH]

        cls.LINE_TIME = cls.CHAN_OFFSETS[0] + cls.CHAN_TIME
        cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH

        cls.TIMING_SEQUENCE = [
            Tone(1200, cls.SYNC_PULSE),
            Tone(1500, cls.SYNC_PORCH),
            Channel(0, cls.PIXEL_TIME),
        ]


class RobotBWAbstract(ModeWide):
    COLOR = ColorScheme.BW
    LINE_WIDTH = 160
    LINE_COUNT = 120
    SYNC_PULSE = 0.006000
    SYNC_PORCH = 0.002000

    CHAN_COUNT = 1
    CHAN_SYNC = 0

    WINDOW_FACTOR = 5  # FIXME

    HAS_ODD_LINES = False
    HAS_START_SYNC = False
    HAS_HALF_SCAN = False
    HAS_ALT_SCAN = False


class RobotBW8(RobotBWAbstract, metaclass=RobotBWMeta):
    NAME = "Robot B&W 8"
    VIS_CODE = 2
    SCAN_TIME = 0.05889709


class RobotBW12(RobotBWAbstract, metaclass=RobotBWMeta):
    NAME = "Robot B&W 12"
    VIS_CODE = 390  # 6 FIXME: Because 6 has 3 bits and parity check fails
    SCAN_TIME = 0.0920
