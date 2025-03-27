from scipy.io.wavfile import read

from sstv import SSTVDecoder


def main(wav_path: str, img_path: str):
    sample_rate, signal = read(wav_path)

    decoder = SSTVDecoder(sample_rate)

    img = decoder.decode(signal)
    img.save(img_path)


if __name__ == '__main__':
    main(
        wav_path="examples/signal.wav",
        img_path="examples/color-bars.png"
    )
