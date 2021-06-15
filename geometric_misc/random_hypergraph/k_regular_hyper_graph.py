from collections import defaultdict, ChainMap
from functools import reduce
from heapq import heappop, heappush
from itertools import combinations
from operator import add
from random import sample, seed
from matplotlib import pyplot as plt
import networkx as nx


def gen(n, k):
    """
    Generate a random k-regular / k-uniform / n-vertex hypergraph

    Parageters
    ----------
        n: number of vertices
        k: uniformity and regularity

    Returns
    -------
        dict: set of hyper-edges (from vertex to list)
    """
    hyper_edges = __gale_shapley(n, k)
    while hyper_edges is None or not __test(hyper_edges):
        hyper_edges = __gale_shapley(n, k)
    return hyper_edges


def __gale_shapley(n, k):
    vp = {i: iter(range(n, 2*n)) for i in range(n)}
    ep = {n+i: sample(range(n), n) for i in range(n)}
    stack = reduce(add, [[x]*k for x in vp])
    m = defaultdict(list)
    while stack:
        try:
            e = next(vp[(v := stack.pop())])
        except(StopIteration):
            return
        if e not in m:
            m[e].append((-ep[e][v], v))
        else:
            heappush(m[e], (-ep[e][v], v))
            if len(m[e]) > k:
                _, w = heappop(m[e])
                stack.append(w)
    return {e: [v for _, v in m[e]] for e in m}


def __test(edges):
    return all(set(x) != set(y) for x, y in combinations(edges.values(), 2))


def draw(edict):
    from pprint import pprint
    pprint(edict)
    pos = get_pos(n := len(edict))
    g = nx.Graph()
    for e in edict:
        g.add_edges_from([(e, v) for v in edict[e]])
    for v, c in zip([range(n), range(n, 2*n)], ['#ffcccc', '#ccccff']):
        nx.draw_networkx_nodes(g, pos, nodelist=v, node_color=c)
    nx.draw_networkx_edges(g, pos, alpha=0.25)
    nx.draw_networkx_labels(g, pos)
    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.autoscale()
    plt.tight_layout()
    # plt.savefig('regula_hyper_graph_ex1.png', bbox_inches='tight')
    plt.show()


def get_pos(n):
    pos = {v: (0, n-i) for i, v in enumerate(range(n))}
    pos.update({v: (n, n-i) for i, v in enumerate(range(n, 2*n))})
    return pos


if __name__ == '__main__':
    seed(4)
    draw(gen(7, 3))
