from math import isclose
from functools import reduce
from unittest import main, TestCase
from gmpy2 import next_prime


def euclid_alg(a, b):
    """ compute greatest common divisor with Euclidean algorithm """
    assert (a > 0 and b > 0 and isinstance(a, int) and isinstance(b, int))
    stack = [(a, b) if a > b else (b, a)]
    while stack:
        a, b = stack.pop()
        if (r := a - b * (q := a // b)) == 0:
            return b
        stack.append((b, r))


class test_euclid(TestCase):
    def test_wikipedia_example1(self):
        self.assertEqual(euclid_alg(1071, 462), 21)
        self.assertEqual(euclid_alg(1071, 1029), 21)

    def test_same_number(self):
        self.assertEqual(euclid_alg(3, 3), 3)
        self.assertEqual(euclid_alg(5, 5), 5)

    def test_with_one(self):
        self.assertEqual(euclid_alg(3, 1), 1)
        self.assertEqual(euclid_alg(1, 3), 1)

    def test_with_both_prime(self):
        a, b = next_prime(11111), next_prime(3333)
        self.assertEqual(euclid_alg(int(a), int(b)), 1)


if __name__ == '__main__':
    main()
