from itertools import combinations
from random import seed, random
from gmpy2 import xmpz
from matplotlib import pyplot as plt
import networkx as nx


def gen(n=16):
    seed(7)
    g = nx.complete_graph(n)
    pos = {i: (random(), random()) for i in range(n)}
    for u, v in combinations(range(n), 2):
        g[u][v]['w'] = (pos[u][0] - pos[v][0])**2 + (pos[u][1] - pos[v][1])**2
    return g, pos


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
