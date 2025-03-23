import math
import typing
from itertools import chain

import numpy as np
from PIL import Image
from scipy.signal.windows import hann

from modes import WIDE_VIS_MAP, NARROW_VIS_MAP
from modes.mode import ColorScheme, Tone, Channel, LineSwitch, ModeWide, ModeNarrow, ToneGenerator
from utils import bit_to_int, barycentric_peak_interp

HDR_TONE_DURATION = 0.100000

VIS_WIDE_BIT_SIZE = 0.030000
VIS_NARROW_BIT_SIZE = 0.022000

Signal = typing.List[float]
SignalGen = typing.Generator[float, None, None]

HEADER_WIDE = [
    Tone(1900, 0.300000),
    Tone(1200, 0.010000),
    Tone(1900, 0.300000),
    Tone(1200, 0.030000),
]

HEADER_NARROW = [
    Tone(1900, 0.300000),
    Tone(2100, 0.100000),
    Tone(1900, 0.022000)
]

HEADERS = [HEADER_WIDE, HEADER_NARROW]


class SSTVDecoder:
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate

    def decode(self, signal: Signal) -> Image:
        if not (header := self._find_header(HEADERS, signal)):
            return None

        hdr_idx, hdr_start, hdr_len = header
        header_end = hdr_start + hdr_len

        match hdr_idx:
            case 0:
                decoder = self._decode_vis_wide
                bit_time = VIS_WIDE_BIT_SIZE
            case 1:
                decoder = self._decode_vis_narrow
                bit_time = VIS_NARROW_BIT_SIZE
            case _:
                raise ValueError("Unsupported header type")

        mode, bit_len = decoder(signal, header_end)

        # vis_len = VIS_BIT_SIZE * (bit_len + 1) * self.sample_rate
        vis_len = bit_time * bit_len * self.sample_rate

        vis_count = getattr(mode, "VIS_COUNT", 1)
        vis_end = hdr_start + (vis_len + hdr_len) * vis_count

        image_data = self._decode_image_data(signal, mode, round(vis_end))

        return self._draw_image(mode, image_data)

    def _peak_fft_freq(self, signal: Signal) -> float:
        windowed_data = signal * hann(len(signal))
        fft = np.abs(np.fft.rfft(windowed_data))

        # Get index of bin with the highest magnitude
        x = np.argmax(fft)
        # Interpolated peak frequency
        peak = barycentric_peak_interp(fft, x)

        # Return frequency in hz
        return peak * self.sample_rate / len(windowed_data)

    def _find_header(
            self,
            headers: typing.List[typing.Iterable[Tone]],
            signal: Signal,
            threshold: float = 50.0,
            stride_time: float = 0.002,
            window_size: float = 0.010
    ) -> typing.Optional[typing.Tuple[int, int, int]]:
        stride_len = round(stride_time * self.sample_rate)  # check every stride_time ms

        stamps = []
        for header in headers:
            hdr_size = round(sum(tone.time for tone in header) * self.sample_rate)
            # The margin of error created here will be negligible when decoding the
            # vis due to each bit having a length of 30ms. We fix this error margin
            # when decoding the image by aligning each sync pulse

            areas = []
            time_acc = 0
            for it in header:
                area = slice(
                    round(time_acc * self.sample_rate),
                    round((time_acc + window_size) * self.sample_rate)
                )
                areas.append((area, it.freq))
                time_acc += it.time

            stamps.append((hdr_size, areas))

        for curr_sample in range(0, len(signal), stride_len):
            for header_idx, (header_size, slices) in enumerate(stamps):
                if curr_sample + header_size >= len(signal):
                    continue

                # Update search progress message
                if curr_sample % (stride_len * 256) == 0:
                    progress = curr_sample / self.sample_rate
                    print(f"Searching for calibration header... {progress:.1f}s")

                search_area = signal[curr_sample:curr_sample + header_size]

                # Check they're the correct frequencies
                if all(abs(self._peak_fft_freq(search_area[part]) - freq) < threshold for part, freq in slices):
                    print("Searching for calibration header... Found!")
                    return header_idx, curr_sample, header_size

        print("Couldn't find SSTV header in the given audio file")
        return None

    def _decode_vis_value(self, vis_bits: typing.List[int]) -> typing.Tuple[int, int]:
        # Check for even parity in last bit
        for bit_len in (16, 8):
            # FIXME
            vis = vis_bits[:bit_len]
            if sum(vis) % 2:
                continue

            # LSB first so we must reverse and ignore the parity bit
            return bit_to_int(vis[:-1]), bit_len

        raise ValueError("Error decoding VIS header (invalid parity bit)")

    def _decode_vis_wide(self, signal: Signal, vis_start: int, bit_time: float = VIS_WIDE_BIT_SIZE) -> tuple:
        """Decodes the vis from the audio data and returns the SSTV mode"""

        bit_size = round(bit_time * self.sample_rate)
        vis_bits = []

        # FIXME: Read 8 and 16 bit vis at the same time
        for bit_idx in range(16):
            bit_offset = vis_start + bit_idx * bit_size
            section = signal[bit_offset:bit_offset + bit_size]
            freq = self._peak_fft_freq(section)
            # 1100 hz = 1, 1300hz = 0
            vis_bits.append(int(freq <= 1200))

        vis_value, bit_len = self._decode_vis_value(vis_bits)
        if mode := WIDE_VIS_MAP.get(vis_value):
            print("Detected SSTV mode {}".format(mode.NAME))
            return mode, bit_len

        error = "SSTV mode is unsupported (VIS: {})"
        raise ValueError(error.format(vis_value))

    def _decode_vis_narrow(self, signal: Signal, vis_start: int, bit_time: float = VIS_NARROW_BIT_SIZE) -> tuple:
        """Decodes the vis from the audio data and returns the SSTV mode"""
        bit_size = round(bit_time * self.sample_rate)
        vis_bits = []

        for bit_idx in range(4 * 6):
            bit_offset = vis_start + bit_idx * bit_size
            section = signal[bit_offset:bit_offset + bit_size]
            freq = self._peak_fft_freq(section)
            # 1900 hz = 1, 2100hz = 0
            vis_bits.append(int(freq <= 2000))

        vis1, vis2, vis_value, vis4 = (bit_to_int(vis_bits[g * 6:g * 6 + 6]) for g in range(4))

        if vis1 != 0x2d or vis2 != 0x15 or vis_value ^ vis2 != vis4:
            raise ValueError(f"Invalid VIS quadruplet ({vis1}, {vis2}, {vis_value}, {vis4})")

        if mode := NARROW_VIS_MAP.get(vis_value):
            print("Detected SSTV mode {}".format(mode.NAME))
            return mode, 24

        error = "SSTV mode is unsupported (VIS: {})"
        raise ValueError(error.format(vis_value))

    def _align_sync(self, signal: Signal, mode, align_start: int, start_of_sync: bool = True):
        """Returns sample where the beginning of the sync pulse was found"""

        # TODO - improve this

        sync_window = round(mode.SYNC_PULSE * 1.4 * self.sample_rate)
        align_stop = len(signal) - sync_window

        if align_stop <= align_start:
            return None  # Reached end of audio

        for current_sample in range(align_start, align_stop):
            search_section = signal[current_sample:current_sample + sync_window]

            if self._peak_fft_freq(search_section) > mode.FREQ_SYNC_MEDIAN:
                break

        end_sync = current_sample + sync_window // 2

        if start_of_sync:
            return end_sync - round(mode.SYNC_PULSE * self.sample_rate)
        else:
            return end_sync

    def _decode_image_data(self, signal: Signal, mode, image_start: int) -> typing.List[typing.List[typing.List[int]]]:
        window_factor = mode.WINDOW_FACTOR
        centre_window_time = (mode.PIXEL_TIME * window_factor) / 2
        pixel_window = round(centre_window_time * 2 * self.sample_rate)

        height = mode.LINE_COUNT
        channels = mode.CHAN_COUNT
        width = mode.LINE_WIDTH
        # Use list comprehension to init list so we can return data early
        image_data = [[[0 for i in range(width)] for j in range(channels)] for k in range(height)]

        seq_start = image_start
        if mode.HAS_START_SYNC:
            # Start at the end of the initial sync pulse
            seq_start = self._align_sync(signal, mode, seq_start, start_of_sync=False)
            if seq_start is None:
                raise EOFError("Reached end of audio before image data")

        for line in range(height):
            if mode.CHAN_SYNC == -1:
                seq_start += mode.LINE_TIME * self.sample_rate
            elif mode.CHAN_SYNC > 0 and line == 0:
                # Align seq_start to the beginning of the previous sync pulse
                sync_offset = mode.CHAN_OFFSETS[mode.CHAN_SYNC]
                seq_start -= round((sync_offset + mode.SCAN_TIME) * self.sample_rate)

            for chan in range(channels):
                if chan == mode.CHAN_SYNC:
                    if line > 0 or chan > 0:
                        # Set base offset to the next line
                        seq_start += round(mode.LINE_TIME * self.sample_rate)

                    # Align to start of sync pulse
                    seq_start = self._align_sync(signal, mode, seq_start)
                    if seq_start is None:
                        print("Reached end of audio whilst decoding.")
                        return image_data

                pixel_time = mode.PIXEL_TIME
                if mode.HAS_HALF_SCAN:
                    # Robot mode has half-length second/third scans
                    if chan > 0:
                        pixel_time = mode.HALF_PIXEL_TIME

                    centre_window_time = (pixel_time * window_factor) / 2
                    pixel_window = round(centre_window_time * 2 * self.sample_rate)

                for px in range(width):
                    chan_offset = mode.CHAN_OFFSETS[chan]

                    px_pos = round(seq_start + (chan_offset + px * pixel_time - centre_window_time) * self.sample_rate)
                    px_end = px_pos + pixel_window

                    # If we are performing fft past audio length, stop early
                    if px_end >= len(signal):
                        print("Reached end of audio whilst decoding.")
                        return image_data

                    pixel_area = signal[px_pos:px_end]
                    freq = self._peak_fft_freq(pixel_area)

                    image_data[line][chan][px] = mode.freq_to_color(freq)

        return image_data

    def _draw_image(self, mode, image_data: typing.List[typing.List[typing.List[int]]]) -> Image:
        if mode.COLOR == ColorScheme.YUV:
            col_mode = "YCbCr"
        else:
            col_mode = "RGB"

        odd_lines = mode.HAS_ODD_LINES
        width = mode.LINE_WIDTH
        height = mode.LINE_COUNT
        channels = mode.CHAN_COUNT

        image = Image.new(col_mode, (width, height))
        pixel_data = image.load()

        print("Drawing image data...")

        line = 0
        for y in range(height // (2 if odd_lines else 1)):
            odd_line = y % 2
            for x in range(width):
                if channels == 1:
                    pixel_data[x, line] = mode.COLOR.to_rbg(image_data[y][0][x])
                elif channels == 2:
                    if mode.HAS_ALT_SCAN:
                        if mode.COLOR == ColorScheme.YUV:  # FIXME
                            # R36
                            pixel_data[x, line] = (image_data[y][0][x],
                                                   image_data[y - (odd_line - 1)][1][x],
                                                   image_data[y - odd_line][1][x])

                elif channels == 3:
                    pixel_data[x, line] = mode.COLOR.to_rbg(
                        (image_data[y][0][x],
                         image_data[y][1][x],
                         image_data[y][2][x])
                    )

                elif channels == 4:
                    pixel_data[x, line] = mode.COLOR.to_rbg(
                        (image_data[y][0][x],
                         image_data[y][1][x],
                         image_data[y][2][x])
                    )

            if odd_lines:
                line += 1

                if channels == 4:
                    for x in range(width):
                        pixel = mode.COLOR.to_rbg(
                            (image_data[y][0][x],
                             image_data[y - 1][1][x],
                             image_data[y - 1][2][x])
                        )

                        pixel_data[x, line] = pixel

            line += 1

        if image.mode != "RGB":
            image = image.convert("RGB")

        print("...Done!")
        return image


class SSTVEncoder:
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate

    def encode(self, image, mode) -> Signal:
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

    def _encode_header(self, mode) -> SignalGen:
        if issubclass(mode, ModeWide):
            tones = [1900, 1500, 1900, 1500, 2300, 1500, 2300, 1500, ]
        elif issubclass(mode, ModeNarrow):
            tones = [1900, 2300, 1900, 2300, ]
        else:
            raise TypeError("Unsupported mode")

        for tone in tones:
            yield (tone, HDR_TONE_DURATION)

    def _encode_vis(self, mode) -> SignalGen:
        # if mode.NARROW:
        #     # fsk = FSK_IDS_NARROW[self.mode]
        #     #
        #     # self.write(1900, 300)
        #     # self.write(FSKSPACE, FSKGARD)
        #     # self.write(1900, FSKINTVAL)
        #     # self.write_fsk(0x2d)
        #     # self.write_fsk(0x15)
        #     # # FSK
        #     # self.write_fsk(fsk)
        #     # self.write_fsk(fsk ^ 0x15)
        #     pass
        # else:
        vis_count = getattr(mode, "VIS_COUNT", 1)
        for _ in range(vis_count):
            yield (1900, 0.3)
            yield (1200, 0.01)
            yield (1900, 0.3)
            yield (1200, 0.03)

            vis = mode.VIS_CODE
            fsk_len = 16 if vis >= 0x100 else 8
            vis |= (vis.bit_count() & 1) << fsk_len - 1  # Parity bit

            for _ in range(fsk_len):
                yield (1100 if vis & 1 else 1300, VIS_WIDE_BIT_SIZE)
                vis >>= 1

            yield (1200, VIS_WIDE_BIT_SIZE)

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
