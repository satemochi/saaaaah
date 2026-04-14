from functools import cached_property, reduce
from unittest import TestCase, main
from matplotlib import pyplot as plt
import numpy as np


class dual_number:
    """ ref) Computing Macroxela (2025.06.18):
            "How Do Computers Compute Derivatives?" [blog] """
    def __init__(self, real, dual):
        self.__real, self.__dual = real, dual

    @property
    def r(self):
        return self.__real

    @property
    def d(self):
        return self.__dual

    def __repr__(self):
        return (f"{self.r} + {self.d}ε" if self.r != 0 and self.d > 0 else
                f"{self.r} - {abs(self.d)}ε" if self.r != 0 and self.d < 0 else
                f"{self.r}" if self.r != 0 else
                f"{self.d}ε" if self.r == 0 and self.d != 0 else "0")

    def __neg__(self):
        return dual_number(-self.__real, -self.__dual)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return dual_number(self.r + other, self.d)
        if isinstance(other, dual_number):
            return dual_number(self.r + other.r, self.d + other.d)
        return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return dual_number(self.r - other, self.d)
        if isinstance(other, dual_number):
            return dual_number(self.r - other.r, self.d - other.d)
        return NotImplemented

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return dual_number(self.r * other, self.d * other)
        if isinstance(other, dual_number):
            coeff1 = self.r * other.r
            coeff2 = self.r * other.d + self.d * other.r
            return dual_number(coeff1, coeff2)
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return dual_number(self.r / other, self.d / other)
        if isinstance(other, dual_number):
            return self * other.conjugate() / other.r**2
        return NotImplemented

    def conjugate(self):
        return dual_number(self.r, -self.d)

    def __rtruediv__(self, other):
        return other * self.conjugate() / self.r**2

    def __pow__(self, exponent):
        if isinstance(exponent, dual_number):
            raise ValueError("Powers between two dual numbers is not defined.")
        new_real = self.r ** exponent
        new_dual = exponent * (self.r ** (exponent - 1)) * self.d
        return dual_number(new_real, new_dual)


class test_dual_numbers(TestCase):
    def test_repr(self):
        r, d = 1, 5
        self.assertEqual(f"{r} + {d}ε", str(dual_number(r, d)))
        r, d = -1, 5
        self.assertEqual(f"{r} + {d}ε", str(dual_number(r, d)))
        r, d = 1, -5
        self.assertEqual(f"{r} - {abs(d)}ε", str(dual_number(r, d)))
        r, d = 0, 5
        self.assertEqual(f"{d}ε", str(dual_number(r, d)))
        r, d = 0, -5
        self.assertEqual(f"{d}ε", str(dual_number(r, d)))
        r, d = 0, 0
        self.assertEqual(f"0", str(dual_number(r, d)))

    def test_neg(self):
        r, d = 1, 5
        self.assertEqual(-1, -dual_number(1, 5).r)
        self.assertEqual(-5, -dual_number(1, 5).d)

    def test_add_int(self):
        r, d = 1, 5
        a = 1000
        self.assertEqual(1001, (dual_number(1, 5) + a).r)
        self.assertEqual(1001, (a + dual_number(1, 5)).r)
        self.assertEqual(5, (dual_number(1, 5) + a).d)
        self.assertEqual(5, (a + dual_number(1, 5)).d)
        a = -1000
        self.assertEqual(-999, (dual_number(1, 5) + a).r)
        self.assertEqual(-999, (a + dual_number(1, 5)).r)

    def test_add_float(self):
        r, d = 1, 5
        a = 1e4
        self.assertEqual(10001, (dual_number(1, 5) + a).r)
        self.assertEqual(10001, (a + dual_number(1, 5)).r)
        self.assertEqual(5, (dual_number(1, 5) + a).d)
        self.assertEqual(5, (a + dual_number(1, 5)).d)
        a = -1e4
        self.assertEqual(-9999, (dual_number(1, 5) + a).r)
        self.assertEqual(-9999, (a + dual_number(1, 5)).r)

    def test_add_dual_number(self):
        n1, n2 = dual_number(1, 5), dual_number(30, 500)
        self.assertEqual(31, (n1 + n2).r)
        self.assertEqual(505, (n1 + n2).d)


class polynomial:
    def __init__(self, a):
        r""" f(x) = \sum_i a_i x^i = a_0 + a_1 x + \cdot + a_d * x^d. """
        self.__a = a

    @cached_property
    def dim(self):
        return len(self.__a) - 1

    def __repr__(self):
        return "".join([self.__s(i) for i in reversed(range(self.dim+1))])

    def __getitem__(self, i):
        return self.__a[i]

    def __s(self, i):
        if i == self.dim or i == -1:
            return f"${self[-1]}x^{self.dim}"
        if i == 0:
            return f" + {self[0]}$" if self[0] >= 0 else f" - {abs(self[0])}$"
        if i == 1:
            return f" + {self[1]}x" if self[1] >= 0 else f" - {abs(self[1])}x"
        return (f" + {self[i]}x^{i}" if self[i] >= 0 else
                f" - {abs(self[i])}x^{i}")

    def at(self, x):    # Horner's method
        return (reduce(lambda y, ai: (y + ai) * x, reversed(self.__a[1:]), 0)
                + self.__a[0])

    def draw(self, xmin=-30, xmax=30):
        x = np.linspace(xmin, xmax, 100)
        y = [self.at(xi) for xi in x]
        plt.plot(x, y, label=str(self))


class line:
    def __init__(self, a, p):
        """ line with slope `a` passing `p` """
        self.__a, self.__x, self.__y = a, p[0], p[1]

    def y(self, x):
        return self.__a * (x - self.__x) + float(self.__y)

    def draw(self, xmin=-30, xmax=30, **kwargs):
        if self.__a is None:
            plt.plot([self.__x, self.__x], [xmin, xmax], **kwargs)
        else:
            plt.plot([xmin, xmax], [self.y(xmin), self.y(xmax)], **kwargs)


if __name__ == '__main__':
    f = polynomial([1, -3, 2, -3/5, 1/200])
    f.draw()
    plt.legend(loc="best")

    a = dual_number(5, 1)
    print("x =", a.r, ": (y, y') =", (dual := f.at(a)))
    line(dual.d, (a.r, dual.r)).draw()
    plt.scatter([a.r], [dual.r], ec='k', zorder=10)

    a = dual_number(22, 1)
    print("x =", a.r, ": (y, y') =", (dual := f.at(a)))
    line(dual.d, (a.r, dual.r)).draw()
    plt.scatter([a.r], [dual.r], ec='k', zorder=10)

    a = dual_number(-15, 1)
    print("x =", a.r, ": (y, y') =", (dual := f.at(a)))
    line(dual.d, (a.r, dual.r)).draw()
    plt.scatter([a.r], [dual.r], ec='k', zorder=10)

    plt.autoscale()
    plt.tight_layout()
    # plt.savefig('dual_number_ex1.png', bbox_inches='tight')
    plt.show()

#    main()
