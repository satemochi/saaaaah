from random import random, randint, seed
from matplotlib import pyplot as plt
from matplotlib.colors import TABLEAU_COLORS
from shapely.geometry import MultiPoint
from descartes.patch import PolygonPatch


def k_means(pts, k, s=None):
    clusters = _random_arrange(pts, k, s)
    draw_cluster(clusters)
    cnt = 0
    while _rearrange(clusters, k):
        cnt += 1
        print(cnt)
        draw_cluster(clusters)
    return clusters


def _random_arrange(pts, k, s):
    seed(s)
    return {p: randint(0, k-1) for p in pts}


def _rearrange(clusters, k):
    centers, modified = _get_centers(clusters, k), False
    for p, i in clusters.items():
        clusters[p] = min((_norm(*pm, *p), j) for j, pm in centers.items())[1]
        if i != clusters[p]:
            modified = True
    return modified


def _get_centers(cluster, k):
    m = {i: (0, 0, 0) for i in range(k)}
    for (x, y), i in cluster.items():
        m[i] = (m[i][0]+x, m[i][1]+y, m[i][2]+1)
    return {i: (m[i][0]/m[i][2], m[i][1]/m[i][2])
            if m[i][2] else (float('inf'), float('inf')) for i in m}


def _norm(x0, y0, x1, y1):
    return (x0-x1)**2 + (y0-y1)**2


colors = list(TABLEAU_COLORS.values())

cnt = 0
def draw_cluster(clusters, interval=.5):
    global colors
    global cnt
    cnt += 1
    plt.cla()
    plt.gca().set_aspect('equal')
    plt.tight_layout()
    for i in range(k):
        pi = [p for p, j in clusters.items() if i == j]
        plt.scatter([x for x, _ in pi], [y for _, y in pi], c=colors[i])
        if len(pi) > 2:
            ch = PolygonPatch(MultiPoint(pi).convex_hull, alpha=0.1, zorder=-2,
                              facecolor=colors[i], edgecolor=colors[i])
            plt.gca().add_patch(ch)
    plt.draw()
    plt.savefig(f'k_means_anim_{cnt}.png', bbox_inches='tight')
    plt.pause(interval)


def gen(n, s):
    seed(s)
    return [(random(), random()) for i in range(n)]


if __name__ == '__main__':
    n, k, s = 100, 5, 0
    plt.scatter([0], [0])
    plt.draw()
    plt.savefig(f'k_means_anim_{cnt}.png', bbox_inches='tight')
    plt.pause(0.1)
    clusters = k_means(gen(n, s), k, s)
    plt.show()
