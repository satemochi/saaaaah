from time import time
import gmpy2


def sieve(limit=1000000):
    sieve_limit = gmpy2.isqrt(limit) + 1
    limit += 1
    bitmap = gmpy2.xmpz(3)
    bitmap[4: limit: 2] = -1
    for p in bitmap.iter_clear(3, sieve_limit):
        bitmap[p*p: limit: p+p] = -1
    return bitmap.iter_clear(2, limit)


def i_sieve(limit=1000000):
    yield 2
    x = init_x(limit)
    limit_sqrt = int(limit**0.5)
    while x:
        p = ffs(x)
        yield p
        i, pp = 1 << p, p+p
        x &= ~i
        if p <= limit_sqrt:
            while ffs(i) <= limit:
                x &= ~i
                i <<= pp


def init_x(limit):
    """ Return a bit-array in which prime-candidates are 1's, and sieved by 2
         * example: (0)10101...0101000, s.t.
            - the first 3-bits are 0 (0 and 1 are not prime, 2 is trivial),
            - each even pos is set (i.e. index begin with 0),
            - the length (or MSB) is limit+1.
    """
    # x = 1
    # for i in range(limit >> 1):
    #     x = (x << 2) + 1
    # return (x >> 1) << 2 & (1 << limit + 1) - 1
    return (2**((((limit+1)//2-1) << 1)+3)-1)//3-2   # sum of geometric series


def ffs(x):
    """ Find First Set: cf.) https://stackoverflow.com/questions/5520655/ """
    return (x & -x).bit_length() - 1


def i_sieve2(limit=1000000):
    yield 2
    goleq = ((((limit+1) >> 1)-1) << 1)+1  # greatest odd less than or equal to
    x = ((2 << (goleq+1))-1)//3-2    # sum(4**i for i in range(goleq))
    sieve_limit, p = int(limit**0.5), 2
    while p <= sieve_limit:
        p = (x & -x).bit_length() - 1   # find first set (ffs/ctz)
        yield p
        n = (limit+1-p) // (2*p) + 1    # approx. exponent of the sieving mask
        x &= ~((1 << p) * ((1 << (2*p*n)) - 1) // ((1 << (2*p)) - 1))   # mask
    while x:
        p = (x & -x).bit_length() - 1   # count trailling zeros (ffs/ctz)
        yield p
        x &= ~(1 << p)      # negate p-th bit


def eval(alg, n):
    s = time()
    list(alg(n))
    return time() - s


def e(n=1000):
    gmpy, mochi, = [], []
    dom = list(range(5, n))
    for i in dom:
        gmpy.append(eval(sieve, i))
        mochi.append(eval(i_sieve2, i))
    from matplotlib import pyplot as plt
    plt.plot(dom, gmpy, label='gmpy2.xmpz')
    plt.plot(dom, mochi, label='hand-made')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('eratos_m1000.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    e(10000)
