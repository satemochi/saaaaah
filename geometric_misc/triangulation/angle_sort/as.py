from functools import cmp_to_key
from random import random, seed
from matplotlib import pyplot as plt


__o = (0, 0)


def cmp(p1, p2):
    """ Sorting points in plane with the argument
        see StackOverflow
            Fastest way to sort vectors by angle
                    without actually computing that angle
        https://stackoverflow.com/questions/16542042/fastest-way-to-sort-vectors-by-angle-without-actually-computing-that-angle/27253590
    """
    x1, y1 = (p1[0]-__o[0], p1[1]-__o[1])
    x2, y2 = (p2[0]-__o[0], p2[1]-__o[1])

    d1, d2 = x1 > y1, x2 > y2
    a1, a2 = x1 > -y1, x2 > -y2

    if (qa := (d1 << 1) + a1) != (qb := (d2 << 1) + a2):
        return (0x6c >> qa * 2 & 6) - (0x6c >> qb * 2 & 6)

    d1 ^= a1
    p, q = x1 * y2, x2 * y1
    na, nb = q * (1 - d1) - p * d1, p * (1 - d1) - q * d1

    return (na > nb) - (na < nb)


def gen(n=30, s=9):
    seed(s)
    return ((random(), random()), [(random(), random()) for i in range(n)])


if __name__ == '__main__':
    __o, pts = gen()
    plt.scatter([__o[0],], [__o[1],], color='r')

    plt.tight_layout()
    plt.gca().set_aspect('equal')
    plt.gca().set_xlim(-0.05, 1.05)
    plt.gca().set_ylim(-0.05, 1.05)
    for x, y in pts:
        plt.scatter([x,], [y,], color='#33cc33')
        plt.draw()
        plt.pause(0.001)

    for i, (x, y) in enumerate(sorted(pts, key=cmp_to_key(cmp))):
        plt.scatter([x,], [y,], color='darkgreen')
        plt.plot([__o[0], x], [__o[1], y], color='darkgreen', zorder=-10)
        plt.draw()
        # plt.savefig(f'as_{str(i).zfill(2)}.png', bbox_inches='tight')
        plt.pause(0.001)

    plt.show()
