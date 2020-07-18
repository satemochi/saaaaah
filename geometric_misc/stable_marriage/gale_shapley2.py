import networkx as nx


def gale_shapley(g, p):
    stack, _ = nx.bipartite.sets(g)
    m, i = {}, {u: 0 for u in stack}
    while stack:
        w, i[v] = p[(v:=stack.pop())][i[v]], i[v]+1
        if w not in m:
            m[w] = v
        else:
            if p[w].index(v) < p[w].index(m[w]):
                if i[m[w]] < len(p[m[w]]):
                    stack.add(m[w])
                m[w] = v
            elif i[v] < len(p[v]):
                stack.add(v)
    return m


def is_stable_exhaustive(g, p, m):
    from itertools import product
    inv = {v: w for w, v in m.items()}
    return not any((p[v].index(w) < p[v].index(inv[v]) and
                    p[w].index(v) < p[w].index(m[w]))
                   for v, w in product(*nx.bipartite.sets(g)))


def draw(g, matching):
    from matplotlib import pyplot as plt
    pos = get_pos(g)
    nx.draw_networkx_edges(g, pos, alpha=0.25)
    for v, c in zip(nx.bipartite.sets(g), ['#ffcccc', '#ccccff']):
        nx.draw_networkx_nodes(g, pos, nodelist=v, node_color=c)
    nx.draw_networkx_edges(g, pos, edgelist=matching, edge_color='g', width=2)
    nx.draw_networkx_labels(g, pos)
    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.savefig('gale_shapley2_01.png', bbox_inches='tight')
    plt.show()


def get_pos(g):
    from collections import ChainMap
    return ChainMap(*[{v: (a*len(V), len(V)-i) for i, v in enumerate(V)}
                      for a, V in enumerate(nx.bipartite.sets(g))])


def gen(n=10, s=1):
    from random import sample, seed
    g, p = nx.complete_bipartite_graph(n, n), {}
    a, b = nx.bipartite.sets(g)
    seed(s)
    for u, v in zip(a, b):
        p[u], p[v] = sample(b, n), sample(a, n)
    from pprint import pprint
    pprint(p)
    return g, p


if __name__ == '__main__':
    g, p = gen(10)
    matching = gale_shapley(g, p)
    print('stable' if is_stable_exhaustive(g, p, matching) else 'not stable')
    draw(g, matching.items())
