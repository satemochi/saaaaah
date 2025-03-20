from collections import defaultdict
from itertools import combinations
from random import seed, random
from gmpy2 import xmpz
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np


def gen(n=18):
    seed(7)
    g = nx.complete_graph(n)
    pos = {i: (random(), random()) for i in range(n)}
    for u, v in combinations(range(n), 2):
        g[u][v]['w'] = (pos[u][0] - pos[v][0])**2 + (pos[u][1] - pos[v][1])**2
    return g, pos


def tsp_min_plus(g):
    """
        M. Stoian (2024): "TSP escape O(2^n n^2) curse"
        ref.
            https://github.com/stoianmihail/FasterTSP/blob/main/TSP.ipynb
    """
    c, partition = nx.to_numpy_array(g, weight='w'), defaultdict(list)
    for subset in range(1, 1 << (n := g.order())):
        partition[xmpz(subset).bit_count()].append(subset)
    dp = np.full((1 << n, n), np.inf)
    dp[1][0] = 0
    for i in range(2, n + 1):
        for b in range(0, len(partition[i-1]), n):
            batch = np.asarray(partition[i-1][b:b + n])
            p = min_plus_prod(dp[batch], c)
            for j, subset in enumerate(batch):
                for k in xmpz(subset).iter_clear(stop=n):
                    dp[a][k] = min(dp[(a := subset | (1 << k))][k], p[j][k])
    return min(dp[(1 << n) - 1][k] + c[k][0] for k in range(n))


def min_plus_prod(A, B):
    assert A.shape[1] == B.shape[0]
    ret = np.full((A.shape[0], B.shape[1]), np.inf)
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                ret[i][j] = min(ret[i][j], A[i][k] + B[k][j])
    return ret


def bellman_held_karp_1962(g):
    L = {}
    for i in range(1, 1 << (s := g.order() - 1)):
        for v in xmpz(i).iter_set():
            if (a := (i ^ (1 << v))) == 0:
                L[i, v] = (g[s][v]['w'], (s,))
            else:
                L[i, v] = min((L[a, u][0] + g[u][v]['w'], L[a, u][1] + (u,))
                              for u in xmpz(a).iter_set())
    return min((L[(x := (1 << s) - 1), v][0] + g[s][v]['w'], L[x, v][1] + (v,))
               for v in range(s))


if __name__ == '__main__':
    g, pos = gen()

    _, c = bellman_held_karp_1962(g)
    print(_)
    print(tsp_min_plus(g))

    nx.draw_networkx_nodes(g, pos, node_color='#ffcccc').set_edgecolor('k')
    nx.draw_networkx_edges(g, pos, alpha=0.07)
    edges = [(c[i], c[i+1]) for i in range(-1, g.order()-1)]
    nx.draw_networkx_edges(g, pos, edge_color='g', width=2.5, alpha=0.5,
                           edgelist=edges)
    nx.draw_networkx_labels(g, pos)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    plt.show()
