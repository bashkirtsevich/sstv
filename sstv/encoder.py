import math
import typing
from itertools import chain

from PIL import Image

from .consts import *
from .modes.mode import ModeAbstract, ModeWide, ModeNarrow, ToneGenerator, Tone, Channel, LineSwitch
from .utils import SignalGen


class SSTVEncoder:
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate

    def encode(self, image, mode) -> SignalGen:
        spms = self.sample_rate / 1000
        offset = 0
        samples = 0
        factor = 2 * math.pi / self.sample_rate
        sample = 0

        generators = chain(
            self._encode_header(mode),
            self._encode_vis(mode),
            self._encode_image_data(image, mode),
        )

        for freq, sec in generators:
            samples += spms * sec * 1000
            tx = int(samples)
            freq_factor = freq * factor

            for sample in range(tx):
                # yield math.sin(math.fmod(sample * freq_factor + offset, 2 * math.pi))
                yield math.sin(sample * freq_factor + offset)

            offset += (sample + 1) * freq_factor
            samples -= tx

    @staticmethod
    def _yield_tones(tones) -> SignalGen:
        for tone in tones:
            yield (tone.freq, tone.time)

    def _encode_header(self, mode: typing.Type[ModeAbstract]) -> SignalGen:
        if issubclass(mode, ModeWide):
            header = HEADERS[ID_WIDE]
        elif issubclass(mode, ModeNarrow):
            header = HEADERS[ID_NARROW]
        else:
            raise TypeError("Unsupported mode")

        yield from self._yield_tones(header)

    def _encode_vis(self, mode) -> SignalGen:
        vis = mode.VIS_CODE

        if issubclass(mode, ModeWide):
            calibration = CALIBRATIONS[ID_WIDE]

            fsk_len = 16 if vis >= 0x100 else 8
            vis |= (vis.bit_count() & 1) << fsk_len - 1  # Parity bit

            vis_count = getattr(mode, "VIS_COUNT", 1)
            for _ in range(vis_count):
                yield from self._yield_tones(calibration)

                value = vis
                for _ in range(fsk_len):
                    yield (VIS_BIT_TONE_WIDE.freq[value & 1], VIS_BIT_TONE_WIDE.time)
                    value >>= 1

                yield (VIS_BIT_TONE_MEDIAN_WIDE.freq, VIS_BIT_TONE_MEDIAN_WIDE.time)

        elif issubclass(mode, ModeNarrow):
            calibration = CALIBRATIONS[ID_NARROW]
            yield from self._yield_tones(calibration)

            for part in [VIS_NARROW_PART1, VIS_NARROW_PART2, vis, vis ^ VIS_NARROW_PART1]:
                value = part
                for _ in range(6):
                    yield (VIS_BIT_TONE_NARROW.freq[value & 1], VIS_BIT_TONE_NARROW.time)
                    value >>= 1

        else:
            raise TypeError("Unsupported mode")

    def _encode_image_data(self, image, mode) -> SignalGen:
        height = mode.LINE_COUNT
        width = mode.LINE_WIDTH

        pixels = image.convert(mode.COLOR.mode_pil()).resize((width, height), Image.Resampling.LANCZOS).load()

        if mode.HAS_START_SYNC:
            if isinstance(mode.TONE_SYNC, list):
                for tone in mode.TIMING_SEQUENCE:
                    if isinstance(tone, ToneGenerator):
                        yield from tone

                    elif isinstance(tone, Tone):
                        yield (tone.freq, tone.time)
            else:
                yield (mode.TONE_SYNC.freq, mode.TONE_SYNC.time)

        y = 0
        while y < height:
            odd_line = y % 2

            for tone in mode.TIMING_SEQUENCE:
                if isinstance(tone, ToneGenerator):
                    yield from tone

                elif isinstance(tone, Tone):
                    if isinstance(freq := tone.freq, tuple):
                        freq = freq[odd_line]

                    yield (freq, tone.time)

                elif isinstance(tone, Channel):
                    for px in range(width):
                        pixel = pixels[px, y]
                        pixel = mode.COLOR.from_rgb(pixel)

                        if isinstance(_id := tone.id, tuple):
                            _id = _id[odd_line]

                        yield (mode.color_to_freq(pixel[_id]), tone.time)

                elif isinstance(tone, LineSwitch):
                    y += 1
            y += 1
