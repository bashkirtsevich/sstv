from .mode import ModeWide, ColorScheme, Tone, Channel, ModeMetaclass


class SC2Meta(ModeMetaclass):
    def init_fields(cls):
        cls.CHAN_TIME = cls.SCAN_TIME

        cls.CHAN_OFFSETS = [cls.SYNC_PULSE + cls.SYNC_PORCH]
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[0] + cls.CHAN_TIME)
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[1] + cls.CHAN_TIME)

        cls.LINE_TIME = cls.SYNC_PULSE + cls.CHAN_COUNT * cls.CHAN_TIME
        cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH

        cls.TIMING_SEQUENCE = [
            Tone(cls.FREQ_SYNC_PULSE, cls.SYNC_PULSE),
            Tone(cls.FREQ_SYNC_PORCH, cls.SYNC_PORCH),
            Channel(0, cls.PIXEL_TIME),
            Channel(1, cls.PIXEL_TIME),
            Channel(2, cls.PIXEL_TIME),
        ]


class SC2Abstract(ModeWide):
    COLOR = ColorScheme.RGB
    LINE_WIDTH = 320
    LINE_COUNT = 256
    SYNC_PORCH = 0.000500  # sec

    CHAN_COUNT = 3
    CHAN_SYNC = 0

    HAS_ODD_LINES = False
    HAS_START_SYNC = False
    HAS_HALF_SCAN = False
    HAS_ALT_SCAN = False


class SC2180(SC2Abstract, metaclass=SC2Meta):
    NAME = "SC2 180"
    VIS_CODE = 55
    SCAN_TIME = 0.235000  # sec
    SYNC_PULSE = 0.0055437  # sec
    WINDOW_FACTOR = 2.48


class SC2120(SC2Abstract, metaclass=SC2Meta):
    NAME = "SC2 120"
    VIS_CODE = 63
    SCAN_TIME = 0.1565  # sec
    SYNC_PULSE = 0.00552248  # sec
    WINDOW_FACTOR = 10


class SC260(SC2Abstract, metaclass=SC2Meta):
    NAME = "SC2 60"
    VIS_CODE = 59
    SCAN_TIME = 0.078128  # sec
    SYNC_PULSE = 0.0055006  # sec
    WINDOW_FACTOR = 10
