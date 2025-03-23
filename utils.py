import typing
from functools import reduce


def bit_to_int(bits: typing.List[int]) -> int:
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
