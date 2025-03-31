from scipy.io.wavfile import read

from sstv import SSTVDecoder
from sstv.bpf import bandpass_filter, cheby2_bandpass


def main(wav_path: str, img_path: str, bpf: bool = True):
    sample_rate, signal = read(wav_path)

    if bpf:
        signal = bandpass_filter(signal, cheby2_bandpass, 700, 2700, sample_rate)

    decoder = SSTVDecoder(sample_rate, print_logs=True)

    img = decoder.decode(signal)
    img.save(img_path)


if __name__ == '__main__':
    main(
        wav_path="examples/signal.wav",
        img_path="examples/color-bars.png"
    )
