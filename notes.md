```
# https://github.com/n5ac/mmsstv/blob/master/Main.cpp
# {'smR24': 'Robot 24',    +
#  'smR36': 'Robot 36',    +
#  'smR72': 'Robot 72',    +
#  'smSCT1': 'Scottie 1',  +
#  'smSCT2': 'Scottie 2',  +
#  'smSCTDX': 'ScottieDX', +
#  'smMRT1': 'Martin 1',   +
#  'smMRT2': 'Martin 2',   +
#  'smMR73': 'MR73',       +
#  'smMR90': 'MR90',       +
#  'smMR115': 'MR115',     +
#  'smMR140': 'MR140',     +
#  'smMR175': 'MR175',     +
#  'smMP73': 'MP73',       +
#  'smMP115': 'MP115',     +
#  'smMP140': 'MP140',     +
#  'smMP175': 'MP175',     +
#  'smML180': 'ML180',     +
#  'smML240': 'ML240',     +
#  'smML280': 'ML280',     +
#  'smML320': 'ML320',     +
#  'smSC2_180': 'SC2 180', +
#  'smSC2_120': 'SC2 120', +
#  'smSC2_60': 'SC2 60',   +
#  'smPD50': 'PD50',       +
#  'smPD90': 'PD90',       +
#  'smPD120': 'PD120',     +
#  'smPD160': 'PD160',     +
#  'smPD180': 'PD180',     +
#  'smPD240': 'PD240',     +
#  'smPD290': 'PD290',     +
#  'smRM8': 'B/W 8',       +
#  'smRM12': 'B/W 12',     +
#  'smP3': 'P3',           +
#  'smP5': 'P5',           +
#  'smP7': 'P7',           +
#  'smAVT': 'AVT 90',      +
#
#
# narrow
#  'smMN73': 'MP73-N',
#  'smMN110': 'MP110-N',
#  'smMN140': 'MP140-N',
#
#  'smMC110': 'MC110-N',
#  'smMC140': 'MC140-N',
#  'smMC180': 'MC180-N'}


FSK_IDS_NARROW = {
    smMN73: 0x02,
    smMN110: 0x04,
    smMN140: 0x05,
    smMC110: 0x14,
    smMC140: 0x15,
    smMC180: 0x16,
}

FSK_IDS_WIDE = {
    smR36: 0x88,
    smR72: 0x0c,
    smAVT: 0x44,
    smSCT1: 0x3c,
    smSCT2: 0xb8,
    smSCTDX: 0xcc,
    smMRT1: 0xac,
    smMRT2: 0x28,
    smSC2_180: 0xb7,
    smSC2_120: 0x3f,
    smSC2_60: 0xbb,
    smPD50: 0xdd,
    smPD90: 0x63,
    smPD120: 0x5f,
    smPD160: 0xe2,
    smPD180: 0x60,
    smPD240: 0xe1,
    smPD290: 0xde,
    smP3: 0x71,
    smP5: 0x72,
    smP7: 0xf3,
    smMR73: 0x4523,
    smMR90: 0x4623,
    smMR115: 0x4923,
    smMR140: 0x4a23,
    smMR175: 0x4c23,
    smMP73: 0x2523,
    smMP115: 0x2923,
    smMP140: 0x2a23,
    smMP175: 0x2c23,
    smML180: 0x8523,
    smML240: 0x8623,
    smML280: 0x8923,
    smML320: 0x8a23,
    smR24: 0x84,
    smRM8: 0x82,
    smRM12: 0x86,

}


CWID_TABLE = {
    "0": 0x0005, "1": 0x8005, "2": 0xc005, "3": 0xe005, "4": 0xf005, "5": 0xf805, "6": 0x7805, "7": 0x3805,
    "8": 0x1805, "9": 0x0805, ":": 0x0000, ";": 0x0000, "<": 0x0000, "=": 0x7005, ">": 0xA805, "?": 0xcc06,
    "@": 0x0000, "A": 0x8002, "B": 0x7004, "C": 0x5004, "D": 0x6003, "E": 0x8001, "F": 0xd004, "G": 0x2003,
    "H": 0xf004, "I": 0xc002, "J": 0x8004, "K": 0x4003, "L": 0xb004, "M": 0x0002, "N": 0x4002, "O": 0x0003,
    "P": 0x9004, "Q": 0x2004, "R": 0xa003, "S": 0xe003, "T": 0x0001, "U": 0xc003, "V": 0xe004, "W": 0x8003,
    "X": 0x6004, "Y": 0x4004, "Z": 0x3004,
}



import math
import typing
from itertools import cycle

from common import RGB
from consts import *
from image import ImageReader
from tools import byte
from utils import get_RY, color_to_freq, color_to_freq_narrow


class Modulator:
    def __init__(self, sample_freq: int):
        self.sample_freq = sample_freq
        self.buffer = []

    def write(self, freq: int, time: typing.Optional[float] = None):
        self.buffer.append((freq, time))

    # def write_n(self, freq: int, ):
    def write_fsk(self, b: int):
        for i in range(6):
            freq = 1900 if b & 0x01 else FSKSPACE

            self.write(freq, FSKINTVAL)
            b = byte(b >> 1)

    # def write_cwid(self, c):
    #     dot = self.cewid_speed + 30
    #     c = char(toupper(c))
    #     c &= 0x7f;
    #     int d;
    #     if( c == '.' ) c = 'R';
    #     if( c == '/' ){
    #     	d = 0x6805;
    #     else if( c == '@' ){
    #     	Write(0, 250)
    #     	return;
    #     else if( (c >= '0') && (c <= 'Z') ){
    #     	c -= '0';
    #     	d = _tbl[c];
    #     else {
    #     	d = 0;
    #     int n = d & 0x00ff;
    #     if( !d ){
    #     	Write(0, dot*7)
    #     	return;
    #     for(int i = 0; i < n; i++ ){
    #     	if( d & 0x8000 ){
    #     		Write(short(sys.m_CWIDFreq), dot)
    #     	else
    #     		Write(short(sys.m_CWIDFreq), dot*3)
    #     	Write(0, dot)
    #     	d = d << 1;
    #     Write(0, dot*2)

    def gen_tones(self):
        """generates samples between -1 and +1 from gen_freq_bits()

           performs sampling according to
           the samples per second value given during construction
        """
        spms = self.sample_freq / 1000
        offset = 0
        samples = 0
        factor = 2 * math.pi / self.sample_freq
        sample = 0

        for freq, msec in self.buffer:
            samples += spms * msec
            tx = int(samples)
            freq_factor = freq * factor

            for sample in range(tx):
                # yield math.sin(math.fmod(sample * freq_factor + offset, 2 * math.pi))
                yield math.sin(sample * freq_factor + offset)

            offset += (sample + 1) * freq_factor
            samples -= tx


class Scaner(Modulator):
    def __init__(self, image: ImageReader, sample_freq: int):
        self.image = image
        super().__init__(sample_freq)

    def line_R24(self, line: typing.List[RGB]):
        line_width = len(line)
        line_ry = cycle(map(get_RY, line))

        self.write(1200, 6)
        self.write(1500, 2)

        for y, ry, by in line_ry:
            self.write(color_to_freq(y), 92.0 / line_width)

        self.write(1500, 3.0)
        self.write(1900, 1.0)

        for y, ry, by in line_ry:
            self.write(color_to_freq(ry), 46.0 / line_width)

        self.write(2300, 3.0)
        self.write(1900, 1.0)

        for y, ry, by in line_ry:
            self.write(color_to_freq(by), 46.0 / line_width)

    def line_R36(self, line: typing.List[RGB]):
        line_width = len(line)
        line_ry = cycle(map(get_RY, line))

        line_odd = bool(line_num & 1)

        self.write(1200, 9)
        self.write(1500, 3)

        for y, ry, by in line_ry:
            self.write(color_to_freq(y), 88.0 / line_width)

        self.write(2300 if line_odd else 1500, 4.5)  # ry=1500, by=2300
        self.write(1900, 1.5)

        for y, ry, by in line_ry:
            self.write(color_to_freq(by if line_odd else ry), 44.0 / line_width)

    def line_R72(self, line: typing.List[RGB]):
        line_width = len(line)
        line_ry = cycle(map(get_RY, line))

        self.write(1200, 9)
        self.write(1500, 3)

        for y, ry, by in line_ry:
            self.write(color_to_freq(y), 138.0 / line_width)

        self.write(1500, 4.5)
        self.write(1900, 1.5)

        for y, ry, by in line_ry:
            self.write(color_to_freq(ry), 69.0 / line_width)

        self.write(2300, 4.5)
        self.write(1900, 1.5)

        for y, ry, by in line_ry:
            self.write(color_to_freq(by), 69.0 / line_width)

    def line_AVT(self, line: typing.List[RGB]):
        line_width = len(line)
        line_rgb = cycle(line)

        for r, g, b in line_rgb:
            self.write(color_to_freq(r) + 0x1000, 125.0 / line_width)

        for r, g, b in line_rgb:
            self.write(color_to_freq(g) + 0x2000, 125.0 / line_width)

        for r, g, b in line_rgb:
            self.write(color_to_freq(b) + 0x3000, 125.0 / line_width)

    def line_SCT(self, tw: float):
        line = self.image.current_line()
        line_width = len(line)

        tw /= line_width

        # self.write(1500 + 0x2000, 1.5)
        self.write(1500, 1.5)

        for r, g, b in line:
            # self.write(color_to_freq(g) + 0x2000, tw)
            self.write(color_to_freq(g), tw)

        # self.write(1500 + 0x3000, 1.5)
        self.write(1500, 1.5)

        for r, g, b in line:
            # self.write(color_to_freq(b) + 0x3000, tw)
            self.write(color_to_freq(b), tw)

        self.write(1200, 9)
        # self.write(1500 + 0x1000, 1.5)
        self.write(1500, 1.5)

        for r, g, b in line:
            # self.write(color_to_freq(r) + 0x1000, tw)
            self.write(color_to_freq(r), tw)

    def line_MRT(self, line: typing.List[RGB], tw: float):
        line_width = len(line)
        line_rgb = cycle(line)

        tw /= line_width

        self.write(1200, 4.862)
        self.write(1500 + 0x2000, 0.572)

        for r, g, b in line_rgb:
            self.write(color_to_freq(g) + 0x2000, tw)

        self.write(1500 + 0x3000, 0.572)

        for r, g, b in line_rgb:
            self.write(color_to_freq(b) + 0x3000, tw)

        self.write(1500 + 0x1000, 0.572)

        for r, g, b in line_rgb:
            self.write(color_to_freq(r) + 0x1000, tw)

        self.write(1500, 0.572)

    def line_SC2180(self, line: typing.List[RGB], s: float, tw: float):
        line_width = len(line)
        line_rgb = cycle(line)

        tw /= line_width

        self.write(1200, s)
        self.write(1500 + 0x1000, 0.5)

        for r, g, b in line_rgb:
            self.write(color_to_freq(r) + 0x1000, tw)

        for r, g, b in line_rgb:
            self.write(color_to_freq(g) + 0x2000, tw)

        for r, g, b in line_rgb:
            self.write(color_to_freq(b) + 0x3000, tw)

    def line_PD(self, line: typing.List[RGB], tw: float):
        line_width = len(line)
        line_ry = cycle(map(get_RY, line))

        tw /= line_width

        self.write(1200, 20)
        self.write(1500, 2.08)

        for y, ry, by in line_ry:
            self.write(color_to_freq(y), tw)

        for y, ry, by in line_ry:
            self.write(color_to_freq(ry), tw)

        for y, ry, by in line_ry:
            self.write(color_to_freq(by), tw)

        # FIXME: Write next line instead current
        for y, ry, by in line_ry:
            self.write(color_to_freq(y), tw)

    def line_P(self, line: typing.List[RGB], s: float, p: float, c: float):
        line_width = len(line)
        line_rgb = cycle(line)

        tw = c / line_width  # 640.0

        self.write(1200, s)
        self.write(1500 + 0x1000, p)

        for r, g, b in line_rgb:
            self.write(color_to_freq(r) + 0x1000, tw)

        for r, g, b in line_rgb:
            self.write(color_to_freq(g) + 0x2000, tw)

        for r, g, b in line_rgb:
            self.write(color_to_freq(b) + 0x3000, tw)

        self.write(1500, p)

    def line_MP(self, line: typing.List[RGB], tw: float):
        line_width = len(line)
        line_ry = cycle(map(get_RY, line))

        tw /= line_width

        self.write(1200, 9)
        self.write(1500, 1)

        for y, ry, by in line_ry:
            self.write(color_to_freq(y), tw)

        for y, ry, by in line_ry:
            self.write(color_to_freq(ry), tw)

        for y, ry, by in line_ry:
            self.write(color_to_freq(by), tw)

        # FIXME: Write next line instead current
        for y, ry, by in line_ry:
            self.write(color_to_freq(y), tw)

    def line_MR(self, line: typing.List[RGB], tw: float):
        # line_width = len(line)
        line_ry = cycle(map(get_RY, line))

        ty = tw / TXW  # FIXME
        tc = ty / 2

        self.write(1200, 9)
        self.write(1500, 1)

        d = 0

        for y, ry, by in line_ry:
            self.write(color_to_freq(y), ty)

        for y, ry, by in line_ry:
            self.write(color_to_freq(ry), tc)

        for y, ry, by in line_ry:
            self.write(color_to_freq(by), tw)

        # FIXME: Write next line instead current
        for y, ry, by in line_ry:
            d = color_to_freq(y)  # FIXME
            self.write(color_to_freq(y), tc)

        self.write(d, 0.1)

    def line_RM(self, line: typing.List[RGB], ts: float, tw: float):
        line_width = len(line)
        line_ry = cycle(map(get_RY, line))

        tw /= line_width

        # ty = tw / TXW # FIXME
        # tc = ty / 2

        self.write(1200, ts)
        self.write(1500, ts / 3)

        # ------------- for y, ry, by in line_ry:
        # -------------     self.write(color_to_freq(y), ty)
        # 	for( x = 0; x < 320; x++ ){     // Y
        # 		GetRY(Y[x], RY, BY, pBitmapTX->Canvas->Pixels[x][mp->m_wLine])
        # 	}
        # 	mp->m_wLine++;
        # 	for( x = 0; x < 320; x++ ){     // Y
        # 		GetRY(YY, RY, BY, pBitmapTX->Canvas->Pixels[x][mp->m_wLine])
        # 		YY = (YY + Y[x]) / 2;
        # 		mp->Write(short(ColorToFreq(YY)), tw)

    def line_MN(self, line: typing.List[RGB], tw: float):
        line_width = len(line)
        line_ry = cycle(map(get_RY, line))

        tw /= line_width

        self.write(NARROW_SYNC, 9)
        self.write(NARROW_LOW, 1)

        for y, ry, by in line_ry:  # odd
            self.write(color_to_freq_narrow(y), tw)

        for y, ry, by in line_ry:
            self.write(color_to_freq_narrow(ry), tw)

        for y, ry, by in line_ry:
            self.write(color_to_freq_narrow(by), tw)

        # FIXME: Write next line instead current
        for y, ry, by in line_ry:  # even
            self.write(color_to_freq_narrow(y), tw)

    def line_MC(self, line: typing.List[RGB], tw: float):
        line_width = len(line)
        line_rgb = cycle(line)

        tw /= line_width  # 640.0

        self.write(NARROW_SYNC, 8)
        self.write(NARROW_LOW, 0.5)

        for r, g, b in line_rgb:
            self.write(color_to_freq_narrow(r), tw)

        for r, g, b in line_rgb:
            self.write(color_to_freq_narrow(g), tw)

        for r, g, b in line_rgb:
            self.write(color_to_freq_narrow(b), tw)


class SSTV(Scaner):
    def __init__(self, image: ImageReader, sample_freq: int, mode: int, narrow: bool = False):
        self.mode = mode
        self.narrow = narrow

        super().__init__(image, sample_freq)

        self.image.size = (320, 256)

    def write_head(self):
        tone_duration = 100  # ms

        if self.narrow:
            tones = [1900, 2300, 1900, 2300]
        else:
            tones = [1900, 1500, 1900, 1500, 2300, 1500, 2300, 1500]

        for freq in tones:
            self.write(freq, tone_duration)

    def write_image(self):
        if self.narrow:
            fsk = FSK_IDS_NARROW[self.mode]

            self.write(1900, 300)
            self.write(FSKSPACE, FSKGARD)
            self.write(1900, FSKINTVAL)
            self.write_fsk(0x2d)
            self.write_fsk(0x15)
            # FSK
            self.write_fsk(fsk)
            self.write_fsk(fsk ^ 0x15)
        else:
            for n in range(3 if self.mode == smAVT else 1):
                self.write(1900, 300)
                self.write(1200, 10)
                self.write(1900, 300)
                self.write(1200, 30)

                d = FSK_IDS_WIDE[self.mode]
                if d >= 0x100:
                    fsk_len = 16
                else:
                    fsk_len = 8

                for _ in range(fsk_len):
                    self.write(1100 if d & 0x0001 else 1300, 30)
                    d >>= 1

                self.write(1200, 30)

            if self.mode == smAVT:
                sd = 0x5fa0

                for _ in range(32):
                    self.write(1900, 9.7646)
                    d = sd
                    for _ in range(16):
                        self.write(1600 if d & 0x8000 else 2200, 9.7646)
                        d <<= 1

                    sd = ((sd & 0xff00) - 0x0100) | ((sd & 0x00ff) + 0x0001)

                self.write(0, 0.30514375)
            elif self.mode in {smSCT1, smSCT2, smSCTDX}:
                self.write(1200, 9.0)

        tl = 256
        line = -51000  # 0
        while not self.image.eof:
            if line >= tl:
                if line == tl:
                    if not self.txfskid:
                        tw = self.sample_freq / 2
                        if not self.narrow:
                            # self.writeC(1500, SSTVSET.m_TW > tw ? tw : SSTVSET.m_TW);
                            for freq in [1900, 1500, 1900, 1500]:
                                self.write(freq, 100)
                        else:
                            # self.writeC(1900, SSTVSET.m_TW > tw ? tw : SSTVSET.m_TW)
                            pass
                    else:
                        self.write(1900 if self.narrow else 1500, 300)

                    line += 1
                elif line == tl + 1:
                    # if( mp->GetBufCnt() < (2 * SampFreq) ){
                    # 	if( sys.m_TXFSKID && !sys.m_Call.IsEmpty() ){
                    # 		OutputFSKID();
                    # 	}
                    # 	if( sys.m_CWID == 1 ){
                    # 		OutputCWID();
                    # 	}
                    # 	else if( (sys.m_CWID == 2) && !sys.m_MMVID.IsEmpty() ){
                    # 		OutputMMV();
                    # 	}
                    # 	mp->m_wLine++;
                    # }
                    pass
                elif line == tl + 2:
                    # if( !mp->m_Cnt && !mp->m_RowCnt ){
                    # 	pSound->TrigBCC();
                    # 	mp->m_wLine++;
                    # }
                    pass
                # else if( pSound->GetBCC() < 0 ){
                #	int lost = mp->m_Lost;
                #	ToRX();
                #	if( lost ) InfoTxLost();
                #	if( KSRR->Checked && (m_MainPage == pgTX) ){
                #		AdjustPage(pgRX);
                #	}
                #	return;
                # }
            else:
                line += 1

                self.write_pixels()
                self.image.next()

    def write_pixels(self):
        if self.mode == smR36:
            self.line_R36()  # v
        elif self.mode == smR72:
            self.line_R72()  # v
        elif self.mode == smAVT:
            self.line_AVT()  # ??
        elif self.mode == smSCT1:
            self.line_SCT(138.24)  # v
        elif self.mode == smSCT2:
            self.line_SCT(88.064)  # v
        elif self.mode == smSCTDX:
            self.line_SCT(345.6)  # v
        elif self.mode == smMRT1:
            self.line_MRT(146.432)  # v
        elif self.mode == smMRT2:
            self.line_MRT(73.216)  # v
        elif self.mode == smSC2_180:
            self.line_SC2180(5.5437, 235.0)
        elif self.mode == smSC2_120:
            self.line_SC2180(5.52248, 156.5)
        elif self.mode == smSC2_60:
            self.line_SC2180(5.5006, 78.128)  # 6.0006
        elif self.mode == smPD50:
            self.line_PD(91.520)
        elif self.mode == smPD90:
            self.line_PD(170.240)
        elif self.mode == smPD120:
            self.line_PD(121.600)
        elif self.mode == smPD160:
            self.line_PD(195.584)
        elif self.mode == smPD180:
            self.line_PD(183.040)
        elif self.mode == smPD240:
            self.line_PD(244.480)
        elif self.mode == smPD290:
            self.line_PD(228.800)
        elif self.mode == smP3:
            self.line_P([],5.208, 1.042, 133.333)
        elif self.mode == smP5:
            self.line_P([],7.813, 1.562375, 200.000)
        elif self.mode == smP7:
            self.line_P([],10.417, 2.083, 266.667)
        elif self.mode == smMR73:
            self.line_MR(138.0)
        elif self.mode == smMR90:
            self.line_MR(171.0)
        elif self.mode == smMR115:
            self.line_MR(220.0)
        elif self.mode == smMR140:
            self.line_MR(269.0)
        elif self.mode == smMR175:
            self.line_MR(337.0)
        elif self.mode == smMP73:
            self.line_MP(140.0)
        elif self.mode == smMP115:
            self.line_MP(223.0)
        elif self.mode == smMP140:
            self.line_MP(270.0)
        elif self.mode == smMP175:
            self.line_MP(340.0)
        elif self.mode == smML180:
            self.line_MR(176.5)
        elif self.mode == smML240:
            self.line_MR(236.5)
        elif self.mode == smML280:
            self.line_MR(277.5)
        elif self.mode == smML320:
            self.line_MR(317.5)
        elif self.mode == smR24:
            self.line_R24()
        elif self.mode == smRM8:
            self.line_RM(6.0, 58.89709)
        elif self.mode == smRM12:
            self.line_RM(6.0, 92.0)
        elif self.mode == smMN73:
            self.line_MN(140.0)
        elif self.mode == smMN110:
            self.line_MN(212.0)
        elif self.mode == smMN140:
            self.line_MN(270.0)
        elif self.mode == smMC110:
            self.line_MC(140.0)
        elif self.mode == smMC140:
            self.line_MC(180.0)
        elif self.mode == smMC180:
            self.line_MC(232.0)

```