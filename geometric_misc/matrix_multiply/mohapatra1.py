from itertools import product
import numpy as np


def mohapatra(a, b):
    """ Matrix multiplication for nxn-matrix of positive integers

        Inspired by
            https://github.com/ShrohanMohapatra/matrix_multiply_quadratic
        and reference:
            S. Mohapatra, (2018).
            "A new quadratic-time number-theoretic algorithm to solve
                matrix multiplication problem"
            https://arxiv.org/abs/1806.03701
    tips:
        a, b:   given matrixes
        n:  length of rows/columns
        m:  digit of the max value among matrix a and b
        p:  digit of sum of n values of mxm digit
        pad1:   padding 0s for separating rows/columns values, or
                effective digits in the solution.
        pad2:   interesting position.

    """
    n = min(a.shape)
    dom = list(range(n))

    m = int(np.math.log10(max(a.max(), b.max()))) + 1
    p = int(np.math.log10((10**(2*m)-1)*n)) + 1
    pad1, pad2 = 10**p, 10**(p*(n-1))

    c = [int(sum(a[i][j]*(pad2/(pad1**j)) for j in dom)) for i in dom]
    d = [int(sum(b[-i-1][j]*(pad2/(pad1**i)) for i in dom)) for j in dom]

    e = np.zeros((n, n))
    for i, j in product(dom, repeat=2):
        e[i][j] = int(c[i]*d[j]/pad2) % pad1
    return e


def _test(a, b):
    print(a)
    print(b)
    n = min(a.shape)
    return all(a[i][j] == b[i][j] for i, j in product(range(n), repeat=2))


if __name__ == '__main__':
    a = np.arange(91,100).reshape((3,3))
    b = np.arange(91,100)[::-1].reshape((3,3))
    print(a)
    print(b)
    print('-----------------')
    print(_test(mohapatra(a, b), a @ b))

