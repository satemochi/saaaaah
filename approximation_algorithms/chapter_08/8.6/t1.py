from tutte_embedding import tutte_embedding
from collections import defaultdict
from itertools import combinations, groupby
import math
from operator import mul
import random
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np


def gen_pair_and_demand(n, max_demand=10):
    numbers = range(n)
    seen = set()
    while True:
        pair = tuple(sorted(random.sample(numbers, 2)))
        if pair not in seen:
            seen.add(pair)
            yield (pair, random.randint(1, max_demand))


def get_instance(r, k=3):
    g = nx.petersen_graph()
    pos = tutte_embedding(g).rpos()
    pos = {k: np.array(map(mul, v, [r, r])) for k, v in pos.items()}
    for u, v in g.edges():
        g[u][v]['weight'] = np.linalg.norm(pos[u] - pos[v])
    gen = gen_pair_and_demand(nx.number_of_nodes(g))
    return g, pos, [gen.next() for i in xrange(k)]


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
    T = nx.Graph()
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
                    edges.append((repr(c), repr(B), 2**(i-1)))
                    if len(B) > 1:
                        plt.gca().add_patch(plt.Circle(pos[u], ri[i - 1],
                                                       fc='none', ec='g'))
        T.add_weighted_edges_from(edges)
        if len(C[i - 1]) == nx.number_of_nodes(g):
            break
    return T


def draw_dist_gaps(dists, T, t):
    Tdists = dict(nx.all_pairs_dijkstra_path_length(T))
    tdists = dict(nx.all_pairs_dijkstra_path_length(t))
    x, o, a, a2 = [], [], [], []
    for u, v in combinations(range(nx.number_of_nodes(g)), 2):
        x.append(repr((u, v)))
        o.append(dists[u][v])
        a.append(Tdists[repr(set([u]))][repr(set([v]))])
        a2.append(tdists[repr(set([u]))][repr(set([v]))])
    plt.clf()
    i = range(len(o))
    plt.bar(i, a2, label=r"tree metrics $(V, T')$")
    plt.bar(i, a, label=r"tree metrics $(V', T)$")
    plt.bar(i, o, label="original")
    plt.legend(loc='best')
    plt.xticks(i, x, rotation=90)


def draw_snapshot(g, s, pos, i=0):
    plt.cla()
    nx.draw_networkx(g, pos)
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    plt.gca().set_title(repr(s))
    plt.savefig('a' + str(i).zfill(2) + '.png', bbox_inches='tight')


def draw_contraction(T):
    t = T.copy()
    stack = [v for v in t.nodes() if len(eval(v)) == 1]
    pos = nx.spring_layout(t)
    draw_snapshot(t, stack, pos)

    i = 1
    while stack:
        v = stack.pop()
        for w in t[v]:
            if len(eval(w)) > 1:
                t = nx.contracted_edge(t, (v, w), self_loops=False)
#                stack.append(v)
                stack = [v] + stack
                draw_snapshot(t, stack, pos, i)
                i += 1
                break
    for u, v in t.edges():
        t[u][v]['weight'] *= 4
    draw_snapshot(t, stack, pos, i)
    return t


def buy_at_bulk_network(g, st, t):
    for x, y in t.edges():
        u, v = next(iter(eval(x))), next(iter(eval(y)))
        t[x][y]['original_shortest_path'] = nx.dijkstra_path(g, u, v)

    paths = []
    for (si, ti), demand in st:
        p = nx.dijkstra_path(t, repr(set([si])), repr(set([ti])))
        route = [si]
        for a, b in zip(p[:-1], p[1:]):
            e = t[a][b]['original_shortest_path']
            if next(iter(eval(a))) == e[0]:
                route = route + e[1:]
            else:
                route = route + e[::-1][1:]
        paths.append(list(x.next() for i, x in groupby(route)))
        for u, v in zip(paths[-1][:-1], paths[-1][1:]):
            if 'cost' in g[u][v]:
                g[u][v]['cost'] += demand
            else:
                g[u][v]['cost'] = demand
    return paths


def draw_cost(g, pos):
    plt.figure(figsize=(4, 4))
    plt.gca().set_aspect('equal')
    nx.draw_networkx(g, pos)
    costs = [g[u][v]['cost'] * 0.2 for u, v in g.edges() if 'cost' in g[u][v]]
    nx.draw_networkx_edges(g, pos, width=costs)
    plt.savefig('network_with_weighted_edges.png', bbox_inches='tight')


if __name__ == '__main__':
    plt.figure(figsize=(11, 4))
    r = 2**9
    g, pos, st = get_instance(r)
    print st
    dists, log_delta = get_distances(g)
    ri, pi = random_parameter(log_delta, nx.number_of_nodes(g))

    T = hierarchical_decomposition(g, pos, dists, ri, pi)
    t = draw_contraction(T)
    draw_dist_gaps(dists, T.to_undirected(), t)
    plt.savefig('dist_gaps2.png', bbox_inches='tight')

    paths = buy_at_bulk_network(g, st, t)
    draw_cost(g, pos)
