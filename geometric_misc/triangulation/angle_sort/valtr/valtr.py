from functools import cmp_to_key, reduce
from random import choice, sample, seed, shuffle
from matplotlib import pyplot as plt


def random_convex_set(n=5, C=100):
    """ random convex n-point set within 2d CxC (integer) grid
        ref) Pat Morin's implementation for Valtr's algorithm
            https://github.com/patmorin/randcon/blob/master/randcon.py
    """
    x, y = sample(range(C), n), sample(range(C), n)
    xmin, ymin = min(x), min(y)
    _x, _y = __get_vectors(x), __get_vectors(y)
    shuffle(_y)
    pts = list(reduce(lambda a, i: a + [(a[-1][0] + i[0], a[-1][1] + i[1])],
                      sorted(zip(_x, _y), key=cmp_to_key(__cmp)), [(0, 0)]))
    dx, dy = xmin - min(x for x, _ in pts), ymin - min(y for _, y in pts)
    return [(xi + dx, yi + dy) for xi, yi in pts[:-1]]


def __get_vectors(x):
    x1, x2 = __split_randomly(sorted(x))
    _ = x1 + list(reversed(x2)) + [x1[0]]
    return [xj - xi for xi, xj in zip(_, _[1:])]


def __split_randomly(x):
    _x, _y = [x[0]], []
    for xi in x[1:-1]:
        if choice((0, 1)):
            _x.append(xi)
        else:
            _y.append(xi)
    return _x, _y + [x[-1]]


def __cmp(p1, p2):
    """ angular sorting around origin """
    (x1, y1), (x2, y2) = p1, p2

    d1, d2 = x1 > y1, x2 > y2
    a1, a2 = x1 > -y1, x2 > -y2

    if (qa := (d1 << 1) + a1) != (qb := (d2 << 1) + a2):
        return (0x6c >> qa * 2 & 6) - (0x6c >> qb * 2 & 6)

    d1 ^= a1
    p, q = x1 * y2, x2 * y1
    na, nb = q * (1 - d1) - p * d1, p * (1 - d1) - q * d1

    return (na > nb) - (na < nb)


if __name__ == '__main__':
    seed(0)
    pts = random_convex_set(n := 30, C := 100)

    plt.gca().set_aspect('equal')
    plt.tight_layout()
    plt.gca().set_xlim(0, C)
    plt.gca().set_ylim(0, C)

    plt.plot([x for x, _ in pts] + [pts[0][0]],
             [y for _, y in pts] + [pts[0][1]], alpha=0.15)
    for i, (x, y) in enumerate(pts):
        plt.scatter([x,], [y,], color='#33cc33')
        plt.draw()
        # plt.savefig(f'valtr_{str(i).zfill(2)}.png', dpi=200)
        plt.pause(0.00001)

    plt.show()
