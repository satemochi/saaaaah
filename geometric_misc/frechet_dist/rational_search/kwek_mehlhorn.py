from random import randint, seed
from unittest import TestCase, main
from gmpy2 import mpq, prev_prime


class black_box:
    def __init__(self, x, m):
        self.__x, self.__m = x, m

    @classmethod
    def random_setting(self, m, s=0):
        seed(s)
        return black_box(mpq(randint(1, m), randint(1, m)), m)

    def __le__(self, other):
        return True if self.__x <= other else False

    def __eq__(self, other):
        return True if self.__x == other else False


def rational_search(unknown, domain_size):
    """ ref) Kwek & Mehlhorn (2003): Optimal search for rationals """
    _x = __detect_int_part(unknown)
    _m = domain_size // _x if _x > 0 else domain_size
    _alpha, _beta, _gamma, _delta = __detect_init_range(unknown, _x, _m)
    a, b = __find_fraction(_alpha, _beta, _gamma, _delta)
    return _x + mpq(a, b)


def __detect_int_part(unknown):
    _max = 1
    while not unknown <= _max:  # exponential search
        _max = _max << 1
    _min = _max >> 1
    while _max - _min != 1:
        if unknown <= (split := ((_min + _max) >> 1)):  # binary search
            _max = split
        else:
            _min = split
    return _min


def __detect_init_range(x, _x, _m):
    _min, _max = 0, (denom := 2 * _m * _m)
    while _max - _min != 1:
        if x <= _x + mpq((split := ((_min + _max) >> 1)), denom):
            _max = split
        else:
            _min = split
    return _min, denom, _max, denom


def __find_fraction(alpha, beta, gamma, delta):
    if (alpha // beta == gamma // delta and not mpq(alpha, beta).is_integer()):
        b, a = __find_fraction(delta, gamma % delta, beta, alpha % beta)
        return (alpha // beta) * b + a, b
    return (alpha + beta - 1) // beta, 1


class test_rational_search(TestCase):
    def test_less_than_one(self):
        x = black_box(mpq(5, 13), (m := 1000))
        self.assertTrue(x == rational_search(x, m))

    def test_greater_than_one(self):
        x = black_box(mpq(997, 37), (m := 1000))
        self.assertTrue(x == rational_search(x, m))


if __name__ == '__main__':
    main()
