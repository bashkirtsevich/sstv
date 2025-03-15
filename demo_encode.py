import numpy as np
from PIL import Image
from scipy import signal
from scipy.io.wavfile import write

from modes import *
from sstv import SSTVEncoder


def lowpass(cutoff, fs, order=5):
    # return signal.butter(order, cutoff, fs=fs, btype='low', analog=False)
    return signal.ellip(order, 1, 40, cutoff, fs=fs, btype='low', analog=False)
    # return signal.cheby2(order, 40, cutoff, fs=fs, btype='low', analog=False)


def lowpass_filter(data, cutoff, fs, order=5):
    b, a = lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y


def main():
    sample_rate = 11025

    path = "examples/color-bars.png"

    encoder = SSTVEncoder(sample_rate)
    with Image.open(path) as im:
        amplitude = np.iinfo(np.int16).max
        tones = np.fromiter(encoder.encode(im, Martin1), dtype=np.float32) * amplitude

    write("examples/signal.wav", sample_rate, tones.astype(np.int16))


if __name__ == '__main__':
    main()
