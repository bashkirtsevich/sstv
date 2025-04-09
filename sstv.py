import click
import numpy as np
from PIL import Image
from scipy.io.wavfile import read
from scipy.io.wavfile import write

from sstv import CODEC_MAP, SSTVEncoder
from sstv import SSTVDecoder
from sstv.bpf import bandpass_filter, FILTERS
from sstv.modes import Robot72


@click.group()
def main():
    pass


@main.command()
@click.argument("img_path", type=click.Path(exists=True, dir_okay=False))
@click.argument("wav_path", type=click.Path(exists=False, dir_okay=False))
@click.option("-m", "--mode", type=click.Choice(CODEC_MAP.keys()), default=Robot72.NAME,
              help="SSTV encoding mode")
@click.option("-s", "--sample_rate", type=click.INT, default=11025,
              help="Output sample rate")
def encode(img_path: str, wav_path: str, mode: str, sample_rate: int):
    encoder = SSTVEncoder(sample_rate)
    with Image.open(img_path) as im:
        amplitude = np.iinfo(np.int16).max
        tones = np.fromiter(encoder.encode(im, CODEC_MAP[mode]), dtype=np.float32) * amplitude

    write(wav_path, sample_rate, tones.astype(np.int16))


@main.command()
@click.argument("wav_path", type=click.Path(exists=True, dir_okay=False))
@click.argument("img_path", type=click.Path(exists=False, dir_okay=False))
@click.option("-b", "--enable_bpf", type=click.BOOL, default=True,
              help="Enable band-pass filter")
@click.option("-f", "--bpf", type=click.Choice(FILTERS.keys()), default="cheby2",
              help="Band-pass filter type")
def decode(wav_path: str, img_path: str, enable_bpf: bool, bpf: str):
    sample_rate, signal = read(wav_path)

    if enable_bpf:
        signal = bandpass_filter(signal, FILTERS[bpf], 700, 2700, sample_rate)

    decoder = SSTVDecoder(sample_rate, print_logs=True)

    img = decoder.decode(signal)
    img.save(img_path)


if __name__ == '__main__':
    main()
