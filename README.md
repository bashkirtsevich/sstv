# HAM SSTV Python implementation

Based on [this](https://github.com/colaclanth/sstv) repository.

Supported codecs:

Narrow:

* MMSSTV MP110-N, MMSSTV MP140-N, MMSSTV MP73-N
* MMSSTV MC110-N, MMSSTV MC140-N, MMSSTV MC180-N

Wide:

* Amiga Video Transceiver 90
* Martin 1, Martin 2
* MMSSTV MR73, MMSSTV MR90, MMSSTV MR115, MMSSTV MR140, MMSSTV MR175, MMSSTV MP73, MMSSTV MP115, MMSSTV MP140, MMSSTV
  MP175, MMSSTV ML180, MMSSTV MP240, MMSSTV MP280, MMSSTV MP320
* P3, P5, P7
* PD50, PD90, PD120, PD160, PD180, PD240, PD290
* Robot 24, Robot 36, Robot 72, Robot B&W 8, Robot B&W 12
* SC2 120, SC2 180, SC2 60
* Scottie 1, Scottie 2, Scottie DX

Documentation:

1. [sstv-handbook](doc/sstv-handbook.pdf)
2. [sstv_05](doc/sstv_05.pdf)

## Installation

### PIP

`pip install -r requirements-cli.txt`

## Usage

Common usage:
```
Usage: sstv.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  decode
  encode
```

Encode:
```
Usage: sstv.py encode [OPTIONS] IMG_PATH WAV_PATH

Options:
  -m, --mode [Amiga Video Transceiver 90|Martin 1|Martin 2|MMSSTV MR73|MMSSTV MR90|MMSSTV MR115|MMSSTV MR140|MMSSTV MR175|MMSSTV MP73|MMSSTV MP115|MMSSTV MP140|MMSSTV MP175|MMSSTV ML180|MMSSTV MP240|MMSSTV MP280|MMSSTV MP320|P3|P5|P7|PD50|PD90|PD120|PD160|PD180|PD240|PD290|Robot 24|Robot 36|Robot 72|Robot B&W 8|Robot B&W 12|SC2 120|SC2 180|SC2 60|Scottie 1|Scottie 2|Scottie DX|MMSSTV MP110-N|MMSSTV MP140-N|MMSSTV MP73-N|MMSSTV MC110-N|MMSSTV MC140-N|MMSSTV MC180-N]
                                  SSTV encoding mode
  -s, --sample_rate INTEGER       Output sample rate
  --help                          Show this message and exit.
```

Decode:
```
Usage: sstv.py decode [OPTIONS] WAV_PATH IMG_PATH

Options:
  -b, --enable_bpf BOOLEAN   Enable band-pass filter
  -f, --bpf [butter|cheby2]  Band-pass filter type
  --help                     Show this message and exit.
```

CLI examples:
```
python sstv.py encode -m "Robot 72" examples/color-bars.png examples/color-bars.wav

python sstv.py decode -b true -f cheby2 examples/color-bars.wav examples/decoded.png
```

Other examples:

1. [Encode](demo_encode.py)
2. [Decode](demo_decode.py)

### Demo

```
python demo_encode.py
python demo_decode.py
```
