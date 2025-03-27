from .mode import ModeWide, ColorScheme, Channel, ModeMetaclass, ToneGenerator, SSTVGen, Tone


class AmigaGen(ToneGenerator):
    def __init__(self, sync: float):
        self.sync = sync

    def gen(self) -> SSTVGen:
        sd = 0x5fa0

        for _ in range(32):
            yield (1900, self.time)
            d = sd
            for _ in range(16):
                yield (1600 if d & 0x8000 else 2200, self.sync)
                d <<= 1

            sd = ((sd & 0xff00) - 0x0100) | ((sd & 0x00ff) + 0x0001)


class AmigaMeta(ModeMetaclass):
    def init_fields(cls):
        cls.CHAN_TIME = cls.SCAN_TIME

        cls.CHAN_OFFSETS = [0]
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[0] + cls.CHAN_TIME)
        cls.CHAN_OFFSETS.append(cls.CHAN_OFFSETS[1] + cls.CHAN_TIME)

        cls.LINE_TIME = cls.CHAN_COUNT * cls.CHAN_TIME
        cls.PIXEL_TIME = cls.SCAN_TIME / cls.LINE_WIDTH

        SYNC_PULSE = 0.0097646  # sec
        SYNC_PORCH = 0.00030514375  # sec

        cls.SYNC_PULSE = SYNC_PULSE * 32 * (16 + 1) + SYNC_PORCH  # sec

        cls.TONE_SYNC = [
            AmigaGen(SYNC_PULSE),
            Tone(0, SYNC_PORCH)
        ]

        cls.TIMING_SEQUENCE = [
            Channel(0, cls.PIXEL_TIME),
            Channel(1, cls.PIXEL_TIME),
            Channel(2, cls.PIXEL_TIME),
        ]


class Amiga90(ModeWide, metaclass=AmigaMeta):
    NAME = "Amiga Video Transceiver 90"

    VIS_CODE = 68
    VIS_COUNT = 3

    COLOR = ColorScheme.RGB
    LINE_WIDTH = 320
    LINE_COUNT = 240
    SCAN_TIME = 0.125000  # sec

    CHAN_COUNT = 3
    CHAN_SYNC = -1

    WINDOW_FACTOR = 20

    HAS_ODD_LINES = False
    HAS_START_SYNC = True
    HAS_HALF_SCAN = False
    HAS_ALT_SCAN = False
