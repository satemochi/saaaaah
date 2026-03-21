from enum import Enum, auto
import unittest
from gmpy2 import mpq


class direction(Enum):
    LEFT, RIGHT = auto(), auto()


def rational_search(a, p, q, d):
    """ ref) Weyers & Vinodchandran (2025):
            Fast Rational Search via Stern-Brocot Tree [arXiv] """
    assert p <= a <= q
    k = exponential_search(a, p, q, d)
    x = binary_search(a, p, q, (1 << (k-1)) - 1, (1 << k) - 1, d)
    if d == direction.LEFT:
        new_q = mpq(q.numerator + (x - 1) * p.numerator,
                    q.denominator + (x - 1) * p.denominator)
        if new_q == a:
            return new_q
        new_p = mpq(q.numerator + x * p.numerator,
                    q.denominator + x * p.denominator)
        return rational_search(a, new_p, new_q, direction.RIGHT)
    else:
        new_p = mpq(p.numerator + (x - 1) * q.numerator,
                    p.denominator + (x - 1) * q.denominator)
        if new_p == a:
            return new_p
        new_q = mpq(p.numerator + x * q.numerator,
                    p.denominator + x * q.denominator)
        return rational_search(a, new_p, new_q, direction.LEFT)


def exponential_search(a, p, q, d):
    assert p <= a <= q
    i, x = 1, mpq(p.numerator + q.numerator, p.denominator + q.denominator)
    if d == direction.RIGHT:
        while x < a:
            i += 1
            x = mpq(p.numerator + ((1 << i) - 1) * q.numerator,
                    p.denominator + ((1 << i) - 1) * q.denominator)
    if d == direction.LEFT:
        while x > a:
            i += 1
            x = mpq(q.numerator + ((1 << i) - 1) * p.numerator,
                    q.denominator + ((1 << i) - 1) * p.denominator)
    return i


def binary_search(a, p, q, higher, lower, d):
    assert p <= a <= q
    if d == direction.RIGHT:
        while lower - higher != 1:
            split = (lower + higher) >> 1
            pivot = mpq(p.numerator + split * q.numerator,
                        p.denominator + split * q.denominator)
            if pivot <= a:
                higher = split
            else:
                lower = split
    if d == direction.LEFT:
        while lower - higher != 1:
            split = (lower + higher) >> 1
            pivot = mpq(q.numerator + split * p.numerator,
                        q.denominator + split * p.denominator)
            if pivot <= a:
                lower = split
            else:
                higher = split
    return lower


class test_rational_search(unittest.TestCase):
    def test_exponential_search(self):
        alpha = mpq(2, 9)
        k = exponential_search(alpha, mpq(0), mpq(1), direction.LEFT)
        self.assertTrue(k == 3)
        self.assertTrue(mpq(1, 1 << k) <= alpha < mpq(1, 1 << (k-1)))

        alpha = mpq(3, 7)
        k = exponential_search(alpha, mpq(0), mpq(1), direction.LEFT)
        self.assertTrue(k == 2)
        self.assertTrue(mpq(1, 1 << k) <= alpha < mpq(1, 1 << (k-1)))

        alpha = mpq(2, 3)
        k = exponential_search(alpha, mpq(0), mpq(1), direction.LEFT)
        self.assertTrue(k == 1)
        self.assertTrue(mpq(1, 1 << k) <= alpha < mpq(1, 1 << (k-1)))

        alpha = mpq(12, 17)
        k = exponential_search(alpha, mpq(0), mpq(1), direction.RIGHT)
        self.assertTrue(k == 2)
        self.assertTrue(alpha < mpq((1 << k) - 1, 1 << k))

        alpha = mpq(10, 13)
        k = exponential_search(alpha, mpq(0), mpq(1), direction.RIGHT)
        self.assertTrue(k == 3)
        self.assertTrue(alpha < mpq((1 << k) - 1, 1 << k))

        alpha = mpq(9, 14)
        k = exponential_search(alpha, mpq(0), mpq(1), direction.RIGHT)
        self.assertTrue(k == 2)
        self.assertTrue(mpq((1 << (k-1)) - 1, 1 << (k-1)) < alpha
                        < mpq((1 << k) - 1, 1 << k))

    def test_binary_search_left(self):
        a = mpq(2, 9)
        p, q = mpq(0), mpq(1)
        k = exponential_search(a, p, q, direction.LEFT)
        x = binary_search(a, p, q, (1 << (k-1))-1, (1 << k)-1, direction.LEFT)
        low = mpq(q.numerator + x * p.numerator,
                  q.denominator + x * p.denominator)
        high = mpq(q.numerator + (x-1) * p.numerator,
                   q.denominator + (x-1) * p.denominator)
        self.assertTrue(low <= a <= high)

    def test_binary_search_right(self):
        a = mpq(9, 14)
        p, q = mpq(0), mpq(1)
        k = exponential_search(a, p, q, direction.RIGHT)
        x = binary_search(a, p, q, (1 << (k-1))-1, (1 << k)-1, direction.RIGHT)
        high = mpq(p.numerator + (x-1) * q.numerator,
                   p.denominator + (x-1) * q.denominator)
        low = mpq(p.numerator + x * q.numerator,
                  p.denominator + x * q.denominator)
        self.assertTrue(high <= a <= low)

    def test_rational_search_01(self):
        p, q = mpq(0), mpq(1)

        a = float(mpq(9, 11))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(6, 7))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(11, 14))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(11, 15))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(13, 18))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(12, 17))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(9, 14))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(12, 19))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(13, 21))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(11, 19))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(9, 16))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(5, 11))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(7, 16))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(7, 17))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(7, 18))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(5, 14))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(4, 13))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(5, 18))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(3, 13))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(3, 14))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(2, 11))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(5, 17))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(4, 15))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(1, 7))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(10, 17))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(6, 11))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(8, 19))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(8, 21))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(7, 19))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(11, 18))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(9, 13))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)

        a = float(mpq(10, 13))
        res = rational_search(a, p, q, direction.LEFT)
        self.assertTrue(res == a)


if __name__ == '__main__':
    unittest.main()
