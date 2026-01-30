from functools import reduce
from matplotlib import pyplot as plt
import numpy as np


def area(P):
    return (reduce(lambda x, p: x + (p[1][0] - p[0][0]) * (p[1][1] + p[0][1]),
                   zip(P, P[1:]), 0)
            + (P[0][0] - P[-1][0]) * (P[0][1] + P[-1][1])) * 0.5


def PolyArea(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def gen():
    return [(0, 5), (3, 10), (9, 9), (13, 10), (16, 6),
            (11, 8), (5, 6), (12, 4), (5, 3)]


if __name__ == '__main__':
    plt.gca().add_patch(plt.Polygon((pts := gen()), edgecolor='k', alpha=0.3))

    print(area(pts))
    print(PolyArea([x for x, _ in pts], [y for _, y in pts]))

    plt.gca().set_aspect('equal')
    plt.gca().set_xlim(-1, 17)
    plt.gca().set_ylim(0, 12)
    plt.grid()
    plt.tight_layout()
    plt.show()
