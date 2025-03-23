from modes.mode import ModeMetaclass, Tone, Channel, ColorScheme, ModeNarrow


class MMSSTVMCNMeta(ModeMetaclass):
    def init_fields(cls):
        cls.CHAN_TIME = cls.SCAN_TIME

        cls.CHAN_OFFSETS = [cls.SYNC_PULSE + cls.SYNC_PORCH]
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[0] + cls.CHAN_TIME)
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[1] + cls.CHAN_TIME)

        cls.LINE_TIME = cls.SYNC_PULSE + cls.SYNC_PORCH * 5.8 + cls.CHAN_COUNT * cls.CHAN_TIME
        cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH

        cls.TIMING_SEQUENCE = [
            Tone(1900, cls.SYNC_PULSE),
            Tone(2044, cls.SYNC_PORCH),
            Channel(0, cls.PIXEL_TIME),
            Channel(1, cls.PIXEL_TIME),
            Channel(2, cls.PIXEL_TIME),
        ]


class MMSSTVMCNAbstract(ModeNarrow):
    COLOR = ColorScheme.RGB
    LINE_WIDTH = 320
    LINE_COUNT = 256
    SYNC_PULSE = 0.008000  # sec
    SYNC_PORCH = 0.000500  # sec

    CHAN_COUNT = 3
    CHAN_SYNC = 0

    WINDOW_FACTOR = 30  # FIXME

    HAS_ODD_LINES = False
    HAS_START_SYNC = False
    HAS_HALF_SCAN = False
    HAS_ALT_SCAN = False


class MMSSTVMCN110(MMSSTVMCNAbstract, metaclass=MMSSTVMCNMeta):
    NAME = "MMSSTV MC110-N"
    VIS_CODE = 0x14
    SCAN_TIME = 0.140000  # sec


class MMSSTVMCN140(MMSSTVMCNAbstract, metaclass=MMSSTVMCNMeta):
    NAME = "MMSSTV MC140-N"
    VIS_CODE = 0x15
    SCAN_TIME = 0.180000  # sec


class MMSSTVMCN180(MMSSTVMCNAbstract, metaclass=MMSSTVMCNMeta):
    NAME = "MMSSTV MC180-N"
    VIS_CODE = 0x16
    SCAN_TIME = 0.232000  # sec
