from collections import ChainMap, deque
from pprint import pprint
from random import seed, sample
from matplotlib import pyplot as plt
import networkx as nx


def gen(n=10, s=1):
    g, p = nx.complete_bipartite_graph(n, n), {}
    a, b = nx.bipartite.sets(g)
    seed(s)
    for u, v in zip(a, b):
        p[u] = deque(sample(b, n))
        p[v] = sample(a, n)
    pprint(p)
    return g, p


def gale_shapley(p):
    m, (stack, _) = {}, nx.bipartite.sets(g)
    while stack:
        v = stack.pop()
        w = p[v].popleft()
        if w not in m:
            m[w] = v
        else:
            if p[w].index(v) < p[w].index(m[w]):
                if p[m[w]]:
                    stack.add(m[w])
                m[w] = v
            elif p[v]:
                stack.add(v)
    return m.items()


def draw(g, matching):
    pos = get_pos(g)
    nx.draw_networkx_edges(g, pos, alpha=0.25)
    for v, c in zip(nx.bipartite.sets(g), ['#ffcccc', '#ccccff']):
        nx.draw_networkx_nodes(g, pos, nodelist=v, node_color=c)
    nx.draw_networkx_edges(g, pos, edgelist=matching, edge_color='g', width=2)
    nx.draw_networkx_labels(g, pos)
    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.savefig('gale_shapley_01.png', bbox_inches='tight')
    plt.show()


def get_pos(g):
    return ChainMap(*[{v: (a*len(V), i) for i, v in enumerate(V)}
                      for a, V in enumerate(nx.bipartite.sets(g))])


if __name__ == '__main__':
    g, p = gen(10)
    draw(g, gale_shapley(p))
