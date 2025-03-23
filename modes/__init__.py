from .amiga import Amiga90
from .bw import RobotBW8, RobotBW12
from .martin import Martin1
from .martin import Martin2
from .mmsstv import MMSSTVML180
from .mmsstv import MMSSTVML240
from .mmsstv import MMSSTVML280
from .mmsstv import MMSSTVML320
from .mmsstv import MMSSTVMPN110
from .mmsstv import MMSSTVMPN140
from .mmsstv import MMSSTVMPN73
from .mmsstv import MMSSTVMPW115
from .mmsstv import MMSSTVMPW140
from .mmsstv import MMSSTVMPW175
from .mmsstv import MMSSTVMPW73
from .mmsstv import MMSSTVMR115
from .mmsstv import MMSSTVMR140
from .mmsstv import MMSSTVMR175
from .mmsstv import MMSSTVMR73
from .mmsstv import MMSSTVMR90
from .pd import PD120
from .pd import PD160
from .pd import PD180
from .pd import PD240
from .pd import PD290
from .pd import PD50
from .pd import PD90
from .px import P3
from .px import P5
from .px import P7
from .robot import Robot24
from .robot import Robot36
from .robot import Robot72
from .sc2 import SC2120
from .sc2 import SC2180
from .sc2 import SC260
from .scottie import Scottie1
from .scottie import Scottie2
from .scottie import ScottieDX

WIDE_CODECS = [
    Amiga90,

    Martin1, Martin2,

    MMSSTVMR73, MMSSTVMR90, MMSSTVMR115, MMSSTVMR140, MMSSTVMR175,
    MMSSTVMPW73, MMSSTVMPW115, MMSSTVMPW140, MMSSTVMPW175,
    MMSSTVML180, MMSSTVML240, MMSSTVML280, MMSSTVML320,

    P3, P5, P7,

    PD50, PD90, PD120, PD160, PD180, PD240, PD290,

    Robot24, Robot36, Robot72,
    RobotBW8, RobotBW12,

    SC2120, SC2180, SC260,

    Scottie1, Scottie2, ScottieDX,
]

NARROW_CODECS = [
    MMSSTVMPN110, MMSSTVMPN140, MMSSTVMPN73,
]

WIDE_CODEC_MAP = {
    codec.NAME: codec
    for codec in WIDE_CODECS
}

WIDE_VIS_MAP = {
    codec.VIS_CODE: codec
    for codec in WIDE_CODECS
}

NARROW_VIS_MAP = {
    codec.VIS_CODE: codec
    for codec in NARROW_CODECS
}
