from .mode import ModeWide, ColorScheme, Tone, Channel


def gen_sync(pulse):
    sd = 0x5fa0

    for _ in range(32):
        yield Tone(1900, pulse)
        d = sd
        for _ in range(16):
            yield Tone(1600 if d & 0x8000 else 2200, pulse)
            d <<= 1

        sd = ((sd & 0xff00) - 0x0100) | ((sd & 0x00ff) + 0x0001)


class Amiga90(ModeWide):
    NAME = "Amiga Video Transceiver 90"

    VIS_CODE = 68
    VIS_COUNT = 3

    COLOR = ColorScheme.RGB
    LINE_WIDTH = 320
    LINE_COUNT = 240
    SCAN_TIME = 0.125000  # sec
    SYNC_PULSE = 0.0097646  # sec
    SYNC_PORCH = 0.00030514375  # sec

    CHAN_COUNT = 3
    CHAN_SYNC = 0
    CHAN_TIME = SCAN_TIME

    CHAN_OFFSETS = [CHAN_TIME]
    CHAN_OFFSETS.append(CHAN_OFFSETS[0] + CHAN_TIME)
    CHAN_OFFSETS.append(CHAN_OFFSETS[1] + CHAN_TIME)

    LINE_TIME = 3 * CHAN_TIME
    PIXEL_TIME = SCAN_TIME / LINE_WIDTH
    WINDOW_FACTOR = 20

    TONE_SYNC = [
        *list(gen_sync(SYNC_PULSE)),
        Tone(0, SYNC_PORCH)
    ]

    TIMING_SEQUENCE = [
        Channel(0, PIXEL_TIME),
        Channel(1, PIXEL_TIME),
        Channel(2, PIXEL_TIME),
    ]

    HAS_ODD_LINES = False
    HAS_START_SYNC = True
    HAS_HALF_SCAN = False
    HAS_ALT_SCAN = False
