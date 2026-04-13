from enum import Enum
from itertools import combinations
import unittest
from gmpy2 import mpq, sqrt


class root_sign(Enum):
    PLUS, MINUS = 1, -1


def flip_sign(sign):
    return root_sign.MINUS if sign == root_sign.PLUS else root_sign.PLUS


class deg2root:
    """ maintain a + s * sqrt{b} """
    def __init__(self, a=mpq(0), b=mpq(0), s=root_sign.PLUS):
        self.__a, self.__b, self.__s = a, b, s

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def s(self):
        return self.__s

    def __compare_with_zero(self):
        if self.b == 0:
            return -1 if self.a < 0 else 1 if self.a > 0 else 0

        if self.s == root_sign.PLUS:
            if self.a >= 0:
                return 1
            sq = self.a * self.a
            return 1 if self.b > sq else -1 if self.b < sq else 0
        else:
            if self.a <= 0:
                return -1
            sq = self.a * self.a
            return -1 if self.b > sq else 1 if self.b < sq else 0

    def __comp(self, other):
        tmp, flipper = deg2root(self.a - other.a, self.b, self.s), 1
        if other.s == root_sign.MINUS:
            tmp = deg2root(-tmp.a, tmp.b, flip_sign(tmp.s))
            flipper = -1
        cmp0 = tmp.__compare_with_zero()
        if cmp0 < 0:
            return -flipper
        if cmp0 == 0:
            if other.b == 0:
                return 0
            if other.b > 0:
                return -flipper
        tmp2 = deg2root(tmp.a * tmp.a + tmp.b - other.b,
                        tmp.b * tmp.a * tmp.a * 4,
                        tmp.s if tmp.a >= 0 else flip_sign(tmp.s))
        cmp = tmp2.__compare_with_zero()
        if cmp < 0:
            return -flipper
        if cmp > 0:
            return flipper
        return 0

    def __lt__(self, other):
        return self.__comp(other) < 0

    def __le__(self, other):
        return self.__comp(other) <= 0

    def __gt__(self, other):
        return self.__comp(other) > 0

    def __ge__(self, other):
        return self.__comp(other) >= 0

    def __eq__(self, other):
        return self.__comp(other) == 0

    def __ne__(self, other):
        return self.__comp(other) != 0

    def __repr__(self):
        head = f"{self.to_double()} = {float(self.a)}"
        sgn = " + " if self.s == root_sign.PLUS else " - "
        tail = f"sqrt({float(self.b)})"
        return head + sgn + tail

    def to_double(self):
        _out, _in = float(self.a), float(self.b)
        return _out + self.s.value * float(sqrt(_in))

    def __float__(self):
        return self.to_double()

    def __add__(self, t):
        return deg2root(self.__a + t, self.__b, self.__s)

    def __sub__(self, t):
        return deg2root(self.__a - t, self.__b, self.__s)

    def __mul__(self, t):
        return deg2root(self.__a * t, self.__b * t * t, self.__s)

    def __truediv__(self, t):
        return deg2root(self.__a / t, self.__b / (t * t), self.__s)


def clamp(t, lower=None, upper=None):
    if lower is None:
        one, zero = mpq(1), mpq(0)
        t = min(t, one)
        t = max(t, zero)
    else:
        t = min(t, upper)
        t = max(t, lower)
    return t


def clip(t, lower, upper):
    return max(min(t, upper), lower)


class TestDeg2Root(unittest.TestCase):
    def test_three(self):
        r1 = deg2root(mpq(1, 1), mpq(4, 1), root_sign.PLUS)
        self.assertEqual(r1.to_double(), 3)

    def test_minus_one(self):
        r2 = deg2root(mpq(1, 1), mpq(4, 1), root_sign.MINUS)
        self.assertEqual(r2.to_double(), -1)

    def test_three_again(self):
        r3 = deg2root(mpq(3, 1), mpq(0, 1), root_sign.PLUS)
        self.assertEqual(r3.to_double(), 3)

    def test_minus_three(self):
        r4 = deg2root(mpq(0, 1), mpq(9, 1), root_sign.MINUS)
        self.assertEqual(r4.to_double(), -3)

    def test_plus_three(self):
        r5 = deg2root(mpq(0, 1), mpq(9, 1), root_sign.PLUS)
        self.assertEqual(r5.to_double(), 3)

    # def test_r1_compare_with_zero(self):
    #     r1 = deg2root(mpq(1, 1), mpq(4, 1), root_sign.PLUS)
    #     self.assertGreater(r1.compare_with_zero(), 0)

    # def test_r2_compare_with_zero(self):
    #     r2 = deg2root(mpq(1, 1), mpq(4, 1), root_sign.MINUS)
    #     self.assertLess(r2.compare_with_zero(), 0)

    # def test_r3_compare_with_zero(self):
    #     r3 = deg2root(mpq(3, 1), mpq(0, 1), root_sign.PLUS)
    #     self.assertGreater(r3.compare_with_zero(), 0)

    # def test_r4_compare_with_zero(self):
    #     r4 = deg2root(mpq(0, 1), mpq(9, 1), root_sign.MINUS)
    #     self.assertLess(r4.compare_with_zero(), 0)

    # def test_r5_compare_with_zero(self):
    #     r5 = deg2root(mpq(0, 1), mpq(9, 1), root_sign.PLUS)
    #     self.assertGreater(r5.compare_with_zero(), 0)

    def test_r1_is_not_equal_to_r2(self):
        r1 = deg2root(mpq(1, 1), mpq(4, 1), root_sign.PLUS)
        r2 = deg2root(mpq(1, 1), mpq(4, 1), root_sign.MINUS)
        self.assertTrue(r1 != r2)

    def test_r1_is_equal_to_r5(self):
        r1 = deg2root(mpq(1, 1), mpq(4, 1), root_sign.PLUS)
        r5 = deg2root(mpq(0, 1), mpq(9, 1), root_sign.PLUS)
        self.assertTrue(r1 == r5)

    def test_r2_is_less_than_r1(self):
        r1 = deg2root(mpq(1, 1), mpq(4, 1), root_sign.PLUS)
        r2 = deg2root(mpq(1, 1), mpq(4, 1), root_sign.MINUS)
        self.assertTrue(r2 < r1)

    def test_r4_is_less_than_r5(self):
        r4 = deg2root(mpq(0, 1), mpq(9, 1), root_sign.MINUS)
        r5 = deg2root(mpq(0, 1), mpq(9, 1), root_sign.PLUS)
        self.assertTrue(r4 < r5)

    def test_r2_is_less_than_r3(self):
        r2 = deg2root(mpq(1, 1), mpq(4, 1), root_sign.MINUS)
        r3 = deg2root(mpq(3, 1), mpq(0, 1), root_sign.PLUS)
        self.assertTrue(r2 < r3)

    def test_not_r3_is_less_than_r1(self):
        r1 = deg2root(mpq(1, 1), mpq(4, 1), root_sign.PLUS)
        r3 = deg2root(mpq(3, 1), mpq(0, 1), root_sign.PLUS)
        self.assertFalse(r3 < r1)

    def test_consistency_between_internal_comp_and_to_double(self):
        roots = [
            deg2root(mpq(1, 1), mpq(4, 1), root_sign.PLUS),
            deg2root(mpq(1, 1), mpq(4, 1), root_sign.MINUS),
            deg2root(mpq(3, 1), mpq(0, 1), root_sign.PLUS),
            deg2root(mpq(0, 1), mpq(9, 1), root_sign.MINUS),
            deg2root(mpq(0, 1), mpq(9, 1), root_sign.PLUS),
            deg2root(mpq(1, 2), mpq(2, 1), root_sign.PLUS),
            deg2root(mpq(1, 2), mpq(2, 1), root_sign.MINUS),
            deg2root(mpq(-3, 1), mpq(5, 1), root_sign.PLUS),
            deg2root(mpq(4, 1), mpq(7, 1), root_sign.MINUS)
        ]
        for r, s in combinations(roots, 2):
            diff = r.to_double() - s.to_double()
            cmp = 0 if r == s else -1 if r < s else 1 if r > s else 999
            """ sign of diffeence should agree """
            if diff < -1e-9:
                self.assertTrue(cmp < 0)
            elif diff > 1e-9:
                self.assertTrue(cmp > 0)
            else:
                self.assertTrue(cmp == 0)

            """ symmetry """
            cmp1 = -1 if r < s else 1 if r > s else 0
            cmp2 = -1 if s < r else 1 if s > r else 0
            self.assertTrue(cmp1 == -cmp2)


if __name__ == '__main__':
    unittest.main()
