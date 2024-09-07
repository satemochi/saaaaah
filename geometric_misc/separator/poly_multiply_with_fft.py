from math import log
from numpy.fft import rfft, irfft


def pm_fft(a, b):
    length = 1 << int(log(len(a)+len(b)+1, 2))
    a_f, b_f = rfft(a, length), rfft(b, length)
    c_f = [ai*bi for ai, bi in zip(a_f, b_f)]
    return [int(ci) for ci in irfft(c_f, length)]


if __name__ == '__main__':
    a = (0, 0, -1, -4)
    b = (-9, 0, 8)
    print(pm_fft(a, b))     # expect to: 0, 0, 9, 36, -8, -32
