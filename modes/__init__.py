from .amiga import Amiga90
from .bw import RobotBW8, RobotBW12
from .martin import Martin1
from .martin import Martin2
from .mmsstv import MMSSTVML180
from .mmsstv import MMSSTVML240
from .mmsstv import MMSSTVML280
from .mmsstv import MMSSTVML320
from .mmsstv import MMSSTVMP115
from .mmsstv import MMSSTVMP140
from .mmsstv import MMSSTVMP175
from .mmsstv import MMSSTVMP73
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

CODECS = [
    Amiga90,

    Martin1, Martin2,

    MMSSTVMR73, MMSSTVMR90, MMSSTVMR115, MMSSTVMR140, MMSSTVMR175,
    MMSSTVMP73, MMSSTVMP115, MMSSTVMP140, MMSSTVMP175,
    MMSSTVML180, MMSSTVML240, MMSSTVML280, MMSSTVML320,

    # MMSSTV73N,

    P3, P5, P7,

    PD50, PD90, PD120, PD160, PD180, PD240, PD290,

    Robot24, Robot36, Robot72,
    RobotBW8, RobotBW12,

    SC2120, SC2180, SC260,

    Scottie1, Scottie2, ScottieDX,
]

CODEC_MAP = {
    codec.NAME: codec
    for codec in CODECS
}

VIS_MAP = {
    codec.VIS_CODE: codec
    for codec in CODECS
}
