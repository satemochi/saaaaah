from random import randint, seed, choices


def k_means_pp_init_clusters(pts, k, s=None):
    seed(s)
    centers = [pts[randint(0, len(pts)-1)]]
    while len(centers) < k:
        w = [min(_norm(*p, *pc) for pc in centers) for p in pts]
        centers.append(pts[choices(range(len(pts)), weights=w)[0]])
    return {p: min((_norm(*p, *pc), i) for i, pc in enumerate(centers))[1]
            for p in pts}


def _norm(x0, y0, x1, y1):
    return (x0-x1)**2 + (y0-y1)**2


def k_means(pts, k, clusters=None, s=None):
    if clusters is None:
        _, clusters = seed(s), {p: randint(0, k-1) for p in pts}
    while _rearrange(clusters, k):
        pass
    return clusters


def _rearrange(clusters, k):
    centers, modified = _get_centers(clusters, k), False
    for p, i in clusters.items():
        clusters[p] = min((_norm(*p, *q), j) for j, q in enumerate(centers))[1]
        modified = True if i != clusters[p] else modified
    return modified


def _get_centers(cluster, k):
    m = {i: (0, 0, 0) for i in range(k)}
    for (x, y), i in cluster.items():
        m[i] = (m[i][0]+x, m[i][1]+y, m[i][2]+1)
    return [(m[i][0]/m[i][2], m[i][1]/m[i][2])
            if m[i][2] else (float('inf'), float('inf')) for i in m]


def gen(n, s):
    from random import random
    seed(s)
    return [(random(), random()) for i in range(n)]


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    from matplotlib.colors import TABLEAU_COLORS
    n, k, s = 200, 5, 0
    pts = gen(n, s)
    # clusters = k_means(pts, k, s=s)
    clusters = k_means(pts, k, clusters=k_means_pp_init_clusters(pts, k, s))

    colors = list(TABLEAU_COLORS.values())
    for i in range(k):
        pi = [p for p, j in clusters.items() if i == j]
        plt.scatter([x for x, _ in pi], [y for _, y in pi], c=colors[i])

    plt.gca().set_aspect('equal')
    plt.tight_layout()
    plt.savefig('k_means_pp_ex2.png', bbox_inches='tight')
    plt.show()
