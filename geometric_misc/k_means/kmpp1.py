from random import random, randint, seed, uniform
from matplotlib import pyplot as plt
from matplotlib.colors import TABLEAU_COLORS


def k_means_pp_centers(pts, k):
    centers = [pts[randint(0, len(pts)-1)]]
    while len(centers) < k:
        centers.append(pts[_pickup(_get_distribution(pts, centers))])
    return {p : min((_norm(*p, *pc), i) for i, pc in enumerate(centers))[1]
            for p in pts}


def _pickup(dist):
    if (pivot := uniform(0, dist[-1][0])) < dist[0][0]:
        return 0
    for i in range(1, len(dist)):
        if dist[i-1][0] < pivot and pivot <= dist[i][0]:
            return dist[i][1]


def _get_distribution(pts, centers):
    s = [(min(_norm(*p, *pc) for pc in centers), i) for i, p in enumerate(pts)]
    for i in range(1, len(s)):
        s[i] = (s[i-1][0]+s[i][0], s[i][1])
    return s


def k_means(pts, k, clusters=None, s=None):
    if clusters is None:
        clusters = _random_arrange(pts, k, s)
    while _rearrange(clusters, k):
        pass
    return clusters


def _random_arrange(pts, k, s):
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
    n, k, s = 200, 5, 0
    pts = gen(n, s)
#    clusters = k_means(pts, k, s=s)
    clusters = k_means(pts, k, clusters=k_means_pp_centers(pts, k))

    colors = list(TABLEAU_COLORS.values())
    for i in range(k):
        pi = [p for p, j in clusters.items() if i == j]
        plt.scatter([x for x, _ in pi], [y for _, y in pi], c=colors[i])

    plt.gca().set_aspect('equal')
    plt.tight_layout()
    plt.savefig('k_means_ex1.png', bbox_inches='tight')
    plt.show()
