from matplotlib import pyplot as plt


def gift_wrapping(pts):
    """ [Assumption]: no collinear triple in `pts` """
    ch = [min(pts)]
    while True:
        q = next((targets := iter(_ for _ in pts if _ != ch[-1])))
        for r in targets:
            if __is_right_turn(ch[-1], q, r):
                q = r
        if q == ch[0]:
            break
        ch.append(q)
    return ch


def __is_right_turn(p, q, r):
    (x1, y1), (x2, y2), (x3, y3) = p, q, r
    return x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1) > 0


def gen(n=30, s=9):
    from random import random, seed
    seed(s)
    return [(random(), random()) for i in range(n)]


if __name__ == '__main__':
    pts = gen()
    plt.scatter([x for x, _ in pts], [y for _, y in pts], color='#ff6666')
    plt.gca().add_patch(plt.Polygon(gift_wrapping(pts), alpha=0.3, zorder=-10))

    plt.gca().set_xlim(-0.05, 1.05)
    plt.gca().set_ylim(-0.05, 1.05)
    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    plt.show()
