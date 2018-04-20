from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib import collections as mc
import numpy as np


#def get_instance(n=10, seed=0):
def get_instance(n=10, seed=None):
    np.random.seed(seed)
    return np.random.random((n, 2))


def draw_instance(P):
    plt.gca().set_aspect('equal')
    plt.gca().scatter(P[:,0], P[:,1], color='r', s=16, zorder=10)


def draw_grid(L, x, y, n, epsilon=4.):
    d = epsilon * L / (2. * n)
    lines = []
    for i in range(1, int(np.floor(2 * n / epsilon))):
        lines.append(((x, y + d * i), (x + L, y + d * i)))
        lines.append(((x + d * i, y), (x + d * i, y + L)))
    plt.gca().add_collection(mc.LineCollection(lines))


def bounding_square(P):
    _max, _min, _ave = P.max(axis=0), P.min(axis=0), np.average(P, axis=0)
    diffs = _max - _min
    L, Ldim = np.max(diffs), np.argmax(diffs)
    ex = Ldim ^ 1

    p = [0, 0]
    p[Ldim] = _min[Ldim]
    if _ave[ex] + L/2. > _max[ex] and _ave[ex] - L/2. < _min[ex]:
        p[ex] = _ave[ex] - L/2.
    elif _ave[ex] + L/2. < _max[ex]:
        p[ex] = _max[ex] - L
    else:
        p[ex] = _min[ex]

    return (L, p)


def draw_bounding_square(L, p):
    sq = patches.Rectangle(p, L, L, fill=False)
    plt.gca().add_patch(sq)


def nice_instance(L, x, y, n, epsilon=4., is_draw=False):
    d = epsilon * L / (2. * n)
    grid_points = []
    for p in P:
        i, j = int((p[0] - x) / d), int((p[1] - y) / d)
        di, dj = d * i + x, d * j + y
        dx = di if abs(di - p[0]) < abs(di + d - p[0]) else di + d
        dy = dj if abs(dj - p[1]) < abs(dj + d - p[1]) else dj + d
        grid_points.append((dx, dy))
    Q = np.array(grid_points)
    if is_draw:
        plt.gca().scatter(Q[:,0], Q[:,1], color='b', s=16, zorder=10)
    f = (8. * n) / (epsilon * L)
    return np.array([(q - (x, y)) * f for q in Q])


if __name__ == '__main__':
    P = get_instance()
    L, (x, y) = bounding_square(P)
    Q = nice_instance(L, x, y, len(P), is_draw=True)
    print P
    print Q

    draw_instance(P)
    draw_bounding_square(L, (x, y))
    draw_grid(L, x, y, len(P))

    plt.autoscale()
    plt.tight_layout()
    plt.savefig('lemma10.1.png', bbox_inches='tight')
    plt.show()
