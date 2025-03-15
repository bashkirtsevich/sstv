from scipy.io.wavfile import read

from sstv import SSTVDecoder


def main():
    path = "examples/signal.wav"
    sample_rate, signal = read(path)

    decoder = SSTVDecoder(sample_rate)

    img = decoder.decode(signal)
    img.save("examples/demo_out.jpg")


if __name__ == '__main__':
    main()
