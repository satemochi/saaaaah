from tutte_embedding import tutte_embedding
from collections import defaultdict
import math
from operator import mul
import random
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np


def get_instance(r):
    g = nx.petersen_graph()
    pos = tutte_embedding(g).rpos()
    pos = {k: np.array(map(mul, v, [r, r])) for k, v in pos.items()}
    for u, v in g.edges():
        g[u][v]['weight'] = np.linalg.norm(pos[u] - pos[v])
    return g, pos


def get_distances(g):
    dists = dict(nx.all_pairs_dijkstra_path_length(g))
    max_dist = max(max(dists[u][v] for v in g.nodes()) for u in g.nodes())
    delta = 1
    while delta < max_dist:
        delta <<= 1
    return dists, int(math.log(delta, 2))


def random_parameter(log_delta, n):
    r0 = random.uniform(0.5, 1)
    ri = [(1 << i)*r0 for i in xrange(log_delta+1)]
    pi = range(n)
    random.shuffle(pi)
    return (ri, pi)


def hierarchical_decomposition(g, pos, dists, ri, pi):
    C = defaultdict(list)
    C[log_delta] = [set(g.nodes())]
    T = nx.DiGraph()
    for i in reversed(xrange(1, log_delta + 1)):
        edges = []
        for c in C[i]:
            S = c.copy()
            for u in pi:
                B = S.intersection(set([v for v in g.nodes()
                                        if dists[u][v] < ri[i - 1]]))
                if len(B) != 0:
                    C[i - 1].append(B)
                    S -= B
                    edges.append((repr(c), repr(B), 2**i))
                    if len(B) > 1:
                        plt.gca().add_patch(plt.Circle(pos[u], ri[i - 1],
                                                       fc='none', ec='g'))
        T.add_weighted_edges_from(edges)
        if len(C[i - 1]) == nx.number_of_nodes(g):
            break
    return T


def draw_results(g, pos, T, r):
    A = nx.drawing.nx_agraph.to_agraph(T)
    arg = '-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8'
    A.layout('dot', args=arg)
    A.draw('hierarchical_tree_decomposition.png')

    nx.draw_networkx(g, pos=pos, node_color='#ff9999')
    plt.gca().set_aspect('equal')
    plt.gca().set_xlim(-1.1 * r, 1.1 * r)
    plt.gca().set_ylim(-1.1 * r, 1.1 * r)


if __name__ == '__main__':
    r = 2**9
    g, pos = get_instance(r)
    dists, log_delta = get_distances(g)
    ri, pi = random_parameter(log_delta, nx.number_of_nodes(g))
    print 'ri:', str(['{0:.2f}'.format(n) for n in ri]).replace("'", "")
    print 'pi:', pi 

    T = hierarchical_decomposition(g, pos, dists, ri, pi)
    draw_results(g, pos, T, r)
    plt.savefig('embedded_graph_img.png', bbox_inches='tight')
