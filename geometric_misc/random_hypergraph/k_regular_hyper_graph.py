from functools import reduce
from heapq import heappop, heappush
from itertools import combinations
from operator import add
from random import sample, seed
from matplotlib import pyplot as plt
import networkx as nx


def random_k_regular_hyper_graph(n, k):
    """ Generate a random k-regular / k-uniform / n-vertex hypergraph

    Parameters
    ----------
        n: number of vertices
        k: uniformity and regularity

    Returns
    -------
        dict: from a hyper-edge to incident vertices
    """
    while ((hyper_edges := __gale_shapley(n, k)) is None
            or __test_multiedge_violation(hyper_edges)):
        pass
    return hyper_edges


def __gale_shapley(n, k):
    vp = {i: iter(range(n, 2*n)) for i in range(n)}
    ep = {n+i: sample(range(n), n) for i in range(n)}
    stack, m = reduce(add, [[x]*k for x in vp]), {}
    while stack:
        try:
            e = next(vp[(v := stack.pop())])
        except(StopIteration):
            return
        if e not in m:
            m[e] = [(-ep[e][v], v)]
        else:
            heappush(m[e], (-ep[e][v], v))
            if len(m[e]) > k:
                _, w = heappop(m[e])
                stack.append(w)
    return {e: [v for _, v in m[e]] for e in m}


def __test_multiedge_violation(edges):
    return any(set(x) == set(y) for x, y in combinations(edges.values(), 2))


def draw(edict):
    from pprint import pprint
    pprint(edict)
    pos = get_pos(n := len(edict))
    g = nx.Graph()
    for e in edict:
        g.add_edges_from([(e, v) for v in edict[e]])
    for v, c in zip([range(n), range(n, 2*n)], ['#ffcccc', '#ccccff']):
        nodes = nx.draw_networkx_nodes(g, pos, nodelist=v, node_color=c)
        nodes.set_edgecolor('black')
    nx.draw_networkx_edges(g, pos, edge_color='g', alpha=0.35)
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
    draw(random_k_regular_hyper_graph(7, 3))
