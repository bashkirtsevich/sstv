from scipy.signal import butter, lfilter, cheby2


def butter_bandpass(low_cut, high_cut, fs, order=5):
    nyq = 0.5 * fs
    low = low_cut / nyq
    high = high_cut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def cheby2_bandpass(low_cut, high_cut, fs, order=5):
    nyq = 0.5 * fs
    low = low_cut / nyq
    high = high_cut / nyq
    b, a = cheby2(order, 20.0, [low, high], btype='band')
    return b, a


def bandpass_filter(signal, method, low_cut, high_cut, fs, order=5):
    b, a = method(low_cut, high_cut, fs, order=order)
    y = lfilter(b, a, signal)
    return y
