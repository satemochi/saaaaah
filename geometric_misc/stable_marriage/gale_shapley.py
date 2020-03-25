from collections import ChainMap, deque
from pprint import pprint
import random
from matplotlib import pyplot as plt
import networkx as nx


def gen(n=10, seed=1):
    g = nx.complete_bipartite_graph(n, n)
    a, b = nx.bipartite.sets(g)
    random.seed(seed)
    for u, v in zip(a, b):
        g.nodes[u]['p'] = deque(random.sample(b, n))
        g.nodes[v]['p'] = random.sample(a, n)
    pprint(nx.get_node_attributes(g, 'p'))
    return g


def get_pos(g):
    return ChainMap(*[{v: [a*len(V), i] for i, v in enumerate(V)}
                      for a, V in enumerate(nx.bipartite.sets(g))])


def gale_shapley(g):
    m, (stack, _) = {}, nx.bipartite.sets(g)
    while stack:
        v = stack.pop()
        w = g.nodes[v]['p'].popleft()
        if w not in m:
            m[w] = v
        else:
            u = m[w]
            if g.nodes[w]['p'].index(v) < g.nodes[w]['p'].index(u):
                stack.add(u)
                m[w] = v
            else:
                stack.add(v)
    return m.items()


def draw(g, mat):
    pos = get_pos(g)
    nx.draw_networkx_edges(g, pos, alpha=0.25)
    for v, c in zip(nx.bipartite.sets(g), ['#ffcccc', '#ccccff']):
        nx.draw_networkx_nodes(g, pos, nodelist=v, node_color=c)
    nx.draw_networkx_edges(g, pos, edgelist=mat, edge_color='g', width=2)
    nx.draw_networkx_labels(g, pos)
    plt.savefig('gale_shapley_01.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    g = gen(10)
    draw(g, gale_shapley(g))
