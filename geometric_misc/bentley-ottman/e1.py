import random
from matplotlib import pyplot as plt
from line_intersections import line_intersections


def gen(n, seed=None):
    random.seed(seed)
    return [((random.random(), random.random()),
             (random.random(), random.random())) for i in xrange(n)]


def plot_segs(segs):
    for (x1, y1), (x2, y2) in segs:
        plt.plot([x1, x2], [y1, y2])


if __name__ == '__main__':
    n = 8
    segs = gen(n, 1)
    plot_segs(segs)

    li = line_intersections(segs)
    for x, y in li.search():
        plt.scatter([x], [y])

    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig('a1.png', bbox_inches='tight')
    plt.show()
