from modes.mode import ModeMetaclass, Tone, Channel, LineSwitch, ColorScheme, ModeNarrow


class MMSSTVMPNMeta(ModeMetaclass):
    def init_fields(cls):
        cls.CHAN_TIME = cls.SCAN_TIME

        cls.CHAN_OFFSETS = [cls.SYNC_PULSE + cls.SYNC_PORCH]
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[0] + cls.CHAN_TIME)
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[1] + cls.CHAN_TIME)
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[2] + cls.CHAN_TIME)

        cls.LINE_TIME = cls.SYNC_PULSE + cls.SYNC_PORCH * 4 + cls.CHAN_COUNT * cls.CHAN_TIME
        cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH

        cls.TIMING_SEQUENCE = [
            Tone(1200, cls.SYNC_PULSE),
            Tone(2044, cls.SYNC_PORCH),
            Channel(0, cls.PIXEL_TIME),
            Channel(1, cls.PIXEL_TIME),
            Channel(2, cls.PIXEL_TIME),
            LineSwitch(),
            Channel(0, cls.PIXEL_TIME),
        ]


class MMSSTVMPNAbstract(ModeNarrow):
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


class MMSSTVMPN73(MMSSTVMPNAbstract, metaclass=MMSSTVMPNMeta):
    NAME = "MMSSTV MP73-N"
    VIS_CODE = 2
    SCAN_TIME = 0.140000  # sec


class MMSSTVMPN110(MMSSTVMPNAbstract, metaclass=MMSSTVMPNMeta):
    NAME = "MMSSTV MP110-N"
    VIS_CODE = 4
    SCAN_TIME = 0.212000  # sec


class MMSSTVMPN140(MMSSTVMPNAbstract, metaclass=MMSSTVMPNMeta):
    NAME = "MMSSTV MP140-N"
    VIS_CODE = 5
    SCAN_TIME = 0.270000  # sec
