from modes.mode import ModeMetaclass, Tone, Channel, LineSwitch, ModeWide, ColorScheme


class MMSSTVMPMeta(ModeMetaclass):
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


class MMSSTVMPAbstract(ModeWide):
    COLOR = ColorScheme.YUV
    LINE_WIDTH = 320
    LINE_COUNT = 256
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


class MMSSTVMP73(MMSSTVMPAbstract, metaclass=MMSSTVMPMeta):
    NAME = "MMSSTV MP73"
    VIS_CODE = 0x2523
    SCAN_TIME = 0.140000  # sec


class MMSSTVMP115(MMSSTVMPAbstract, metaclass=MMSSTVMPMeta):
    NAME = "MMSSTV MP115"
    VIS_CODE = 0x2923
    SCAN_TIME = 0.223000  # sec


class MMSSTVMP140(MMSSTVMPAbstract, metaclass=MMSSTVMPMeta):
    NAME = "MMSSTV MP140"
    VIS_CODE = 0x2a23
    SCAN_TIME = 0.270000  # sec


class MMSSTVMP175(MMSSTVMPAbstract, metaclass=MMSSTVMPMeta):
    NAME = "MMSSTV MP175"
    VIS_CODE = 0x2c23
    SCAN_TIME = 0.340000  # sec
