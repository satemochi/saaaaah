from itertools import combinations
from random import random, seed
from matplotlib import pyplot as plt
import networkx as nx
from split_tree import split_tree


def gen(n=100, s=0):
    seed(s)
    return [(random(), random()) for i in range(n)]


def test_t_paths(pts, spanner_edges, t):
    g = nx.Graph(spanner_edges)
    for p, q in g.edges:
        g[p][q]['weight'] = _dis(p, q)
    length = nx.shortest_path_length
    return all(length(g, source=p, target=q, weight='weight') < t * _dis(p, q)
               for p, q in combinations(pts, 2))


def _dis(p, q):
    return ((p[0]-q[0])**2 + (p[1]-q[1])**2)**0.5


if __name__ == '__main__':
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.set_aspect('equal')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax2.set_aspect('equal')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)

    n = 100
    pts = gen(n)

    ax1.set_title(f'The numbe of nodes = {n} ({n*(n-1)//2} edges)')
    for (x1, y1), (x2, y2) in combinations(pts, 2):
        ax1.plot([x1, x2], [y1, y2], c='b', alpha=0.1)
    ax1.scatter([x for x, _ in pts], [y for _, y in pts], c='orange',
                edgecolors='k', zorder=10, alpha=0.7)

    size = 20
    for i, t in ((i, 1.1+0.1*i) for i in range(size)):
        ax2.cla()
        ax2.set_aspect('equal')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)

        s = 4 * (t+1) / (t-1)
        spanner_edges = [(next(iter(a)), next(iter(b)))
                         for a, b in split_tree(pts).wspd(s)]
        print(n*(n-1)//2, len(spanner_edges))
        ax2.set_title(f'stretch factor = {round(t, 2)} / ' +
                      f'spanner edges = {len(spanner_edges)}')
        for (x1, y1), (x2, y2) in spanner_edges:
            ax2.plot([x1, x2], [y1, y2], c='b', alpha=0.1)
        ax2.scatter([x for x, _ in pts], [y for _, y in pts], c='orange',
                    edgecolors='k', zorder=10, alpha=0.7)
        plt.draw()
        # plt.savefig(f't_spanner_{str(i).zfill(2)}.png', bbox_inches='tight')
        # print(test_t_paths(pts, spanner_edges, t))
        plt.pause(0.1)

    plt.tight_layout()
    plt.show()
