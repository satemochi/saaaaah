from functools import reduce
from random import randint, seed
from matplotlib import pyplot as plt
import networkx as nx
from networkx.algorithms.flow import edmonds_karp


def gomory_hu_tree(g, cap='capacity', flow_func=edmonds_karp):
    root = next((iter_nodes := iter(g)))
    tree, w = {v: root for v in iter_nodes}, {}
    rg = build_residual_network(g, cap)
    for s in tree:
        w[s, t], (sp, _) = nx.minimum_cut(g, s, (t := tree[s]), capacity=cap,
                                          flow_func=flow_func, residual=rg)
        for v in sp:
            if v not in (s, root) and tree[v] == t:
                tree[v], w[v, s] = s, w.get((v, t), w[s, t])
    T = nx.Graph()
    T.add_weighted_edges_from(((u, v, w[(u, v)]) for u, v in tree.items()))
    return T


def build_residual_network(g, capacity):
    assert(g.size() == len(g.edges(data=True)))
    r = nx.DiGraph(reduce(lambda x, e: x+[e, (e[1], e[0], e[2])],
                          g.edges(data=True), []))
    r.graph['inf'] = 3 * sum(g[u][v][capacity] for u, v in g.edges)
    return r


def graph_setting(s):
    g = nx.frucht_graph()
    seed(s)
    for u, v in g.edges:
        g[u][v]['capacity'] = randint(1, 10)
    return g


if __name__ == '__main__':
    g = graph_setting(0)
    tree = gomory_hu_tree(g)

    pos = nx.spring_layout(g)

    nx.draw_networkx_nodes(g, pos, node_color='#ffcccc')
    nx.draw_networkx_edges(g, pos, alpha=0.25)
    nx.draw_networkx_labels(g, pos)
    
    nx.draw_networkx_edges(tree, pos, edge_color='r')

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.savefig('gomory_hu_tree_01.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
