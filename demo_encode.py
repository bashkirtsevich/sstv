import numpy as np
from PIL import Image
from scipy.io.wavfile import write

from sstv import CODEC_MAP, SSTVEncoder


def main(img_path: str, wav_path: str, mode: str, sample_rate=11025):
    encoder = SSTVEncoder(sample_rate)
    with Image.open(img_path) as im:
        amplitude = np.iinfo(np.int16).max
        tones = np.fromiter(encoder.encode(im, CODEC_MAP[mode]), dtype=np.float32) * amplitude

    write(wav_path, sample_rate, tones.astype(np.int16))


if __name__ == '__main__':
    main(
        img_path="examples/color-bars.png",
        wav_path="examples/signal.wav",
        mode="Scottie DX"
    )
