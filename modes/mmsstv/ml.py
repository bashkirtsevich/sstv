from modes.mmsstv.mr import MMSSTVMRMeta
from modes.mode import ModeWide, ColorScheme


class MMSSTVMLAbstract(ModeWide):
    COLOR = ColorScheme.YUV
    LINE_WIDTH = 640
    LINE_COUNT = 496
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


class MMSSTVML180(MMSSTVMLAbstract, metaclass=MMSSTVMRMeta):
    NAME = "MMSSTV ML180"
    VIS_CODE = 0x0523
    SCAN_TIME = 0.176500  # sec


class MMSSTVML240(MMSSTVMLAbstract, metaclass=MMSSTVMRMeta):
    NAME = "MMSSTV MP240"
    VIS_CODE = 0x0623
    SCAN_TIME = 0.236500  # sec


class MMSSTVML280(MMSSTVMLAbstract, metaclass=MMSSTVMRMeta):
    NAME = "MMSSTV MP280"
    VIS_CODE = 0x0923
    SCAN_TIME = 0.277500  # sec


class MMSSTVML320(MMSSTVMLAbstract, metaclass=MMSSTVMRMeta):
    NAME = "MMSSTV MP320"
    VIS_CODE = 0x0a23
    SCAN_TIME = 0.317500  # sec
