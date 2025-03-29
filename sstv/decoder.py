import typing

from PIL import Image

from .consts import *
from .modes import WIDE_VIS_MAP, NARROW_VIS_MAP
from .modes.mode import ColorScheme, Tone
from .utils import bits_to_int, peak_fft_freq, Signal, read_bits, tones_to_slices, match_frequencies


class SSTVDecoder:
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate

    def decode(self, signal: Signal) -> Image:
        if not (header := self._find_header(CALIBRATIONS, signal)):
            return None

        hdr_idx, hdr_start, hdr_len = header
        header_end = hdr_start + hdr_len

        if hdr_idx == ID_WIDE:
            decoder = self._decode_vis_wide
            bit_time = VIS_WIDE_BIT_SIZE

        elif hdr_idx == ID_NARROW:
            decoder = self._decode_vis_narrow
            bit_time = VIS_NARROW_BIT_SIZE

        else:
            raise ValueError("Unsupported header type")

        mode, bit_len = decoder(signal, header_end)

        if hdr_idx == ID_WIDE:
            bit_len += 1

        # vis_len = VIS_BIT_SIZE * (bit_len + 1) * self.sample_rate
        vis_len = bit_time * bit_len * self.sample_rate

        vis_count = getattr(mode, "VIS_COUNT", 1)
        vis_end = hdr_start + (vis_len + hdr_len) * vis_count

        image_data = self._decode_image_data(signal, mode, round(vis_end))

        return self._draw_image(mode, image_data)

    def _find_header(
            self,
            headers: typing.Mapping[int, typing.Iterable[Tone]],
            signal: Signal,
            threshold: float = 50.0,
            stride_time: float = 0.002,
            window_size: float = 0.010
    ) -> typing.Optional[typing.Tuple[int, int, int]]:
        stride_len = round(stride_time * self.sample_rate)  # check every stride_time ms

        stamps = {
            header_id: tones_to_slices(header, self.sample_rate, window_size)
            for header_id, header in headers.items()
        }

        for curr_sample in range(0, len(signal), stride_len):
            for header_id, (header_size, slices) in stamps.items():
                if curr_sample + header_size >= len(signal):
                    continue

                # Update search progress message
                if curr_sample % (stride_len * 256) == 0:
                    progress = curr_sample / self.sample_rate
                    print(f"Searching for calibration header... {progress:.1f}s")

                search_area = signal[curr_sample:curr_sample + header_size]

                if match_frequencies(search_area, slices, self.sample_rate, threshold=threshold):
                    print("Searching for calibration header... Found!")
                    return header_id, curr_sample, header_size

        print("Couldn't find SSTV header in the given audio file")
        return None

    def _decode_vis_wide(self, signal: Signal, vis_start: int, bit_time: float = VIS_WIDE_BIT_SIZE) -> tuple:
        """Decodes the vis from the audio data and returns the SSTV mode"""
        vis_bits = list(
            read_bits(
                signal, 16, bit_time,
                freq_true=BIT_1_WIDE_FREQ, freq_false=BIT_0_WIDE_FREQ,
                sample_rate=self.sample_rate, offset=vis_start
            )
        )

        # Check for even parity in last bit
        for bit_len in (16, 8):
            # FIXME
            vis = vis_bits[:bit_len]
            if sum(vis) % 2:
                continue

            # LSB first so we must reverse and ignore the parity bit
            vis_value = bits_to_int(vis[:-1])
            if mode := WIDE_VIS_MAP.get(vis_value):
                print(f"Detected SSTV mode {mode.NAME}")
                return mode, bit_len

            raise ValueError(f"SSTV mode is unsupported (VIS: {vis_value})")

        raise ValueError("Error decoding VIS header (invalid parity bit)")

    def _decode_vis_narrow(self, signal: Signal, vis_start: int, bit_time: float = VIS_NARROW_BIT_SIZE) -> tuple:
        """Decodes the vis from the audio data and returns the SSTV mode"""
        bit_groups = 4
        bit_count = 6
        vis_bits = list(
            read_bits(
                signal, bit_groups * bit_count, bit_time,
                freq_true=BIT_1_NARROW_FREQ, freq_false=BIT_0_NARROW_FREQ,
                sample_rate=self.sample_rate, offset=vis_start
            )
        )

        vis1, vis2, vis_value, vis4 = (bits_to_int(
            vis_bits[g * bit_count:g * bit_count + bit_count]
        ) for g in range(bit_groups))

        if vis1 != VIS_NARROW_PART1 or vis2 != VIS_NARROW_PART1 or vis_value ^ vis2 != vis4:
            raise ValueError(f"Invalid VIS quadruplet ({vis1}, {vis2}, {vis_value}, {vis4})")

        if mode := NARROW_VIS_MAP.get(vis_value):
            print(f"Detected SSTV mode {mode.NAME}")
            return mode, bit_groups * bit_count

        raise ValueError(f"SSTV mode is unsupported (VIS: {vis_value})")

    def _align_sync(self, signal: Signal, mode, align_start: int, start_of_sync: bool = True):
        """Returns sample where the beginning of the sync pulse was found"""

        # TODO - improve this

        sync_window = round(mode.SYNC_PULSE * 1.4 * self.sample_rate)
        align_stop = len(signal) - sync_window

        if align_stop <= align_start:
            return None  # Reached end of audio

        current_sample = align_start
        for current_sample in range(align_start, align_stop):
            search_section = signal[current_sample:current_sample + sync_window]

            if peak_fft_freq(search_section, self.sample_rate) > mode.FREQ_SYNC_MEDIAN:
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
        image_data = [[[0 for _ in range(width)] for _ in range(channels)] for _ in range(height)]

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
                    freq = peak_fft_freq(pixel_area, self.sample_rate)

                    image_data[line][chan][px] = mode.freq_to_color(freq)

        return image_data

    def _draw_image(self, mode, image_data: typing.List[typing.List[typing.List[int]]]) -> Image:
        odd_lines = mode.HAS_ODD_LINES
        width = mode.LINE_WIDTH
        height = mode.LINE_COUNT
        channels = mode.CHAN_COUNT

        image = Image.new(mode.COLOR.mode_pil(), (width, height))
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

        image = image.convert("RGB")

        print("...Done!")
        return image
