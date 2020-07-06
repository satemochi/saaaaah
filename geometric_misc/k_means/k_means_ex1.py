from random import random, randint, seed
from matplotlib import pyplot as plt
from matplotlib.colors import TABLEAU_COLORS


def k_means(pts, k, s=None):
    clusters = _arrange_randomly(pts, k, s)
    while _rearrange(clusters, k):
        pass
    return clusters


def _arrange_randomly(pts, k, s):
    seed(s)
    return {p: randint(0, k-1) for p in pts}


def _rearrange(clusters, k):
    centers, modified = _get_centers(clusters, k), False
    for p, i in clusters.items():
        clusters[p] = min((_norm(*pm, *p), j) for j, pm in centers)[1]
        modified = True if i != clusters[p] else modified
    return modified


def _get_centers(cluster, k):
    m = {i: (0, 0, 0) for i in range(k)}
    for (x, y), i in cluster.items():
        m[i] = (m[i][0]+x, m[i][1]+y, m[i][2]+1)
    return [(i, (m[i][0]/m[i][2], m[i][1]/m[i][2]))
            if m[i][2] else (i, (float('inf'), float('inf'))) for i in m]


def _norm(x0, y0, x1, y1):
    return (x0-x1)**2 + (y0-y1)**2


def gen(n, s):
    seed(s)
    return [(random(), random()) for i in range(n)]


if __name__ == '__main__':
    n, k, s = 50, 5, 0
    clusters = k_means(gen(n, s), k, s)

    colors = list(TABLEAU_COLORS.values())
    for i in range(k):
        pi = [p for p, j in clusters.items() if i == j]
        plt.scatter([x for x, _ in pi], [y for _, y in pi], c=colors[i])

    plt.gca().set_aspect('equal')
    plt.tight_layout()
    # plt.savefig('k_means_ex1.png', bbox_inches='tight')
    plt.show()
