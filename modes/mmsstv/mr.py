from modes.mode import ModeMetaclass, Tone, Channel, ModeWide, ColorScheme


class MMSSTVMRMeta(ModeMetaclass):
    def init_fields(cls):
        cls.CHAN_TIME = cls.SCAN_TIME + cls.SEP_PULSE

        cls.HALF_SCAN_TIME = cls.SCAN_TIME / 2
        cls.HALF_CHAN_TIME = cls.SEP_PULSE + cls.HALF_SCAN_TIME

        cls.CHAN_OFFSETS = [cls.SYNC_PULSE + cls.SYNC_PORCH]
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[0] + cls.CHAN_TIME + cls.SEP_PORCH)
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[1] + cls.HALF_CHAN_TIME + cls.SEP_PORCH)

        cls.LINE_TIME = cls.CHAN_OFFSETS[2] + cls.HALF_SCAN_TIME
        cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH
        cls.HALF_PIXEL_TIME = cls.HALF_SCAN_TIME / cls.LINE_WIDTH

        cls.TIMING_SEQUENCE = [
            Tone(1200, cls.SYNC_PULSE),
            Tone(1500, cls.SYNC_PORCH),
            Channel(0, cls.PIXEL_TIME),
            Tone(0, cls.SEP_PULSE),  # FIXME: instead of 0 tone we should send previous pixel
            Channel(1, cls.HALF_PIXEL_TIME),
            Tone(0, cls.SEP_PULSE),
            Channel(2, cls.HALF_PIXEL_TIME),
            Tone(0, cls.SEP_PULSE),
        ]


class MMSSTVMRAbstract(ModeWide):
    VIS_COUNT = 1

    COLOR = ColorScheme.YUV
    LINE_WIDTH = 320
    LINE_COUNT = 256
    SYNC_PULSE = 0.009000  # sec
    SYNC_PORCH = 0.001000  # sec
    SEP_PULSE = 0.000100  # sec
    SEP_PORCH = 0.0

    CHAN_COUNT = 3
    CHAN_SYNC = 0

    WINDOW_FACTOR = 30  # FIXME

    HAS_ODD_LINES = False
    HAS_START_SYNC = False
    HAS_HALF_SCAN = True
    HAS_ALT_SCAN = False


class MMSSTVMR73(MMSSTVMRAbstract, metaclass=MMSSTVMRMeta):
    NAME = "MMSSTV MR73"

    VIS_CODE = 0x4523
    SCAN_TIME = 0.138000  # sec


class MMSSTVMR90(MMSSTVMRAbstract, metaclass=MMSSTVMRMeta):
    NAME = "MMSSTV MR90"
    VIS_CODE = 0x4623
    SCAN_TIME = 0.171000  # sec


class MMSSTVMR115(MMSSTVMRAbstract, metaclass=MMSSTVMRMeta):
    NAME = "MMSSTV MR115"
    VIS_CODE = 0x4923
    SCAN_TIME = 0.220000  # sec


class MMSSTVMR140(MMSSTVMRAbstract, metaclass=MMSSTVMRMeta):
    NAME = "MMSSTV MR140"
    VIS_CODE = 0x4a23
    SCAN_TIME = 0.269000  # sec


class MMSSTVMR175(MMSSTVMRAbstract, metaclass=MMSSTVMRMeta):
    NAME = "MMSSTV MR175"
    VIS_CODE = 0x4c23
    SCAN_TIME = 0.337000  # sec
