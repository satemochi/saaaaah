import numpy as np


def gen(n=100, s=10):
    return (np.sort(np.random.choice(range(1, n), s)),
            np.sort(np.random.choice(range(1, n), s)))


def min_ratio(A, B):
    return min([float(a) / b for a, b in zip(A, B)])


def max_ratio(A, B):
    return max([float(a) / b for a, b in zip(A, B)])


def sum_ratio(A, B):
    return float(np.sum(A)) / np.sum(B)


if __name__ == '__main__':
    for i in range(5):
        a, b = gen()
        print a
        print b
        print min_ratio(a, b), sum_ratio(a, b), max_ratio(a, b)
        print True if min_ratio(a, b) <= sum_ratio(a, b) and \
                      sum_ratio(a, b) <= max_ratio(a, b) else False
