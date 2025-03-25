import typing
from functools import reduce
from statistics import median

import numpy as np
from scipy.signal.windows import hann

from modes.mode import Tone

Bit = typing.Literal[0, 1]
Signal = typing.List[float]
SignalGen = typing.Generator[float, None, None]
BitGen = typing.Generator[Bit, None, None]
ToneSlice = typing.Tuple[slice, float]
ToneSlices = typing.List[ToneSlice]


def bits_to_int(bits: typing.List[Bit]) -> int:
    return reduce(lambda value, bit: (value << 1) | (bit & 1), bits[::-1])


def barycentric_peak_interp(bins, x):
    # Takes x as the index of the largest bin and interpolates the
    # x value of the peak using neighbours in the bins array

    # Make sure data is in bounds
    y1 = bins[x] if x <= 0 else bins[x - 1]
    y3 = bins[x] if x + 1 >= len(bins) else bins[x + 1]

    denom = y3 + bins[x] + y1
    if denom == 0:
        return 0  # erroneous

    return (y3 - y1) / denom + x


def peak_fft_freq(signal: Signal, sample_rate: float) -> float:
    windowed_data = signal * hann(len(signal))
    fft = np.abs(np.fft.rfft(windowed_data))

    # Get index of bin with the highest magnitude
    x = np.argmax(fft)
    # Interpolated peak frequency
    peak = barycentric_peak_interp(fft, x)

    # Return frequency in hz
    return peak * sample_rate / len(windowed_data)


def read_bits(signal: Signal,
              bit_count: int, bit_time: float,
              freq_true: float, freq_false: float,
              sample_rate: float,
              offset: int = 0) -> BitGen:
    bit_threshold = median([freq_true, freq_false])
    bit_size = round(bit_time * sample_rate)

    for bit_idx in range(bit_count):
        bit_offset = offset + bit_idx * bit_size
        section = signal[bit_offset:bit_offset + bit_size]
        freq = peak_fft_freq(section, sample_rate)
        yield int(freq <= bit_threshold)


def tones_to_slices(tones: typing.Iterable[Tone],
                    sample_rate: float,
                    window_size: typing.Optional[float] = None) -> typing.Tuple[int, ToneSlices]:
    # The margin of error created here will be negligible when decoding the
    # vis due to each bit having a length of 30ms. We fix this error margin
    # when decoding the image by aligning each sync pulse
    slices = []
    time_acc = 0
    for it in tones:
        area = slice(
            round(time_acc * sample_rate),
            round((time_acc + (window_size or it.time)) * sample_rate)
        )
        slices.append((area, it.freq))
        time_acc += it.time

    return (round(time_acc * sample_rate), slices)


def match_frequencies(signal: Signal, slices: typing.List[typing.Tuple[slice, float]],
                      sample_rate: float, threshold: float = 50.0) -> bool:
    # Check they're the correct frequencies
    return all(abs(peak_fft_freq(signal[part], sample_rate) - freq) < threshold for part, freq in slices)
