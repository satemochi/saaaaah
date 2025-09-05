from functools import cmp_to_key
from matplotlib import pyplot as plt


def cmp(p1, p2):
    (x1, y1), (x2, y2) = p1, p2

    d1, d2 = x1 > y1, x2 > y2
    a1, a2 = x1 > -y1, x2 > -y2

    if (qa := (d1 << 1) + a1) != (qb := (d2 << 1) + a2):
        return (0x6c >> qa * 2 & 6) - (0x6c >> qb * 2 & 6)

    d1 ^= a1
    p, q = x1 * y2, x2 * y1
    na, nb = q * (1 - d1) - p * d1, p * (1 - d1) - q * d1

    return (na > nb) - (na < nb)


def __is_right_turn(p, q, r):
    (x1, y1), (x2, y2), (x3, y3) = p, q, r
    return x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1) > 0


def gen(n=77, s=9):
    from random import random, seed
    seed(s)
    return [(random(), random()) for i in range(n)]


if __name__ == '__main__':
    pts = gen()
    plt.scatter([x for x, _ in pts], [y for _, y in pts], color='#33cc33')

    ch = []
    ox, oy = min(pts, key=lambda p: p[1])
    ch.append((ox, oy))
    for x, y in sorted(((x-ox, y-oy) for x, y in pts if x != ox or y != oy),
                       key=cmp_to_key(cmp)):
        if len(ch) < 2:
            ch.append((x+ox, y+oy))
            continue
        while __is_right_turn(ch[-2], ch[-1], (x+ox, y+oy)):
            ch.pop()
        ch.append((x+ox, y+oy))
        plt.cla()
        plt.scatter([x for x, _ in pts], [y for _, y in pts], color='#33cc33')
        plt.plot([x for x, _ in ch], [y for _, y in ch], zorder=-10)

        plt.gca().set_xlim(-0.05, 1.05)
        plt.gca().set_ylim(-0.05, 1.05)
        plt.gca().set_aspect('equal')
        plt.gca().axis('off')
        plt.tight_layout()
        plt.draw()
        plt.pause(0.1)
    plt.pause(1.0)

    plt.cla()
    plt.scatter([x for x, _ in pts], [y for _, y in pts], color='#33cc33')
    plt.gca().add_patch(plt.Polygon(ch, alpha=0.3))
    plt.gca().set_xlim(-0.05, 1.05)
    plt.gca().set_ylim(-0.05, 1.05)
    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    plt.show()
